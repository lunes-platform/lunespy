def validate_sign(public_key: bytes, message: bytes, signature: bytes) -> bool:
    from axolotl_curve25519 import verifySignature

    verified = verifySignature(
        public_key,
        message,
        signature
    )

    return True if verified == 0 else False


def sign(private_key: bytes, message: bytes) -> bytes:
    from axolotl_curve25519 import calculateSignature as curve
    from os import urandom

    return curve(
            urandom(64),
            private_key,
            message
        )

