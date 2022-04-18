from lunespy.tx.sponsor import SponsorToken


def serialize_sponsor(tx: SponsorToken) -> bytes:
    from lunespy.crypto import b58_to_bytes
    from struct import pack

    return (
        chr(tx.type).encode() + \
        b58_to_bytes(tx.senderPublicKey) + \
        b58_to_bytes(tx.assetId) + \
        pack(">Q", tx.minSponsoredAssetFee) + \
        pack(">Q", tx.fee) + \
        pack(">Q", tx.timestamp)
    )


def sign_sponsor(private_key: str, tx: SponsorToken) -> str:
    from lunespy.crypto import fast_signature
    from lunespy.crypto import b58_to_bytes, bytes_to_b58

    tx.message = bytes_to_b58(serialize_sponsor(tx))

    return bytes_to_b58(fast_signature(
        b58_to_bytes(private_key),
        b58_to_bytes(tx.message)
    ))

