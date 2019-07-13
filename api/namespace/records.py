import json
from flask import jsonify
from flask_restplus import Resource, Namespace
import boto3

from api.db import conn_db
from api.utils import send_message

QUEUE_NAME = flask.current_app.config["QUEUE_NAME"]

ns = Namespace("records")

@ns.route("/")
class Records(Resource):
    parser = ns.parser()
    parser.add_argument("record", type=str, required=True)

    def get(self):
        """
        Get all records
        """        
        conn = conn_db()
        cur = conn.cursor(real_dict_cursor=True)
        cur.execute(
            """
            SELECT * FROM records ORDER BY created_on DESC
            """)

        records = cur.fetchall()
        return jsonify(records)
    
    @ns.expect(parser)
    def post(self):
        """
        Create a record via queue
        """
        try:
            body = {"record": self.parser.parse_args()["record"]}
            send_message(QUEUE_NAME, json.dumps(body))
            return "", 204
        except Exception as e:
            return "", 500


@ns.route("/<string:id>")
class Record(Resource):
    parser = ns.parser()
    parser.add_argument("record", type=str, required=True)

    def get(self, id):
        """
        Get a record given id
        """        
        record = Record.get_record(id)
        if record is None:
            return {"message": "No record"}, 404
        return jsonify(record)

    @ns.expect(parser)
    def put(self, id):
        """
        Update a record via SQS
        """
        record = Record.get_record(id)
        if record is None:
            return {"message": "No record"}, 404        

        try:
            message = {
                "id": record["id"],
                "record": self.parser.parse_args()["record"],
                "num_changed": record["num_changed"] + 1
            }
            send_message(QUEUE_NAME, json.dumps(body))
            return "", 204
        except Exception as e:
            return "", 500

    @staticmethod
    def get_record(id):
        conn = conn_db()
        cur = conn.cursor(real_dict_cursor=True)
        cur.execute(
            """
            SELECT * FROM records WHERE id = %(id)s
            """, {"id": id})

        return cur.fetchone()
