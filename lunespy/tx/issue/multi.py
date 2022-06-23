from lunespy.tx.issue import IssueToken, issue_token_factory
from pydantic import BaseModel, Field
from typing import List


class MultiTokens(BaseModel):
    from httpx import Response

    tokens: List[IssueToken] = Field(..., description="list of issue tokens")

    @property
    def length(cls) -> int:
        return len(cls.tokens)

    def sign(cls, private_key: str):
        cls.tokens = list(
            map(lambda tx: tx.sign(private_key), cls.tokens)
        )

    def broadcast(cls, node: str = None) -> Response:
        from lunespy.utils import broadcast_tx

        broadcast = lambda tx: broadcast_tx(
            node if not node == None else "https://lunesnode-testnet.lunes.io",
            tx.dict()
        )

        return list(map(broadcast, cls.tokens))


def issue_multiples_tokens(sender_public_key: str, tokens_list: List[dict]) -> MultiTokens:
    return MultiTokens(tokens=[
        issue_token_factory(
            sender_public_key,
            token["name"],
            token["quantity"],
            token["description"],
            token["reissuable"],
            token["decimals"]
        )
        for token in tokens_list
    ])


def mint_multiples_NFT(sender_public_key: str, tokens_list: List[dict]) -> MultiTokens:
    def toNFT(token: dict) -> dict:
        token["quantity"], token["decimals"] = 1, 0
        return token

    return issue_multiples_tokens(
        sender_public_key,
        tokens_list=[
            toNFT(token)
            for token in tokens_list
        ]
    )
