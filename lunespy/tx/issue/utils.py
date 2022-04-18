from lunespy.tx.issue import IssueToken


def serialize_issue(tx: IssueToken) -> bytes:
    from lunespy.crypto import b58_to_bytes
    from struct import pack

    return (
        chr(tx.type).encode() + \
        b58_to_bytes(tx.senderPublicKey) + \
        pack(">H", len(tx.name)) + \
        tx.name.encode("latin-1") + \
        pack(">H", len(tx.description)) + \
        tx.description.encode("latin-1") + \
        pack(">Q", tx.quantity) + \
        pack(">B", tx.decimals) + \
        (b'\1' if tx.reissuable else b'\0') + \
        pack(">Q", tx.fee) + \
        pack(">Q", tx.timestamp)
    )


def sign_issue(private_key: str, tx: IssueToken) -> str:
    from lunespy.crypto import fast_signature
    from lunespy.crypto import b58_to_bytes, bytes_to_b58

    tx.message = bytes_to_b58(serialize_issue(tx))

    return bytes_to_b58(fast_signature(
        b58_to_bytes(private_key),
        b58_to_bytes(tx.message)
    ))

