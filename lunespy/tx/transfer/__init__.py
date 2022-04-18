from pydantic import BaseModel, Field, validator

class TransferToken(BaseModel):
    from lunespy.utils import now
    from requests import Response

    senderPublicKey: str = Field(..., description="public_key")
    assetId: str = Field("", description="token id | NFT id")
    sender: str = Field("", description="address of sender")
    recipient: str = Field(..., description="address")
    timestamp: int = Field(now(), ge=1483228800)
    message: str = Field("", exclude=True)
    fee: int = Field(1000000, ge=1000000)
    type: int = Field(4, const=True)
    amount: int = Field(..., gt=0)
    signature: str = Field("")
    feeAsset: int = Field("")

    @validator("recipient")
    def same_chain(cls, recipient, values):
        from lunespy.crypto import same_chain_address

        if not same_chain_address(recipient, values['sender']):
            raise ValueError(f"Different chain addresses ({recipient}, {values['sender']})")
        return recipient

    def sign(cls, private_key: str):
        from lunespy.tx.transfer.utils import sign_transfer
        cls.signature = sign_transfer(private_key, cls)
        return cls

    def broadcast(cls, node: str = None) -> Response:
        from lunespy.utils import broadcast_tx

        return broadcast_tx(
            cls.dict(),
            node if not node == None else "https://lunesnode-testnet.lunes.io"
        )



def transfer_token_factory(sender_public_key: str, receiver_address: str, amount: float, chain: int = 1, **kwargs: dict) -> TransferToken:
    from lunespy.crypto import b58_to_bytes, bytes_to_b58, to_address


    return TransferToken(
        sender=bytes_to_b58(to_address(b58_to_bytes(sender_public_key), chain, 1)),
        amount=int(amount * 10e7),
        senderPublicKey=sender_public_key,
        recipient=receiver_address,
        **kwargs
    )

