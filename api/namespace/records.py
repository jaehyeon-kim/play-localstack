from flask import jsonify
from flask_restplus import Resource, Namespace

from api.db import conn_db

ns = Namespace("records")


@ns.route("/")
class Records(Resource):
    parser = ns.parser()
    parser.add_argument("record", type=str, required=True)

    def get(self):
        conn = conn_db()
        cur = conn.cursor(real_dict_cursor=True)
        cur.execute("""
            SELECT * FROM records ORDER BY created_on DESC
        """
        )

        records = cur.fetchall()
        return jsonify(records)
    
    @ns.expect(parser)
    def post(self):
        conn = conn_db()
        cur = conn.cursor(real_dict_cursor=True)
        cur.execute("""
            INSERT INTO records (record, source) 
                VALUES (%(record)s)
                RETURNING *
        """, {
            "record": self.parser.parse_args()["record"],
            "source": "web"    
        })

        return jsonify(cur.fetchone())


@ns.route("/<string:id>")
class Record(Resource):
    parser = ns.parser()
    parser.add_argument("record", type=str, required=True)

    def get(self, id):
        conn = conn_db()
        cur = conn.cursor(real_dict_cursor=True)
        cur.execute("""
            SELECT * FROM records WHERE id = %(id)s
        """, {"id": id})

        record = cur.fetchone()
        if record is None:
            return {"message": "No record"}, 404
        return jsonify(record)

    @ns.expect(parser)
    def put(self):

        message = {
            "record": self.parser.parse_args()["record"],
            "source": "queue"
        }

        return "", 204