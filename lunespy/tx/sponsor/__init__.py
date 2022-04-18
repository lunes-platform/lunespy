from pydantic import BaseModel, Field

class SponsorToken(BaseModel):
    from lunespy.utils import now
    from requests import Response

    minSponsoredAssetFee: int = Field(..., description="minimal fee")
    senderPublicKey: str = Field(..., description="public_key")
    assetId: str = Field(..., description="token id | NFT id")
    timestamp: int = Field(now(), ge=1483228800)
    message: str = Field("", exclude=True)
    fee: int = Field(1000000, ge=1000000)
    type: int = Field(14, const=True)
    version: int = Field(1, const=True)
    proofs: str = Field([""])

    def sign(cls, private_key: str):
        from lunespy.tx.sponsor.utils import sign_sponsor
        cls.proofs[0] = sign_sponsor(private_key, cls)
        return cls

    def broadcast(cls, node: str = None) -> Response:
        from lunespy.utils import broadcast_tx

        return broadcast_tx(
            cls.dict(),
            node if not node == None else "https://lunesnode-testnet.lunes.io"
        )


def sponsor_token_factory(sender_public_key: str, asset_id: str, minimal_fee: int, **kwargs: dict) -> SponsorToken:

    return SponsorToken(
        senderPublicKey=sender_public_key,
        minSponsoredAssetFee=minimal_fee,
        assetId=asset_id,
        **kwargs
    )
