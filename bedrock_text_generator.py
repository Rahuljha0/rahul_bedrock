import boto3
import json
import sys
import argparse

class BedrockTextGenerator:
    def __init__(self, region='us-east-1', model_id='anthropic.claude-3-sonnet-20240229-v1:0', debug=False):
        self.session = boto3.Session()
        self.bedrock = self.session.client('bedrock-runtime', region_name=region)
        self.model_id = model_id
        self.debug = debug
    
    def generate_text(self, question, max_tokens=1000):
        """Generate text from Bedrock model.

        This method is defensive: it checks for AWS credentials and attempts to
        parse multiple possible response shapes returned by different models.
        """
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {"role": "user", "content": question}
            ]
        }

        # If there are no AWS credentials configured, return the request for inspection
        if not self.session.get_credentials():
            return f"No AWS credentials configured. Request body: {json.dumps(body)}"

        try:
            response = self.bedrock.invoke_model(
                ModelId=self.model_id,
                Body=json.dumps(body),
                ContentType='application/json',
                Accept='application/json'
            )

            raw = response['body'].read()
            if isinstance(raw, bytes):
                raw_str = raw.decode('utf-8', errors='replace')
            else:
                raw_str = str(raw)

            # Try to parse JSON response
            try:
                response_body = json.loads(raw_str)
            except Exception:
                if self.debug:
                    return f"Non-JSON response from model: {raw_str}"
                return "Received non-JSON response from model."

            # Try multiple common response shapes
            # 1) outputs -> content -> text
            if isinstance(response_body, dict):
                outputs = response_body.get('outputs')
                if outputs and isinstance(outputs, list):
                    for out in outputs:
                        content = out.get('content')
                        if isinstance(content, list):
                            for c in content:
                                if isinstance(c, dict):
                                    text = c.get('text') or c.get('content') or c.get('data')
                                    if text:
                                        return text
                                elif isinstance(c, str):
                                    return c

                # 2) top-level content
                content = response_body.get('content')
                if isinstance(content, list) and content:
                    first = content[0]
                    if isinstance(first, dict):
                        text = first.get('text') or first.get('content')
                        if text:
                            return text
                    elif isinstance(first, str):
                        return first

                # 3) choices/message style
                choices = response_body.get('choices') or response_body.get('items')
                if choices and isinstance(choices, list):
                    first = choices[0]
                    if isinstance(first, dict):
                        # message containing content
                        msg = first.get('message')
                        if msg and isinstance(msg, dict):
                            return msg.get('content') or msg.get('text') or json.dumps(msg)
                        # direct text
                        text = first.get('text') or first.get('content')
                        if text:
                            return text

            # Fallback: return a truncated JSON string of the response
            res_str = json.dumps(response_body)
            return res_str if len(res_str) < 1000 else res_str[:1000] + '...'

        except Exception as e:
            return f"Error invoking Bedrock model: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description='AWS Bedrock Text Generator')
    parser.add_argument('--test', action='store_true', help='Run a single test prompt non-interactively')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--model-id', default=None, help='Override model id')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    args = parser.parse_args()

    model_id = args.model_id if args.model_id else 'anthropic.claude-3-sonnet-20240229-v1:0'
    generator = BedrockTextGenerator(region=args.region, model_id=model_id, debug=args.debug)

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