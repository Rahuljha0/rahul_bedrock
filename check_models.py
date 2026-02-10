import boto3
import json

session = boto3.Session()
bedrock = session.client('bedrock', region_name='us-east-1')

try:
    response = bedrock.list_foundation_models()
    print("Available models in your account:\n")
    for model in response.get('modelSummaries', []):
        print(f"Model ID: {model['modelId']}")
        print(f"  Name: {model['modelName']}")
        print(f"  Provider: {model['providerName']}")
        print(f"  Status: {model.get('modelLifecycle', {}).get('status', 'N/A')}")
        print()
except Exception as e:
    print(f"Error listing models: {e}")
