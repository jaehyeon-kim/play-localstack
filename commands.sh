# https://github.com/MathiasBojda/sqs-localstack-lambda
aws --endpoint-url http://localhost:4574 lambda invoke \
    --function-name dev-lambda '{}'

aws --endpoint-url http://localhost:4576 sqs send-message \
    --queue-url http://localhost:4576/queue/test-queue \
    --message-body '{"id": null, "message": "test"}'


aws --endpoint-url http://localhost:4576 sqs send-message \
    --queue-url http://localhost:4576/queue/test-queue \
    --message-body '{"id": 1, "message": "test"}'


aws --endpoint-url http://localhost:4576 sqs receive-message \
    --queue-url http://localstack:4576/queue/dev-queue

##
FLASK_APP=api FLASK_ENV=development flask run

http http://localhost:5000/api/records

http http://localhost:5000/api/records/1

echo '{"message": "test post"}' | \
    http POST http://localhost:5000/api/records

echo '{"message": "test put"}' | \
    http PUT http://localhost:5000/api/records/4