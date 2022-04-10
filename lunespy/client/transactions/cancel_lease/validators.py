from lunespy.client.account import Wallet


def mount_cancel(sender: Account, cancel_data: dict) -> dict:
    from lunespy.client.transactions.constants import CancelLeaseType
    from lunespy.utils.crypto.converters import sign
    from lunespy.utils import now
    from base58 import b58decode
    import struct

    lease_tx_id: str = cancel_data['lease_tx_id']
    timestamp: int = cancel_data.get('timestamp', now())
    fee: int = cancel_data.get('fee', CancelLeaseType.fee.value)

    bytes_data: bytes = CancelLeaseType.to_byte.value + \
        b58decode(sender.public_key) + \
        struct.pack(">Q", fee) + \
        struct.pack(">Q", timestamp) + \
        b58decode(lease_tx_id)

    signature: bytes = sign(sender.private_key, bytes_data)
    mount_tx: dict = {
        "type":CancelLeaseType.to_int.value,
        "senderPublicKey": sender.public_key,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "fee": fee,

        "leaseId": lease_tx_id
    }
    return mount_tx


def validate_cancel(sender: Account, cancel_data: dict) -> bool:
    from lunespy.utils import bcolors

    amount: int = cancel_data.get('amount', -1)
    lease_tx_id: str = cancel_data.get('lease_tx_id', '')

    if not sender.private_key:
        print(bcolors.FAIL + 'Staker `Account` not have a private key' + bcolors.ENDC)
        return False
    elif lease_tx_id == '':
        print(bcolors.FAIL + 'Leasing must be `lease_tx_id`' + bcolors.ENDC)
        return False
    return True


# todo async
def send_cancel(mount_tx: dict, node_url: str) -> dict:
    from requests import post

    response = post(
        f'{node_url}/transactions/broadcast',
        json=mount_tx,
        headers={
            'content-type':
            'application/json'
        })

    if response.status_code in range(200, 300):
        mount_tx['send'] = True
        mount_tx['response'] = response.json()
        return mount_tx
    else:
        mount_tx['send'] = False
        mount_tx['response'] = response.text
        return mount_tx