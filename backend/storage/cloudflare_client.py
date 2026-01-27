import boto3
from botocore.config import Config
import os

account_id = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
access_key = os.environ.get('R2_ACCESS_KEY_ID')
secret_key = os.environ.get('R2_SECRET_ACCESS_KEY')
bucket_name = os.environ.get('R2_BUCKET')
my_endpoint_url = os.environ.get('CLOUDFLARE_ENDPOINT_UR')

s3 = boto3.client(
    's3',
    endpoint_url = my_endpoint_url,
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key,
    config = Config(signature_version='s3v4'),
    region_name='auto'
)



