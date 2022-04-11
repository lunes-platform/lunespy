from pydantic import BaseModel, Field


class Wallet(BaseModel):
    nonce: int = Field(0, ge=0, le=4_294_967_296)
    seed_len: int = Field(12, multiple_of=3)
    chain: int = Field(1, le=1, ge=0)
    private_key: str = Field("")
    public_key: str = Field("")
    address: str = Field("")
    seed: str = Field("")


def wallet_factory(
    private_key: str = None,
    seed_len: int = None,
    chain: int = None,
    nonce: int = None,
    seed: str = None
    ) -> Wallet:
    """
        chain: 1 for mainnet, 0 for testnet
    """
    from lunespy.wallet.assembly import from_private_key, from_seed

    return from_private_key(private_key, chain) if private_key else from_seed(seed, nonce, chain, seed_len)

