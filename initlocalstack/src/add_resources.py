import os
import boto3
from utils import wait_for_services, set_client, \
    create_bucket, create_queue

wait_for_services()

BUCKET_NAME = os.environ["BUCKET_NAME"]
QUEUE_NAME = os.environ["QUEUE_NAME"]

## set up clients
s3 = set_client("s3")
sqs = set_client("sqs")

## create S3 bucket (to upload lambda package)
create_bucket(s3, BUCKET_NAME)

## create queue
attributes = {"DelaySeconds": "1", "FifoQueue": "true"}
create_queue(sqs, QUEUE_NAME, attributes)

## set up lambda function
# upload lambda package


# create lambda function


# set event mapping

