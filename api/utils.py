import os
import json
import boto3
from datetime import datetime
from flask.json import JSONEncoder


def send_message(name, body, delaySec=0):
    session = boto3.session.Session()
    client = session.client(service_name="sqs", endpoint_url="http://localhost:4576")
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