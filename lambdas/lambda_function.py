import json
import boto3


def lambda_handler(event, context):
    print("Hello world")
    return json.dumps({"message": "ok"})