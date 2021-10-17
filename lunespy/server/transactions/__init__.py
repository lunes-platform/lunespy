from requests import get

def transaction_from_id(id: str) -> dict:
    full_url = f'https://lunesnode.lunes.io/transactions/info/{id}'
    response = get(full_url)
    return response.json()
    