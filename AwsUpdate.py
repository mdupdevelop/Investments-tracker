import os
import boto3
from botocore.exceptions import ClientError

print("Updating to AWS")

ACCESS_KEY = os.environ.get('AWS_ACCESSKEY')
SECRET_KEY = os.environ.get('AWS_SECRETKEY')


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False



uploadedT212 = upload_to_aws('Trading212Trades.csv', 'investingreporting', 'Trading212Trades.csv')
uploadedGemini = upload_to_aws('GeminiTrades.csv', 'investingreporting', 'Trading212Trades.csv')