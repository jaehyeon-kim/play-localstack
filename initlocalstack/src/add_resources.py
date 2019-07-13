import os
import boto3
from utils import wait_for_services, create_queue, \
    create_execution_role, create_lambda, create_event_source_mapping

wait_for_services()

QUEUE_NAME = os.environ["QUEUE_NAME"]
FUNCTION_NAME = os.environ["FUNCTION_NAME"]
PKG_PATH = os.environ["PKG_PATH"]
IS_LOCAL_STACK = os.environ["IS_LOCAL_STACK"]
DB_CONNECT = os.environ["DB_CONNECT"]


## create queue
#attributes = {"DelaySeconds": "1", "FifoQueue": "true"}
attributes = {"DelaySeconds": "1"}
create_queue(QUEUE_NAME, attributes)
QUEUE_ARN = "arn:aws:sqs:ap-southeast-2:queue:{0}".format(QUEUE_NAME)

##  create lambda function and event source mapping
role = create_execution_role(FUNCTION_NAME)
role_arn = role["Role"]["Arn"]

envars = {
    "IS_LOCAL_STACK": IS_LOCAL_STACK, "DB_CONNECT": DB_CONNECT, "QUEUE_NAME": QUEUE_NAME
}
create_lambda(FUNCTION_NAME, path=PKG_PATH, envars=envars, role=role_arn)

create_event_source_mapping(FUNCTION_NAME, QUEUE_ARN)
