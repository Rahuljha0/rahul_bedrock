# AWS Bedrock Text Generator Setup

## Prerequisites
1. AWS Account with Bedrock access
2. AWS CLI configured with credentials
3. Python 3.8+

## Setup Steps

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure AWS credentials (one of these methods):
   - AWS CLI: `aws configure`
   - Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
   - IAM role (if running on EC2)

3. Enable Claude model in AWS Bedrock console:
   - Go to AWS Bedrock console
   - Navigate to Model access
   - Request access to Anthropic Claude models

4. Run the application:
   ```
   python bedrock_text_generator.py
   ```

## Usage
- Enter your question when prompted
- Type 'quit' to exit
- The AI will generate and display answers

## Note
Make sure you have proper IAM permissions for bedrock:InvokeModel action.