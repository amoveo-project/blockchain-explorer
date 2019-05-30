# Amoveo blockchain explorer
This project offers API-enabled Amoveo blockchain explorer. It has no UI (at least at the moment) at all. It stores every transaction with its metadata into PostgreSQL database and allows to request transactions etc. API can be easily extended.

## Build
You need python3.5+ and PostgreSQL 9+ to run this project.
Also you will need Amoveo full node with access to its internal API (i.e. port 8081 accessible).
Steps to start:
```
$ virtualenv -p python3 .  # create virtualenv for the project
$ . bin/activate  # activate virtualenv
$ pip install .   # install dependencies
```
Next you need to configure parameters in `service/settings_local.py` looking on `settings.py`: `NODE_EXT_URL`, `NODE_INT_URL` and `DATABASE_URI` for db connection.

Next you can run network listener and API in different shells:
```
$ python -m service.core       # starting API service
$ python -m service.network    # starting network listener
```

## Deployment

Manual start should not be used on production instances. There is `package` directory containing script to build Debian package with the whole virtualenv inside. Also, there are `supervisor` config files for starting both services in `package/debian/etc/supervisor/conf.d`.

## Usage
#### Request transaction by txid
`GET /api/v1/tx?txid=<txid>`
where `txid` is not url-encoded.

Response contains obvious fields. All the amounts are in satoshis (1e-8 VEO). Own address in `from` or `to` shows whether tx was sent or received.

**Please note:**
* `amount` can be null or zero. It’s possible for some specific tx types.
* `to` can be absent also

Basic `spend` and `create_acc_tx` transactions will do have these fields, but another types can be different. `extra` field can contain additional info for specific transactions.

#### Transaction list by account

`GET /api/v1/txlist?address=<pubkey>`
where `pubkey` is not url-encoded.

Transactions are returned in descending order by block number. Optional GET-parameter `limit=N` allows to limit the output to N records. Optional GET-parameter `format=json|csv` can switch output to `text/csv`. Default format is `json`.

## License
The project is licensed under the Apache License 2.0.
