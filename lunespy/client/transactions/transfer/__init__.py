from lunespy.wallet.crypto import b58_to_bytes, bytes_to_b58, to_address
from lunespy.utils import lunes_to_unes, now
from pydantic import BaseModel, Field


class TransferToken(BaseModel):
    chain: int = Field(1, ge=0, le=1, description="1 for mainnet, 0 for testnet")
    fee: int = Field(lunes_to_unes(0.01), gt=lunes_to_unes(0.01))
    sender_public_key: str = Field(..., description="public_key")
    token_id: str = Field("", description="token id | NFT id")
    sender: int = Field("", description="address of sender")
    receiver: str = Field(..., description="address")
    timestamp: int = Field(default_factory=now)
    amount: int = Field(..., gt=0)
    token_fee: int = Field(None)


    def transactions(cls: BaseModel):
        tx = cls.dict()
        tx["sender"] = bytes_to_b58(to_address(b58_to_bytes(cls.sender_public_key), cls.chain, 1))
        tx["senderPublicKey"] = tx.pop("sender_public_key")
        tx["assetId"] = tx.pop("token_id")
        tx["feeAsset"] = tx.pop("token_fee")
        return tx


    def sign(cls, v: str):
        tx = cls.transactions()
        tx["signature"] = v
        return tx

    def broadcast(cls):
        return 

