import os
import logging
import json
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = psycopg2.connect(os.environ["DB_CONNECT"], connect_timeout=5)
except psycopg2.Error as e:
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to DB")

def lambda_handler(event, context):
    for r in event["Records"]:
        body = json.loads(r["body"])
        logger.info("Body: {0}".format(body))
        with conn.cursor() as cur:
            if body["id"] is None:
                cur.execute(
                    """
                    INSERT INTO records (message) VALUES (%(message)s)
                    """, {k:j for k,j in body.items() if j is not None})
            else:
                cur.execute(
                    """
                    UPDATE records
                       SET message = %(message)s
                     WHERE id = %(id)s
                    """, body)
    conn.commit()

    logger.info("SUCCESS: Processing {0} records".format(len(event["Records"])))
