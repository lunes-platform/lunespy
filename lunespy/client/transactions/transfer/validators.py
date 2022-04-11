def serialize_transfer(**tx: dict) -> bytes:
    from lunespy.client.transactions.constants import TransferType
    from lunespy.utils.crypto.converters import b58_to_bytes
    from struct import pack

    return (
        TransferType.to_byte.value + \
        b58_to_bytes(tx["sender_public_key"]) + \
        (b'\1' + b58_to_bytes(tx["token_id"]) if tx["token_id"] != "" else b'\0') + \
        (b'\1' + b58_to_bytes(tx["token_fee"]) if tx["token_fee"] != "" else b'\0') + \
        pack(">Q", tx["timestamp"]) + \
        pack(">Q", tx["amount"]) + \
        pack(">Q", tx["fee"]) + \
        b58_to_bytes(tx["receiver"])
    )


def sign_transaction(private_key: str, **tx: dict) -> dict:
    from lunespy.utils.crypto.converters import b58_to_bytes, string_to_b58
    from lunespy.utils.crypto.converters import sign


    tx["signature"] = string_to_b58(sign(b58_to_bytes(private_key), serialize_transfer(**tx)))
    return tx


# todo async
def broadcast_transfer(mount_tx: dict, node_url: str) -> dict:
    from requests import post

    response = post(
        f'{node_url}/transactions/broadcast',
        json=mount_tx,
        headers={
            'content-type':
            'application/json'
        })

    if response.status_code in range(200, 300):
        mount_tx.update({
            'send': True,
            'response': response.json()
        })
        return mount_tx
    else:
        mount_tx.update({
            'send': False,
            'response': response.text
        })
        return mount_tx
