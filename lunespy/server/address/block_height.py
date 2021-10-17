from requests import get 

def heigth(h: str) -> dict:
    full_url = f'https://lunesnode.lunes.io/blocks/at/{h}'
    response = get(full_url)
    return response.json()
    