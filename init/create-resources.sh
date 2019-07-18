#!/bin/bash

echo "Creating $TEST_QUEUE and $FUNCTION_NAME"

aws --endpoint-url=http://localhost:4576 sqs create-queue \
    --queue-name $TEST_QUEUE

aws --endpoint-url=http://localhost:4574 lambda create-function \
    --function-name $TEST_LAMBDA \
    --code S3Bucket="__local__",S3Key="/tmp/lambda_package" \
    --runtime python3.6 \
    --environment Variables="{DB_CONNECT=$DB_CONNECT}"
    --role arn:aws:lambda:ap-southeast-2:000000000000:function:$TEST_LAMBDA \
    --handler lambda_function.lambda_handler \

aws --endpoint-url=http://localhost:4574 lambda create-event-source-mapping \
    --function-name $TEST_LAMBDA \
    --event-source-arn arn:aws:sqs:elasticmq:000000000000:$TEST_QUEUE
