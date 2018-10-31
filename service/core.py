import asyncio
import argparse
import logging
import json
import csv
import time
from io import StringIO
from decimal import Decimal

import asyncpg
from aiohttp import web

from .settings import DATABASE_URI


logging.basicConfig(level=logging.INFO, format='[%(levelname)s]: %(asctime)s: %(message)s')


async def transactions(request):
    # sanitize request a little
    query = {}
    allowed = ("address", "fromblock", "toblock", "limit", "sort", "format", "readableAmounts")
    for key in request.rel_url.query:
        if key in allowed: query[key] = request.rel_url.query[key]

    fmt = query.get("format")
    if fmt not in ["json", "csv"]:
        fmt = "json"

    readableAmounts = query.get("readableAmounts") == "true"

    # validate fields
    if not 'address' in query:
        raise web.HTTPBadRequest(text="Valid address must be supplied")

    address = query['address'].replace(' ', '+')

    args = [address, address]
    sql = """SELECT blockNumber, "timestamp", "hash", nonce, "type",
          transactionIndex, "from", "to", amount, fee, extra
          FROM transactions
          WHERE ("from" = $1 OR "to" = $2) """

    if query.get('fromblock'):
        args.append(int(query['fromblock']))
        sql += "AND blockNumber >= $%d " % len(args)

    if query.get('toblock'):
        args.append(int(query['toblock']))
        sql += "AND blockNumber <= $%d " % len(args)

    sort = query.get('sort', None)
    if sort not in ['asc', 'desc']: sort = 'desc'
    sql += "ORDER BY (blockNumber, transactionIndex) %s " % sort

    limit = int(query.get('limit', 100))
    sql += "LIMIT %s" % limit

    pool = request.app['pool']
    async with pool.acquire() as connection:
        rows = await connection.fetch(sql, *args)
        data = []
        for row in rows:
            d = dict(row)
            if d['amount'] is not None:
                d['amount'] = int(d['amount'])
            if d['extra']:
                d['extra'] = json.loads(d['extra'])

            d['fee'] = int(d['fee'])
            data.append(d)

        if fmt == "json":
            return web.Response(
                body=json.dumps({"result": data}),
                headers={"content-type": "application/json"})

        else:
            if data:
                if readableAmounts:
                    for d in data:
                        d['amount'] = Decimal(d['amount']) / Decimal(1e8) if d['amount'] is not None else None
                        d['fee'] = Decimal(d['fee']) / Decimal(1e8) if d['fee'] is not None else None

                stream = StringIO()
                writer = csv.DictWriter(
                    stream,
                    fieldnames=["blocknumber", "transactionindex", "timestamp", "hash", "type",
                                "from", "to", "amount", "fee", "nonce", "extra"])
                writer.writeheader()
                writer.writerows(data)
                text = stream.getvalue()
                stream.close()
            else:
                text = ""

            filename = "%s_%s.csv" % (address, int(time.time()))
            return web.Response(
                body=text,
                headers={"content-type": "text/csv",
                         "content-disposition": "attachment; filename=%s" % filename})


async def get_tx(request):
    txid = request.rel_url.query.get('txid')
    if not txid:
        raise web.HTTPNotFound()

    txid = txid.replace(' ', '+')

    args = [txid]
    sql = """SELECT blockNumber, "timestamp", "hash", nonce, "type",
          transactionIndex, "from", "to", amount, fee, extra
          FROM transactions
          WHERE "hash" = $1 """

    pool = request.app['pool']
    async with pool.acquire() as connection:
        rows = await connection.fetch(sql, *args)
        if not rows:
            raise web.HTTPNotFound()

        d = dict(rows[0])
        if d['amount'] is not None:
            d['amount'] = int(d['amount'])
        if d['extra']:
            d['extra'] = json.loads(d['extra'])

        d['fee'] = int(d['fee'])

        return web.Response(
            body=json.dumps({"result": d}),
            headers={"content-type": "application/json"})

async def init_pg(app):
    app['pool'] = await asyncpg.create_pool(DATABASE_URI)

async def close_pg(app):
    await app['pool'].close()


app = web.Application()
app.add_routes([
    web.get('/api/v1/txlist', transactions),
    web.get('/api/v1/tx', get_tx)
])
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Amoveo explorer API backend")
    parser.add_argument('--host')
    parser.add_argument('--port', default=6050)

    args = parser.parse_args()

    web.run_app(app, host=args.host, port=args.port)
