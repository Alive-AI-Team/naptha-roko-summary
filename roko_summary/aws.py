import os
import boto3
from dotenv import load_dotenv

load_dotenv()


def get_dynamodb():
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name="us-east-1",
    )
    return dynamodb
