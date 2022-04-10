def validate_transfer(sender: str, receiver: str, amount: int, chain: str) -> bool:
    from lunespy.client.account.utils import validate_address
    from lunespy.utils import bcolors
    from base58 import alphabet


    if amount <= 0:
        print(bcolors.FAIL + 'Amount dont should be more than 0' + bcolors.ENDC)
        return False
    elif not all([i in alphabet.decode() for i in sender]):
        print(bcolors.FAIL + 'Sender invalid `public key`' + bcolors.ENDC)
        return False
    elif not validate_address(receiver, "1" if chain == "mainnet" else "0"):
        return False
    else:
        return True


def mount_transfer(sender: str, timestamp: str, receiver: str, asset_fee: str, asset_id: str, amount: int, chain_id: str, fee: int) -> dict:
    from lunespy.client.transactions.constants import TransferType
    from lunespy.utils.crypto.converters import b58_to_bytes, string_to_b58
    from lunespy.client.account.utils import address_generator

    return {
        "type": TransferType.to_int.value,
        "senderPublicKey": sender,
        "timestamp": timestamp,
        "recipient": receiver,
        "feeAsset": asset_fee,
        "assetId": asset_id,
        "amount": amount,
        "sender": string_to_b58(address_generator(b58_to_bytes(sender), chain_id)),
        "fee": fee
    }


def serialize_transfer(**tx: dict) -> bytes:
    from lunespy.client.transactions.constants import TransferType
    from lunespy.utils.crypto.converters import b58_to_bytes
    from struct import pack

    return (
        TransferType.to_byte.value + \
        b58_to_bytes(tx["senderPublicKey"]) + \
        (b'\1' + b58_to_bytes(tx["assetId"]) if tx["assetId"] != "" else b'\0') + \
        (b'\1' + b58_to_bytes(tx["feeAsset"]) if tx["feeAsset"] != "" else b'\0') + \
        pack(">Q", tx["timestamp"]) + \
        pack(">Q", tx["amount"]) + \
        pack(">Q", tx["fee"]) + \
        b58_to_bytes(tx["recipient"])
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
