import boto3
import json
import sys
import argparse

class BedrockTextGenerator:
    def __init__(self, region='us-east-1', model_id='amazon.nova-lite-v1:0', debug=False):
        self.session = boto3.Session()
        self.bedrock = self.session.client('bedrock-runtime', region_name=region)
        self.model_id = model_id
        self.debug = debug
    
    def generate_text(self, question, max_tokens=1000, timeout=30):
        """Generate text from Bedrock model with proper resource management."""
        # Input validation
        if not question or not isinstance(question, str):
            return "Invalid input: question must be a non-empty string"
        
        if max_tokens > 4000:  # Reasonable upper limit
            max_tokens = 4000
        
        # Different body format for different models
        if 'amazon.nova' in self.model_id:
            body = {
                "messages": [
                    {"role": "user", "content": [{"text": question[:2000]}]}
                ],
                "inferenceConfig": {"max_new_tokens": max_tokens}
            }
        else:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {"role": "user", "content": question[:2000]}  # Limit input length
                ]
            }

        if not self.session.get_credentials():
            return "No AWS credentials configured"

        try:
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )
            result = self._parse_response(response)
            # Ensure response body is properly closed
            if hasattr(response.get('body'), 'close'):
                response['body'].close()
            return result
        except Exception as e:
            return f"Error invoking Bedrock model: {str(e)}"
    
    def _parse_response(self, response):
        """Parse Bedrock response with proper error handling."""
        try:
            raw = response['body'].read()
            raw_str = raw.decode('utf-8', errors='replace') if isinstance(raw, bytes) else str(raw)
            
            response_body = json.loads(raw_str)
            return self._extract_text_content(response_body) or self._fallback_response(response_body)
        except json.JSONDecodeError:
            return "Received non-JSON response from model." if not self.debug else f"Non-JSON response: {raw_str}"
    
    def _extract_text_content(self, response_body):
        """Extract text content from various response formats."""
        if not isinstance(response_body, dict):
            return None
        
        # Try Nova format: output.message.content[0].text
        output = response_body.get('output')
        if output and isinstance(output, dict):
            message = output.get('message')
            if message and isinstance(message, dict):
                content = message.get('content')
                if isinstance(content, list) and content:
                    first = content[0]
                    if isinstance(first, dict) and 'text' in first:
                        return first['text']
            
        # Try content array format (Anthropic)
        content = response_body.get('content')
        if isinstance(content, list) and content:
            first = content[0]
            if isinstance(first, dict):
                return first.get('text') or first.get('content')
            elif isinstance(first, str):
                return first
        
        # Try outputs format
        outputs = response_body.get('outputs')
        if isinstance(outputs, list):
            for out in outputs:
                if isinstance(out, dict):
                    content = out.get('content')
                    if isinstance(content, list):
                        for c in content:
                            if isinstance(c, dict):
                                text = c.get('text') or c.get('content')
                                if text:
                                    return text
        return None
    
    def _fallback_response(self, response_body):
        """Fallback response formatting."""
        res_str = json.dumps(response_body)
        return res_str if len(res_str) < 1000 else res_str[:1000] + '...'

def main():
    parser = argparse.ArgumentParser(description='AWS Bedrock Text Generator')
    parser.add_argument('--test', action='store_true', help='Run a single test prompt non-interactively')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--model-id', default='amazon.nova-lite-v1:0', help='Override model id')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    args = parser.parse_args()

    generator = BedrockTextGenerator(region=args.region, model_id=args.model_id, debug=args.debug)

    if args.test:
        prompt = "Hello, please say something brief."
        print("=== TEST MODE ===")
        print("Prompt:", prompt)
        print("Generating answer...")
        answer = generator.generate_text(prompt)
        print("Answer:", answer)
        return

    print("=== AWS Bedrock Text Generator ===")
    print("Type 'quit' to exit\n")

    while True:
        try:
            question = input("Enter your question: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if question.lower() == 'quit':
            break

        print("\nGenerating answer...")
        answer = generator.generate_text(question)
        print(f"\nAnswer: {answer}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()