import os
import boto3
from utils import wait_for_services, create_queue, \
    get_queue_attributes, create_lambda, create_event_source_mapping

wait_for_services()

QUEUE_NAME = os.environ["QUEUE_NAME"]
FUNCTION_NAME = os.environ["FUNCTION_NAME"]
PKG_PATH = os.environ["PKG_PATH"]
IS_LOCAL_STACK = os.environ["IS_LOCAL_STACK"]
DB_CONNECT = os.environ["DB_CONNECT"]


## create queue
#attributes = {"DelaySeconds": "1", "FifoQueue": "true"}
attributes = {"DelaySeconds": "1"}
resp = create_queue(QUEUE_NAME, attributes)

queueUrl = resp["QueueUrl"]
attributes = ["QueueArn"]
resp = get_queue_attributes(queueUrl, attributes)

qeueArn = resp["Attributes"]["QueueArn"]

##  create lambda function and event source mapping
envars = {
    "IS_LOCAL_STACK": IS_LOCAL_STACK, "DB_CONNECT": DB_CONNECT
}
create_lambda(FUNCTION_NAME, path=PKG_PATH, envars=envars)

create_event_source_mapping(FUNCTION_NAME, qeueArn)
