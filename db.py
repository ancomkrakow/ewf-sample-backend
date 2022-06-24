import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    def __init__(self, conn_string):
        self.conn = psycopg2.connect(conn_string)
        self.conn.set_session(autocommit=True)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def begin(self):
        self.cur.execute("BEGIN")

    def commit(self):
        self.cur.execute("COMMIT")

    def rollback(self):
        self.cur.execute("ROLLBACK")
