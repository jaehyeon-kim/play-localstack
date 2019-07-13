import os
import time
import requests
import boto3

AWS_DEFAULT_REGION = os.environ["AWS_DEFAULT_REGION"]
MAX_WAIT_SEC = int(os.getenv("MAX_WAIT_SEC", 10))


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
            requests.get(set_endpoint_url("sqs"))
            requests.get(set_endpoint_url("lambda"))
            break
        except Exception as e:
            print(e)

        if this_trial > MAX_WAIT_SEC:
            raise Exception("Service not available")

        time.sleep(1)


def create_queue(client, name, attributes):
    print("create queue - {0}".format(name))
    try:
        resp_queue = client.create_queue(
            QueueName=name, 
            Attributes=attributes
        )
        print(">>>>>>>>>> queue created <<<<<<<<<<")
        print(resp_queue)
    except Exception as e:
        print(e)


def create_lambda(client, name, **kwargs):
    print("create function - {0}".format(name))
    try:
        runtime = kwargs["runtime"] if "runtime" in kwargs else "python3.6"
        memory = kwargs["memory"] if "memory" in kwargs else 128
        environment = {}
        if "envars" in kwargs:
            environment.update({"Variables": kwargs["envars"]})
        if "bucket" in kwargs:
            code={"S3Bucket": kwargs["bucket"], "S3Key": kwargs["key"]}
        else:
            code={'ZipFile': open(kwargs["path"], "rb").read()}

        resp = client.create_function(
            FunctionName=name,
            Runtime=runtime,
            Role="arn:aws:iam::123456:role/{0}".format(name.lower()),
            Handler="lambda_function.lambda_handler",
            Code=code,
            MemorySize=memory,
            Environment=environment
        )
        print(">>>>>>>>>> lambda created <<<<<<<<<<")
        print(resp)
    except Exception as e:
        print(e)


def create_event_source_mapping(client, name, eventArn, **kwargs):
    print("create event source mapping to function - {0}".format(name))
    try:
        batchsize = kwargs["batchsize"] if "batchsize" in kwargs else 10
        resp = client.create_event_source_mapping(
            EventSourceArn=eventArn,
            FunctionName=name,
            BatchSize=batchsize
        )
        print(">>>>>>>>>> event source mapping created <<<<<<<<<<")
        print(resp)
    except Exception as e:
        print(e)



# BUCKET_NAME = os.environ["BUCKET_NAME"]
# s3 = set_client("s3")
## create S3 bucket and upload lambda package
# create bucket
# create_bucket(s3, BUCKET_NAME)

# upload lambda package
# upload_obj(s3, BUCKET_NAME, PKG_NAME)

# def create_bucket(client, name, region=None):
#     print("create bucket - {0}".format(name))
#     try:
#         config = {"LocationConstraint": AWS_DEFAULT_REGION if region is None else region}
#         resp_bucket = client.create_bucket(
#             ACL="public-read",
#             Bucket=name,
#             CreateBucketConfiguration=config
#         )
#         print(">>>>>>>>>> bucket created <<<<<<<<<<")
#         print(resp_bucket)
#     except Exception as e:
#         print(e)
#         print(">>>>>>>>>> check if {0} exists <<<<<<<<<<".format(name))
#         print(client.list_buckets()["Buckets"])


# def upload_obj(client, bucket, key):
#     print("upload object to s3://{0}/{1}".format(bucket, key))
#     try:
#         with open("/tmp/lambdas/{0}".format(key), "rb") as pkg:
#             client.upload_fileobj(pkg, bucket, key)
#         contents = client.list_objects_v2(Bucket=bucket)["Contents"]
#         print(">>>>>>>>>> object uploaded <<<<<<<<<<")
#         print([c for c in contents if c['Key'] == key])
#     except Exception as e:
#         print(e)