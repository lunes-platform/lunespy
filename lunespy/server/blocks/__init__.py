from requests import get 

def block_from_height(node: str, height: str) -> dict:
    full_url = f'https://{node}/blocks/at/{height}'
    response = get(full_url)
    
    if response.ok:
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }

def range_block(node: str, start_block: str, end_block: str) -> dict:
    full_url = f'https://{node}/blocks/seq/{start_block}/{end_block}'
    response = get(full_url)
    
    if response.ok:
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'status': 'error',
            'response': response.text
        }