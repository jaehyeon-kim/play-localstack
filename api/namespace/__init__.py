from flask_restplus import Api

from .records import ns as records

api = Api(
    title="play with localstack",
    version="1.0",
    prefix="/api"
)

api.add_namespace(records, "/record")
