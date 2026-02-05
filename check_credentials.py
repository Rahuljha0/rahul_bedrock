import boto3
import botocore
import json
import os

print('Environment variables (AWS_ACCESS_KEY_ID present?):', 'AWS_ACCESS_KEY_ID' in os.environ)
print('AWS credential profiles file exists?', os.path.exists(os.path.expanduser('~/.aws/credentials')))

sess = boto3.Session()
creds = sess.get_credentials()
print('\nCredentials found:', creds is not None)

if not creds:
    print('\nNo credentials found: set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY env vars, run `aws configure`, or use an IAM role.')
else:
    try:
        sts = sess.client('sts')
        identity = sts.get_caller_identity()
        print('\nSTS GetCallerIdentity:')
        print(json.dumps(identity, indent=2))
    except botocore.exceptions.NoCredentialsError as e:
        print('\nNoCredentialsError:', e)
    except Exception as e:
        print('\nError calling STS:', type(e).__name__, e)
