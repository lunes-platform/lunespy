from pydantic import BaseModel, Field

class IssueToken(BaseModel):
    from lunespy.utils import now
    from requests import Response

    description: str = Field(..., description="description with size smaller than 1000 char", )
    reissuable: bool = Field(..., description="token will be reissued")
    quantity: int = Field(..., description="total supply of token")
    decimals: int = Field(..., description="token fractionability")
    senderPublicKey: str = Field(..., description="public_key")
    name: str = Field(..., description="name of token")
    timestamp: int = Field(now(), ge=1483228800)
    message: str = Field("", exclude=True)
    fee: int = Field(100000000, ge=100000000)
    type: int = Field(3, const=True)
    signature: str = Field("")

    def sign(cls, private_key: str):
        from lunespy.tx.issue.utils import sign_issue
        cls.signature = sign_issue(private_key, cls)
        return cls

    def broadcast(cls, node: str = None) -> Response:
        from lunespy.utils import broadcast_tx

        return broadcast_tx(
            cls.dict(),
            node if not node == None else "https://lunesnode-testnet.lunes.io"
        )


def issue_token_factory(sender_public_key: str, name: str, quantity: int, description: str, reissuable: bool = True, decimals: int = 8, **kwargs: dict) -> IssueToken:
    return IssueToken(
        senderPublicKey=sender_public_key,
        name=name,
        quantity=quantity,
        description=description,
        reissuable=reissuable,
        decimals=decimals,
        **kwargs
    )


def mint_NFT_factory(sender_public_key: str, name: str, description: str, **kwargs: dict) -> IssueToken:
    return IssueToken(
        senderPublicKey=sender_public_key,
        description=description,
        reissuable=False,
        decimals=0,
        quantity=1,
        name=name,
        **kwargs
    )


def tokens_airdrop():
    """
    # Create your token and send to list of address
    """
    ...

def mint_multiple_NFT():
    """
    # Create multiples NFTs
    """
    ...