aws --endpoint-url http://localhost:4574 lambda invoke \
    --function-name dev-lambda '{}'

aws --endpoint-url http://localhost:4576 sqs send-message \
    --queue-url http://localhost:4576/queue/dev-queue \
    --message-body '{"foo": "bar"}'

aws --endpoint-url http://localhost:4586 logs filter-log-events \
    --log-group-name /aws/lambda/dev-lambda

aws --endpoint-url http://localhost:4586 logs describe-log-groups

aws --endpoint-url http://localhost:4576 sqs receive-message \
    --queue-url http://localhost:4576/queue/dev-queue

# https://github.com/MathiasBojda/sqs-localstack-lambda