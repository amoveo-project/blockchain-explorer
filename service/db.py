import psycopg2

from service.settings import DATABASE_URI


class DBWriter:
    def __init__(self):
        self.db = psycopg2.connect(DATABASE_URI)
        self.cur = self.db.cursor()

    def store_transactions(self, txns):
        dataText = b",".join([self.cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", tx) for tx in txns])
        self.cur.execute(b"INSERT INTO transactions VALUES " + dataText + b" ON CONFLICT (hash) DO NOTHING")

    def store_block(self, block):
        dataText = self.cur.mogrify("(%s, %s)", block)
        self.cur.execute(b"INSERT INTO blocks VALUES " + dataText + b" ON CONFLICT (blockNumber) DO NOTHING")

    def get_last_block(self):
        self.cur.execute(b"SELECT blockNumber, timestamp FROM blocks ORDER BY blockNumber DESC LIMIT 1")
        result = self.cur.fetchone()

        return result

    def commit(self):
        self.db.commit()

    def close(self):
        self.cur.close()
        self.db.close()
