import os
import time
import requests
import boto3

AWS_DEFAULT_REGION = os.environ["AWS_DEFAULT_REGION"]
MAX_WAIT_SEC = int(os.environ["MAX_WAIT_SEC"])

def set_endpoint_url(service, hostname="localstack"):
    mapping = {"s3": 4572, "sqs": 4576, "lambda": 4574}
    return "http://{0}:{1}".format(hostname, mapping[service])

def set_client(service, region=None):
    session = boto3.session.Session()
    return session.client(
        service_name=service, 
        endpoint_url=set_endpoint_url(service),
        region_name = AWS_DEFAULT_REGION if region is None else region
    )

def wait_for_services():
    this_trial = 0
    while True:
        this_trial += 1
        print("wait for service - {0}".format(this_trial))
        try:
            requests.get(set_endpoint_url("s3"))
            break
        except Exception as e:
            print(e)

        if this_trial > MAX_WAIT_SEC:
            raise Exception("Service not available")

        time.sleep(1)


def create_bucket(client, name, region=None):
    print("create bucket - {0}".format(name))
    try:
        config = {"LocationConstraint": AWS_DEFAULT_REGION if region is None else region}
        resp_bucket = client.create_bucket(
            ACL="public-read",
            Bucket=name,
            CreateBucketConfiguration=config
        )
        print(resp_bucket)
    except Exception as e:
        print(e)
        print("check if {0} exists".format(name))
        print(client.list_buckets()["Buckets"])


def create_queue(client, name, attributes):
    print("create queue - {0}".format(name))
    try:
        resp_queue = client.create_queue(
            QueueName=name, 
            Attributes=attributes
        )
        print(resp_queue)
    except Exception as e:
        print(e)