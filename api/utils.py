import flask
import os
import json
import boto3

IS_LOCAL_STACK = flask.current_app.config["IS_LOCAL_STACK"]

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


def send_message(name, body, delaySec=0)
    client = init_service("sqs")
    queueUrl = client.get_queue_url(QueueName=name)["QueueUrl"]
    resp = client.send_message(
        QueueUrl=queueUrl,
        DelaySeconds=delaySec,
        MessageBody=body
    )
    return resp["ResponseMetadata"]["HTTPStatusCode"]


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)