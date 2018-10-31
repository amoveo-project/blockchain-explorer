import base64

def parse_tx(tx):
    data = {"type": tx[0],
            "from": tx[1],
            "nonce": tx[2],
            "fee": tx[3],
            "to": tx[4],
            "amount": None,
            "extra": None}

    if tx[0] == "create_acc_tx":
        data.update({"amount": tx[5]})

    elif tx[0] == "spend":
        data.update({"amount": tx[5]})

    elif tx[0] == "delete_acc_tx":
        pass

    elif tx[0] == "nc":
        data.update({"to": tx[2], "fee": tx[3], "nonce": tx[4], "extra": {
            "bal1": tx[5], "bal2": tx[6], "delay": tx[7], "id": tx[8]
        }})

    elif tx[0] == "csc":
        data.update({"to": None, "extra": {
            "scriptpubkey": tx[4], "scriptsig": tx[5]
        }})

    elif tx[0] == "cs":
        data.update({"to": None, "extra": {
            "scriptpubkey": tx[4], "scriptsig": tx[5]
        }})

    elif tx[0] == "ctc":
        data.update({"to": tx[2], "fee": tx[3], "nonce": tx[4],
                     "amount": tx[6], "extra": {
                         "id": tx[5]
                    }})

    elif tx[0] == "timeout":
        data.update({"to": None, "extra": {
            "cid": tx[4], "spk_aid1": tx[5], "spk_aid2": tx[6]
        }})

    elif tx[0] == "oracle_new":
        data.update({"to": None, "extra": {
            "question": tx[4] and base64.b64decode(tx[4]).decode('utf-8'),
            "start": tx[5], "id": tx[6],
            "difficulty": tx[7], "governance": tx[8], "governance_amount": tx[9]
        }})

    elif tx[0] == "oracle_bet":
        data.update({"amount": tx[6], "extra": {"type": tx[5]}})

    elif tx[0] == "oracle_close":
        pass

    elif tx[0] == "unmatched":
        pass

    elif tx[0] == "oracle_winnings":
        pass

    elif tx[0] == "coinbase":
        data.update({"to": None})

    elif tx[0] == "nc_accept":
        offer = tx[2][1]
        data.update({"to": offer[1], "nonce": offer[2], "extra": {
            "bal1": offer[4], "bal2": offer[5], "nlocktime": offer[3],
            "delay": offer[7], "id": offer[8], "contract_hash": offer[9],
            "miner_commission": offer[6]}})

    return data
