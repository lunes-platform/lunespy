## Getting Started

You can install LunesPy using:

    pip install lunespy

## Documentation

The library is driven-transactions on the *lunesnode* architecture:

**classes**
- Account
- TransferAssets
- IssueAsset
- Leasing
- Comming Soon...

## Generate a Wallet

A `Wallet` is as `email account` thats have:
- seed
- nonce
- private key
- public key
- address

The wallet can be generated for `testnet` or `mainnet`. **This will only change the address**

You can generate a wallet passing your `seed`, `private_key`, `public_key`, `address` as **parameters** or none of that.

Changing the `nonce` is possible generate `4,294,967,295` different wallets with only a `seed`.

**Exemple code**
```python
from lunespy.client.wallet import Account

# Generating Wallet
new_wallet = Account()
print(new_wallet)

# Saving your wallet
new_wallet.to_json(path='./')
```

```py
[output]:

seed
 └── "roast mother supply match result breeze canoe immune spike vague poverty apology found ivory reward"
nonce
 └── 0
private key
 └── "EUMUHS8StgpYPkNFVLC1yucioN1WAEXLA16XbaTc4i7g"
public key
 └── "8oo2AThLJtRwhBrwsZgdHtZfPpAp2bKhcLT11FbvL6xr"
address
 └── "37p2LHMx3WP3n2thAyBeP3wzidiEmKxjxU9"

"Your wallet has been saved in `./wallet.json`"
```


## Send Lunes

Only for send `Lunes` asset **you dont must be pass `asset_id` parameter** in `TranferAssets`.

The transfer costs **`0.001Lunes`**


**Exemple code**
```python
from lunespy.client.transactions.transfer_asset import TransferAsset
from lunespy.client.wallet import Account

# Generate the wallets
seed = "My_seed"
my_wallet = Account(seed=seed, chain="testnet", nonce=0)
random_wallet = Account(chain='testnet')

# Mount a transfer asset Transaction
tx = TransferAsset(my_wallet, random_wallet, amount=100)

# Returns `True` if the data passed is valid
print(tx.ready)

# Returns the transaction mounted before sending
print(tx.transaction)

# Send a transfer transaction
print(tx.send)

# Shows all sent transfers
print(tx.history)
```
**If failed**
```json
[
  {
    "ready": true,
    "senderPublicKey": "4SpyrKC8KFq2AF2RjgS6o373vTFrAAwrFmMfYL8PfezE",
    "signature": "4jD1B37yewcwedSZ6gt8LeVPY8f2i4tn8VjrnhNukCkpTrvm1e5YtrH7Byzj7rYTbB9dMzKzdL5P1E7xR7N89zp9",
    "timestamp": 1631473467403,
    "recipient": "37ani1re8pMVYRkHo1xDPtj8kBYyDu3DGkP",
    "feeAsset": "",
    "assetId": "",
    "amount": 100,
    "type": 4,
    "fee": 100000,
    "send": false,
    "reason": {
      "error": 112,
      "message": "State check failed. Reason: Attempt to transfer unavailable funds: Transaction application leads to negative lunes balance to (at least) temporary negative state, current balance equals 0, spends equals -100100, result is -100100",
      "tx": {
        "type": 4,
        "id": "EzQVTZGavd9jmWprnADWMK3dya8ZeF1dAF4JNYmAkkH1",
        "sender": "37QqvghNGWrUWSjALayGjCnT1nC28wXV6pL",
        "senderPublicKey": "4SpyrKC8KFq2AF2RjgS6o373vTFrAAwrFmMfYL8PfezE",
        "fee": 100000,
        "timestamp": 1631473467403,
        "signature": "4jD1B37yewcwedSZ6gt8LeVPY8f2i4tn8VjrnhNukCkpTrvm1e5YtrH7Byzj7rYTbB9dMzKzdL5P1E7xR7N89zp9",
        "recipient": "37ani1re8pMVYRkHo1xDPtj8kBYyDu3DGkP",
        "assetId": null,
        "amount": 100,
        "feeAsset": null
      }
    }
  }
]
```
**If successful**
```json
[
  {
    "ready": true,
    "senderPublicKey": "4SpyrKC8KFq2AF2RjgS6o373vTFrAAwrFmMfYL8PfezE",
    "signature": "4jD1B37yewcwedSZ6gt8LeVPY8f2i4tn8VjrnhNukCkpTrvm1e5YtrH7Byzj7rYTbB9dMzKzdL5P1E7xR7N89zp9",
    "timestamp": 1631473467403,
    "recipient": "37ani1re8pMVYRkHo1xDPtj8kBYyDu3DGkP",
    "feeAsset": "",
    "assetId": "",
    "amount": 100,
    "type": 4,
    "fee": 100000,
    "send": true,
    "reason": {
      "type": 4,
      "id": "DFh451K5ot7J8sjobVsrMcAQiFnRESXG6C19UnKsS5Mi",
      "sender": "37bpECMv85nUr14YEfkyyyWKN2gYgrCfDhX",
      "senderPublicKey": "FYvp88jP2xC21JCQfeSxUkg6qmLSGs5x8TBr5V3pT2NH",
      "fee": 100000,
      "timestamp": 1631473695599,
      "signature": "2VwHiMtN2CUqJuMiaGqhsM1Qorhz7jMbjGb5wxN9Hb7WnLZXAwPPTEYjht8Ey8FjDt8739EFnuSvwMiwioqJ3XXd",
      "recipient": "37hqrPGmzzT6xk5GFXbc9u5yYnRmBWSJuTY",
      "assetId": null,
      "amount": 100,
      "feeAsset": null
    }
  }
]
```


