from requests import get 

def block_from_height(node_url: str, height: int) -> dict:
    full_url = f'https://{node_url}/blocks/at/{height}'
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

def range_block(node_url: str, start_block: int, end_block: int) -> dict:
    full_url = f'https://{node_url}/blocks/seq/{start_block}/{end_block}'
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