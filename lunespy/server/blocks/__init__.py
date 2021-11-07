from requests import get 

def block_from_height(height: str) -> dict:
    full_url = f'https://lunesnode.lunes.io/blocks/at/{height}'
    response = get(full_url)
    return response.json()
    