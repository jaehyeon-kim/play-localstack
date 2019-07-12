import flask
from flask import g
import psycopg2
from psycopg2.extras import RealDictCursor


class PostgreSQLConnection(psycopg2.extensions.connection):
    def cursor(self, real_dict_cursor=False):
        """
        Get a new cursor.
        If real_dict_cursor is set, a RealDictCursor is returned
        """
        kwargs = {}
        if real_dict_cursor:
            kwargs["cursor_factory"] = RealDictCursor
        return super(PostgreSQLConnection, self).cursor(**kwargs)


def conn_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            flask.current_app.config["DB_CONNECT"], connection_factory=PostgreSQLConnection
        )

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def commit(response=None):
    if "db" in g:
        g.db.commit()

    return response


def init_app(app):
    app.after_request(commit)
    app.teardown_appcontext(close_db)
