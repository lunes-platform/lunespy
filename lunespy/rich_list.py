from requests import get

def get_rich_list(number: int, node_ip: str, node_api_key: str) -> dict:
    url = f"http://{node_ip}/debug/state"
    wallets = get(
        url,
        headers={
            "X-API-key": node_api_key
            }
        ).json()
    address = sorted(wallets, key=wallets.get, reverse=True)

    rich_list = {}
    for i in range(number):
        key = address[i]
        value = wallets[key]
        rich_list[key] = value / 10e7
    return rich_list
