from httpx import Response

def now() -> int:
    from time import time

    return int(time() * 1000)

# todo async
def broadcast_tx(node_url: str, tx: dict) -> Response:
    from httpx import post

    return post(
        f'{node_url}/transactions/broadcast',
        json=tx,
        headers={
            'content-type':
            'application/json'
        }
    )

