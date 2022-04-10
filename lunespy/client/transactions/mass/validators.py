from lunespy.client.account import Wallet


def mount_mass_transfer(sender: Account, receivers_list: list, mass_transfer_data: dict) -> dict:
    from lunespy.client.transactions.constants import TransferType
    from lunespy.client.transactions.constants import MassType
    from lunespy.utils.crypto.converters import sign
    from lunespy.utils import lunes_to_unes
    from lunespy.utils import now
    from base58 import b58decode
    import struct

    fee: int = TransferType.fee.value + len(receivers_list) * mass_transfer_data.get('fee', MassType.fee.value)
    timestamp: int = mass_transfer_data.get('timestamp', now())
    asset_id: str = mass_transfer_data.get('asset_id', "")
    receivers_list: list = [
        {'receiver': tx['receiver'], 'amount': lunes_to_unes(tx['amount'])}
        for tx in receivers_list
    ]


    hash_transfer: bytes = lambda tx: b58decode(tx['receiver']) + struct.pack(">Q", tx['amount']) 
    receivers_list_data = b''.join(
        map(hash_transfer, receivers_list)
    )

    bytes_data: bytes = MassType.to_byte.value + \
            b'\1' + \
            b58decode(sender.public_key) + \
            (b'\1' + b58decode(asset_id) if asset_id != "" else b'\0') + \
            struct.pack(">H", len(receivers_list)) + \
            receivers_list_data + \
            struct.pack(">Q", timestamp) + \
            struct.pack(">Q", fee)

    signature: bytes = sign(sender.private_key, bytes_data)

    data = {
        "type": MassType.to_int.value,
        "senderPublicKey": sender.public_key,
        "signature": signature.decode(),
        "timestamp": timestamp,
        "fee": fee,

        "version": 1,
        "assetId": asset_id,
        "transfers": [
            {'recipient': tx['receiver'], 'amount': tx['amount']}
            for tx in receivers_list
        ],
        "proofs": [
            signature.decode()
        ]
    }

    return data


def validate_mass_transfer(sender: Account, receivers_list: list):
    from lunespy.client.account.utils import validate_address
    from lunespy.utils import bcolors

    amounts_list: list = [tx['amount'] for tx in receivers_list]

    if not sender.private_key:
        print(bcolors.FAIL + 'Sender `Account` not have a private key' + bcolors.ENDC)
        return False
    elif not all(filter(lambda address: validate_address(address['receiver'], sender.chain_id), receivers_list)):
        return False
    elif len(receivers_list) > 100:
        print(bcolors.FAIL + '`receivers_list` cannot contain more than 100 addresses' + bcolors.ENDC)
        return False
    elif not all(filter(lambda amount: amount <= 0, amounts_list)):
        print(bcolors.FAIL + 'Some address contains 0 as `amount`' + bcolors.ENDC)
        return False
    return True


def send_mass_transfer(mount_tx: dict, node_url: str) -> dict:
    from requests import post

    response = post(
        f'{node_url}/transactions/broadcast',
        json=mount_tx,
        headers={
            'content-type':
            'application/json'
        })

    if response.status_code in range(200, 300):
        mount_tx.update({
            'send': True,
            'response': response.json()
        })
        return mount_tx
    else:
        mount_tx.update({
            'send': False,
            'response': response.text
        })
        return mount_tx