## Issue your Token

**Brief description of what Tokens, Assets and NFT's are**

- **Token** are representations of something real or not, such as identity, value, product, etc...
- **NFT** are a type of token, non-fractional, that represents the intellectual property of something, such as music, video, photo, etc.
- **Asset** are tokens that represent some value, which can be fractionable.

Your parameter `name` must be more than 4 and less than 16 characters.

You can choose how many tokens to create by changing the `quantity` parameter.

The `decimal` parameter can be useful to fractionate your asset.

Putting `True` in the `reissuable` parameter will allow you to issue more of the same asset in the future.

The issue Token costs **`1Lunes`**

**Exemple code**
```python
from lunespy.client.wallet import Account
from lunespy.client.transactions.issue_asset import IssueAsset


# Generate the wallet
seed = 'Your Seed'
genesis = Account(seed=seed, chain='testnet')


# Information of issue your new token
token_info = {
  'name': "MyTokenName",
  'description': "My new experimental token",
  'quantity': 799,
  'decimals': 3,
  'reissueable': False
}


# Mount a issue asset Transaction
issue = IssueAsset(genesis, **token_info)


# Returns `True` if the data passed is valid
print(tx.ready)

# Returns the transaction mounted before sending
print(tx.transaction)

# Send a transfer transaction
print(tx.send)

# Shows all sent transfers
print(tx.history)
```

## Send your Tokens

By passing an `asset_id` parameter it is possible to send any asset that has already been `issued` in lunes-blockchain


The transfer costs **`0.001Lunes`**

```python
from lunespy.client.transactions.transfer_asset import TransferAsset
from lunespy.client.wallet import Account

# Generate the wallet
seed = "My_seed"
my_wallet = Account(seed=seed, chain="testnet", nonce=0)
random_wallet = Account(chain='testnet')

# Get Asset or Token ID
token = "9ax6usn3TmwdTRoTnn8zr5Kku9qykstYxRkUb4Z1Z2oY"

# Mount a transfer asset Transaction
tx = TransferAsset(my_wallet, random_wallet, amount=100, asset_id=token)

# Send a transaction
tx.send
print(tx.history)
```
**Successful**
```json
[
  {
    "ready": true, 
    "senderPublicKey": "FYvp88jP2xC21JCQfeSxUkg6qmLSGs5x8TBr5V3pT2NH",
    "signature": "4DbDKGpykZ6we8VckTNGCeVFhLgiFaaDobcbjXi5vy7wupbxLUMtnkhwRc2HmdGctFTm8URZ8bzVEwxPgbofCzWT",
    "timestamp": 1631475869750,
    "recipient": "37cefY8nWHhBTkFLSiSdNyDSg6n9e7G5DF2",
    "feeAsset": "",
    "assetId": "9ax6usn3TmwdTRoTnn8zr5Kku9qykstYxRkUb4Z1Z2oY",
    "amount": 100,
    "type": 4,
    "fee": 100000,
    "send": true,
    "reason": {
      "type": 4,
      "id": "B31BCDgKGr1bisKChb3LF1mL3Wfb1Yaqkvwiv9MargzR",
      "sender": "37bpECMv85nUr14YEfkyyyWKN2gYgrCfDhX",
      "senderPublicKey": "FYvp88jP2xC21JCQfeSxUkg6qmLSGs5x8TBr5V3pT2NH",
      "fee": 100000,
      "timestamp": 1631475869750,
      "signature": "4DbDKGpykZ6we8VckTNGCeVFhLgiFaaDobcbjXi5vy7wupbxLUMtnkhwRc2HmdGctFTm8URZ8bzVEwxPgbofCzWT",
      "recipient": "37cefY8nWHhBTkFLSiSdNyDSg6n9e7G5DF2",
      "assetId": "9ax6usn3TmwdTRoTnn8zr5Kku9qykstYxRkUb4Z1Z2oY", 
      "amount": 100,
      "feeAsset": null
    }
  }
]
```

## Reissue your Token or New Asset

```python
Comming Soon...
```
## Burn your Token or New Asset

```python
Comming Soon...
```

## Send your Lease

```python
Comming Soon...
```

## Cancel your Lease

```python
Comming Soon...
```

## Create new Payment

```python
Comming Soon...
```

## Create Alias for your Address

```python
Comming Soon...
```

## Send MassTransfer of Lunes

```python
Comming Soon...
```
## Send MassTransfer of any Assets

```python
Comming Soon...
```

## Registry your data in Blockchain

```python
Comming Soon...
```

## Set Script

```python
Comming Soon...
```

## Transfer Script

```python
Comming Soon...
```

## Generate your Genesis Trasaction

```python
Comming Soon...
```