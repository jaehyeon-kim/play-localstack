import os
import boto3
from utils import wait_for_services, set_client, \
    create_queue, create_lambda, create_event_source_mapping

wait_for_services()

QUEUE_NAME = os.environ["QUEUE_NAME"]
FUNCTION_NAME = os.environ["FUNCTION_NAME"]
PKG_PATH = os.environ["PKG_PATH"]

## set up clients
sqs = set_client("sqs")
lambda_client = set_client("lambda")

## create queue
attributes = {"DelaySeconds": "1", "FifoQueue": "true"}
create_queue(sqs, QUEUE_NAME, attributes)
QUEUE_ARN = "arn:aws:sqs:ap-southeast-2:queue:{0}".format(QUEUE_NAME)

##  create lambda function and event source mapping
envars = {"foo": "bar"}
create_lambda(lambda_client, FUNCTION_NAME, path=PKG_PATH, envars=envars)

create_event_source_mapping(lambda_client, FUNCTION_NAME, QUEUE_ARN)
