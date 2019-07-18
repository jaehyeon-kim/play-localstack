import os
import json
import boto3
import psycopg2

IS_LOCAL_STACK = os.environ["IS_LOCAL_STACK"]
DB_CONNECT = os.environ["DB_CONNECT"]

def set_endpoint_url(service, hostname="localhost"):
    mapping = {"s3": 4572, "sqs": 4576, "lambda": 4574, "iam": 4593, "logs":4586}
    return "http://{0}:{1}".format(hostname, mapping[service])


def init_service(service, is_client=True, region=None):
    session = boto3.session.Session()
    args = {"service_name": service}
    if IS_LOCAL_STACK == "1":
        args.update({
            "endpoint_url": set_endpoint_url(service),
            "region_name": "ap-southeast-2" if region is None else region
        })
    return session.client(**args) if is_client else session.resource(**args)


def process_messages(name):
    resource = init_service("sqs", is_client=False)
    queue = resource.get_queue_by_name(QueueName=name)
    for message in queue.receive_messages():
        body = message.body
        print(json.loads(body))
        message.delete()


def lambda_handler(event, context):
    print(event)
    # try:
    #     process_messages(QUEUE_NAME)
    # except Exception as e:
    #     print("fails to process messages")
    #     print(e)
    
    # print("Hello world")
    # return json.dumps({"message": "ok"})