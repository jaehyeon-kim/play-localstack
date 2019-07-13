FROM python:3.6

RUN pip install \
    awscli \
    awscli-local \
    requests \
    localstack-client \
    --upgrade

ENTRYPOINT ["/docker-entrypoint.sh"]
