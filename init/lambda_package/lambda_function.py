import os
import psycopg2

def lambda_handler(event, context):
    print(os.environ["DB_CONNECT"])
    print(event)
