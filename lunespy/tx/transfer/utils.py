from lunespy.tx.transfer import TransferToken
from requests import Response

from lunespy.crypto import bytes_to_b58


def serialize_transfer(tx: TransferToken) -> bytes:
    from lunespy.crypto import b58_to_bytes
    from struct import pack

    return (
        chr(tx.type).encode() + \
        b58_to_bytes(tx.senderPublicKey) + \
        (b'\1' + b58_to_bytes(tx.assetId) if tx.assetId != "" else b'\0') + \
        (b'\1' + b58_to_bytes(tx.feeAsset) if tx.feeAsset != "" else b'\0') + \
        pack(">Q", tx.timestamp) + \
        pack(">Q", tx.amount) + \
        pack(">Q", tx.fee) + \
        b58_to_bytes(tx.recipient)
    )


def sign_transfer(private_key: str, tx: TransferToken) -> dict:
    from lunespy.crypto import fast_signature
    from lunespy.crypto import b58_to_bytes, bytes_to_b58

    tx.message = bytes_to_b58(serialize_transfer(tx))

    return bytes_to_b58(fast_signature(
        b58_to_bytes(private_key),
        b58_to_bytes(tx.message)
    ))
