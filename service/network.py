import time
import requests
import json
import logging

from service.model import parse_tx
from service.db import DBWriter

from service.settings import NODE_EXT_URL, NODE_INT_URL


logging.basicConfig(level=logging.INFO, format='[%(levelname)s]: %(asctime)s: %(message)s')


db = DBWriter()

last_top, _ = db.get_last_block() or (37000, 0)

logging.info("Starting from %s" % last_top)

while True:
    data = requests.post(NODE_INT_URL,
                         json=["top"]).json()
    height = data[1][2]

    size = min(height - last_top, 500)

    if size > 0:
        headers = requests.post(NODE_EXT_URL,
                                json=["headers", size + 1, last_top]).json()[1][1:]

        for idx, block in enumerate(range(last_top, last_top + size + 1)):
            data = requests.post(NODE_INT_URL,
                                 json=["block", 3, block]).json()

            data, hashes = data[1][1][1:], data[1][2][1:]
            txs = zip([x[1] for x in data], hashes)

            timestamp = (headers[idx][5] + 15192951759) // 10

            db.store_block((block, timestamp))

            txns = []
            for tidx, (tx, _hash) in enumerate(txs):
                txi = parse_tx(tx)
                txns.append((
                    block,
                    timestamp,
                    _hash,
                    txi['nonce'],
                    tidx,
                    txi['from'],
                    txi['to'],
                    txi['amount'],
                    txi['fee'],
                    txi['type'],
                    txi['extra'] and json.dumps(txi['extra'])
                ))

            if len(txns):
                db.store_transactions(txns)

            logging.info("Handling block %d, tx count %d" % (block, len(txns)))
            db.commit()

            last_top = block

    time.sleep(20)

db.close()
