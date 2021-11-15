from requests import get


def transaction_from_id(id: str) -> dict:
    full_url = f'https://lunesnode.lunes.io/transactions/info/{id}'
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


def unconfirmed_transaction(node_url: str) -> dict:
    full_url = f'https://{node_url}/transactions/unconfirmed'
    response = get(full_url)

    if response.ok:
        return {
            'status': 'ok',
            'response': response.json()
        }
    else:
        return {
            'stauts': 'error',
            'response': response.text
        }


def transactions_from_address(node_url: str, address: str, limit_transactions: int) -> dict:
    full_url = f'https://{node_url}/transactions/address/{address}/limit/{limit_transactions}'
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
