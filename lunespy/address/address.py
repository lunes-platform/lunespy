import LunesPy as lunespy
import axolotl_curve25519 as curve
import os
import LunesPy.crypto as crypto
import time
import struct
import json
import base58
import base64
import logging
import requests

class Address(object):
    def __init__(self, address='', publicKey='', privateKey='', seed='', alias='', nonce=0):
        if nonce<0 or nonce>4294967295:
            raise ValueError('Nonce must be between 0 and 4294967295')
        if seed:
            self._generate(seed=seed, nonce=nonce)
        elif privateKey:
            self._generate(privateKey=privateKey)
        elif publicKey:
            self._generate(publicKey=publicKey)
        elif address:
            if not lunespy.validateAddress(address):
                raise ValueError("Invalid address")
            else:
                self.address = address
                self.publicKey = publicKey
                self.privateKey = privateKey
                self.seed = seed
                self.nonce = nonce
        elif alias and not lunespy.OFFLINE:
            self.address = lunespy.wrapper('/addresses/alias/by-alias/%s' % alias).get("address", "")
            self.publicKey = ''
            self.privateKey = ''
            self.seed = ''
            self.nonce = 0
        else:
            self._generate(nonce=nonce)
        if not lunespy.OFFLINE:
            self.aliases = self.aliases()

    def __str__(self):
        if self.address:
            ab = []
            try:
                assets_balances = lunespy.wrapper('/assets/balance/%s' % self.address)['balances']
                for a in assets_balances:
                    if a['balance'] > 0:
                        ab.append("  %s (%s) = %d" % (a['assetId'], a['issueTransaction']['name'].encode('ascii', 'ignore'), a['balance']))
            except:
                pass
            return 'address = %s\npublicKey = %s\nprivateKey = %s\nseed = %s\nnonce = %d\nbalances:\n  Lunes = %d%s' % (self.address, self.publicKey, self.privateKey, self.seed, self.nonce, self.balance(), '\n'+'\n'.join(ab) if ab else '')

    __repr__ = __str__

    def balance(self, assetId='', confirmations=0):
        try:
            if assetId:
                return lunespy.wrapper('/assets/balance/%s/%s' % (self.address, assetId))['balance']
            else:
                return lunespy.wrapper('/addresses/balance/%s%s' % (self.address, '' if confirmations==0 else '/%d' % confirmations))['balance']
        except:
            return 0

    def assets(self):
        req = lunespy.wrapper('/assets/balance/%s' % self.address)['balances']
        return [r['assetId'] for r in req]

    def aliases(self):
        a = lunespy.wrapper('/addresses/alias/by-address/%s' % self.address)
        if type(a)==list:
            for i in range(len(a)):
                a[i] = a[i][8:]
        return a

    def _generate(self, publicKey='', privateKey='', seed='', nonce=0):
        self.seed = seed
        self.nonce = nonce
        if not publicKey and not privateKey and not seed:
            wordCount = 2048
            words = []
            for i in range(5):
                r = crypto.bytes2str(os.urandom(4))
                x = (ord(r[3])) + (ord(r[2]) << 8) + (ord(r[1]) << 16) + (ord(r[0]) << 24)
                w1 = x % wordCount
                w2 = ((int(x / wordCount) >> 0) + w1) % wordCount
                w3 = ((int((int(x / wordCount) >> 0) / wordCount) >> 0) + w2) % wordCount
                words.append(wordList[w1])
                words.append(wordList[w2])
                words.append(wordList[w3])
            self.seed = ' '.join(words)
        if publicKey:
            pubKey = base58.b58decode(publicKey)
            privKey = ""
        else:
            seedHash = crypto.hashChain(struct.pack(">L", nonce) + crypto.str2bytes(self.seed))
            accountSeedHash = crypto.sha256(seedHash)
            if not privateKey:
                privKey = curve.generatePrivateKey(accountSeedHash)
            else:
                privKey = base58.b58decode(privateKey)
            pubKey = curve.generatePublicKey(privKey)
        unhashedAddress = chr(1) + str(lunespy.CHAIN_ID) + crypto.hashChain(pubKey)[0:20]
        addressHash = crypto.hashChain(crypto.str2bytes(unhashedAddress))[0:4]
        self.address = base58.b58encode(crypto.str2bytes(unhashedAddress + addressHash))
        self.publicKey = base58.b58encode(pubKey)
        if privKey != "":
            self.privateKey = base58.b58encode(privKey)

    def issueAsset(self, name, description, quantity, decimals=0, reissuable=False, txFee=lunespy.DEFAULT_ASSET_FEE):
        if not self.privateKey:
            logging.error('Private key required')
        elif len(name) < 4 or len(name) > 16:
            logging.error('Asset name must be between 4 and 16 characters long')
        else:
            timestamp = int(time.time() * 1000)
            sData = b'\3' + \
                    base58.b58decode(self.publicKey) + \
                    struct.pack(">H", len(name)) + \
                    crypto.str2bytes(name) + \
                    struct.pack(">H", len(description)) + \
                    crypto.str2bytes(description) + \
                    struct.pack(">Q", quantity) + \
                    struct.pack(">B", decimals) + \
                    (b'\1' if reissuable else b'\0') + \
                    struct.pack(">Q", txFee) + \
                    struct.pack(">Q", timestamp)
            signature=crypto.sign(self.privateKey, sData)
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "name": name,
                "quantity": quantity,
                "timestamp": timestamp,
                "description": description,
                "decimals": decimals,
                "reissuable": reissuable,
                "fee": txFee,
                "signature": signature
            })
            req = lunespy.wrapper('/assets/broadcast/issue', data)
            if lunespy.OFFLINE:
                return req
            else:
                return lunespy.Asset(req['assetId'])

    def reissueAsset(self, Asset, quantity, reissuable=False, txFee=lunespy.DEFAULT_TX_FEE):
        timestamp = int(time.time() * 1000)
        sData = b'\5' + \
                base58.b58decode(self.publicKey) + \
                base58.b58decode(Asset.assetId) + \
                struct.pack(">Q", quantity) + \
                (b'\1' if reissuable else b'\0') + \
                struct.pack(">Q",txFee) + \
                struct.pack(">Q", timestamp)
        signature = crypto.sign(self.privateKey, sData)
        data = json.dumps({
            "senderPublicKey": self.publicKey,
            "assetId": Asset.assetId,
            "quantity": quantity,
            "timestamp": timestamp,
            "reissuable": reissuable,
            "fee": txFee,
            "signature": signature
        })
        req = lunespy.wrapper('/assets/broadcast/reissue', data)
        if lunespy.OFFLINE:
            return req
        else:
            return req.get('id', 'ERROR')

    def burnAsset(self, Asset, quantity, txFee=lunespy.DEFAULT_TX_FEE):
        timestamp = int(time.time() * 1000)

        sData = '\6' + \
                crypto.bytes2str(base58.b58decode(self.publicKey)) + \
                crypto.bytes2str(base58.b58decode(Asset.assetId)) + \
                crypto.bytes2str(struct.pack(">Q", quantity)) + \
                crypto.bytes2str(struct.pack(">Q", txFee)) + \
                crypto.bytes2str(struct.pack(">Q", timestamp))
        signature = crypto.sign(self.privateKey, crypto.str2bytes(sData))
        data = json.dumps({
            "senderPublicKey": self.publicKey,
            "assetId": Asset.assetId,
            "quantity": quantity,
            "timestamp": timestamp,
            "fee": txFee,
            "signature": signature
        })
        req = lunespy.wrapper('/assets/broadcast/burn', data)
        if lunespy.OFFLINE:
            return req
        else:
            return req.get('id', 'ERROR')

    def sendLunes(self, recipient, amount, attachment='', txFee=lunespy.DEFAULT_TX_FEE, timestamp=0):
        if not self.privateKey:
            logging.error('Private key required')
        elif amount <= 0:
            logging.error('Amount must be > 0')
        elif not lunespy.OFFLINE and self.balance() < amount + txFee:
            logging.error('Insufficient Lunes balance')
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\4' + \
                    base58.b58decode(self.publicKey) + \
                    b'\0\0' + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", amount) + \
                    struct.pack(">Q", txFee) + \
                    base58.b58decode(recipient.address) + \
                    struct.pack(">H", len(attachment)) + \
                    crypto.str2bytes(attachment)
            signature = crypto.sign(self.privateKey, sData)
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "recipient": recipient.address,
                "amount": amount,
                "fee": txFee,
                "timestamp": timestamp,
                "attachment": base58.b58encode(crypto.str2bytes(attachment)),
                "signature": signature
            })

            return lunespy.wrapper('/assets/broadcast/transfer', data)

    def massTransferLunes(self, transfers, attachment='', timestamp=0):
        txFee = 100000 + len(transfers) * 50000
        totalAmount = 0

        for i in range(0, len(transfers)):
            totalAmount += transfers[i]['amount']

        if not self.privateKey:
            logging.error('Private key required')
        elif len(transfers) > 100:
            logging.error('Too many recipients')
        elif not lunespy.OFFLINE and self.balance() < totalAmount + txFee:
            logging.error('Insufficient Lunes balance')
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            transfersData = b''
            for i in range(0, len(transfers)):
                transfersData += base58.b58decode(transfers[i]['recipient']) + struct.pack(">Q", transfers[i]['amount'])
            sData = b'\x0b' + \
                    b'\1' + \
                    base58.b58decode(self.publicKey) + \
                    b'\0' + \
                    struct.pack(">H", len(transfers)) + \
                    transfersData + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", txFee) + \
                    struct.pack(">H", len(attachment)) + \
                    crypto.str2bytes(attachment)

            signature = crypto.sign(self.privateKey, sData)

            data = json.dumps({
                "type": 11,
                "version": 1,
                "assetId": "",
                "senderPublicKey": self.publicKey,
                "fee": txFee,
                "timestamp": timestamp,
                "transfers": transfers,
                "attachment": base58.b58encode(crypto.str2bytes(attachment)),
                "signature": signature,
                "proofs": [
                    signature
                ]
            })

            return lunespy.wrapper('/transactions/broadcast', data)

    def sendAsset(self, recipient, asset, amount, attachment='', feeAsset='', txFee=lunespy.DEFAULT_TX_FEE, timestamp=0):
        if not self.privateKey:
            logging.error('Private key required')
        elif not lunespy.OFFLINE and asset and not asset.status():
            logging.error('Asset not issued')
        elif amount <= 0:
            logging.error('Amount must be > 0')
        elif not lunespy.OFFLINE and asset and self.balance(asset.assetId) < amount:
            logging.error('Insufficient asset balance')
        elif not lunespy.OFFLINE and not asset and self.balance() < amount:
            logging.error('Insufficient Lunes balance')
        elif not lunespy.OFFLINE and not feeAsset and self.balance() < txFee:
            logging.error('Insufficient Lunes balance')
        elif not lunespy.OFFLINE and feeAsset and self.balance(feeAsset.assetId) < txFee:
            logging.error('Insufficient asset balance')
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\4' + \
                    base58.b58decode(self.publicKey) + \
                    (b'\1' + base58.b58decode(asset.assetId) if asset else b'\0') + \
                    (b'\1' + base58.b58decode(feeAsset.assetId) if feeAsset else b'\0') + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", amount) + \
                    struct.pack(">Q", txFee) + \
                    base58.b58decode(recipient.address) + \
                    struct.pack(">H", len(attachment)) + \
                    crypto.str2bytes(attachment)
            signature = crypto.sign(self.privateKey, sData)
            data = json.dumps({
                "assetId": (asset.assetId if asset else ""),
                "feeAssetId": (feeAsset.assetId if feeAsset else ""),
                "senderPublicKey": self.publicKey,
                "recipient": recipient.address,
                "amount": amount,
                "fee": txFee,
                "timestamp": timestamp,
                "attachment": base58.b58encode(crypto.str2bytes(attachment)),
                "signature": signature
            })

            return lunespy.wrapper('/assets/broadcast/transfer', data)

    def massTransferAssets(self, transfers, asset, attachment='', timestamp=0):
        txFee = 100000 + len(transfers) * 50000
        totalAmount = 0

        if not self.privateKey:
            logging.error('Private key required')
        elif len(transfers) > 100:
            logging.error('Too many recipients')
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            transfersData = b''
            for i in range(0, len(transfers)):
                transfersData += base58.b58decode(transfers[i]['recipient']) + struct.pack(">Q", transfers[i]['amount'])
            sData = b'\x0b' + \
                    b'\1' + \
                    base58.b58decode(self.publicKey) + \
                    b'\1' + \
                    base58.b58decode(asset.assetId) + \
                    struct.pack(">H", len(transfers)) + \
                    transfersData + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", txFee) + \
                    struct.pack(">H", len(attachment)) + \
                    crypto.str2bytes(attachment)

            signature = crypto.sign(self.privateKey, sData)

            data = json.dumps({
                "type": 11,
                "version": 1,
                "assetId": asset.assetId,
                "senderPublicKey": self.publicKey,
                "fee": txFee,
                "timestamp": timestamp,
                "transfers": transfers,
                "attachment": base58.b58encode(crypto.str2bytes(attachment)),
                "signature": signature,
                "proofs": [
                    signature
                ]
            })

            return lunespy.wrapper('/transactions/broadcast', data)

    def dataTransaction(self, data, timestamp=0):
        if not self.privateKey:
            logging.error('Private key required')
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            dataObject = {
                "type": 12,
                "version": 1,
                "senderPublicKey": self.publicKey,
                "data": data,
                "fee": 0,
                "timestamp": timestamp,
                "proofs": ['']
            }
            dataBinary = b''
            for i in range(0, len(data)):
                d = data[i]
                keyBytes = crypto.str2bytes(d['key'])
                dataBinary += struct.pack(">H", len(keyBytes))
                dataBinary += keyBytes
                if d['type'] == 'binary':
                    dataBinary += b'\2'
                    valueAsBytes = d['value']
                    dataBinary += struct.pack(">H", len(valueAsBytes))
                    dataBinary += crypto.str2bytes(valueAsBytes)
                elif d['type'] == 'boolean':
                    if d['value']:
                        dataBinary += b'\1\1'
                    else:
                        dataBinary += b'\1\0'
                elif d['type'] == 'integer':
                    dataBinary += b'\0'
                    dataBinary += struct.pack(">Q", d['value'])
                elif d['type'] == 'string':
                    dataBinary += b'\3'
                    dataBinary += struct.pack(">H", len(d['value']))
                    dataBinary += crypto.str2bytes(d['value'])
            # check: https://stackoverflow.com/questions/2356501/how-do-you-round-up-a-number-in-python
            txFee = (int(( (len(crypto.str2bytes(json.dumps(data))) + 2 + 64 )) / 1000.0) + 1 ) * 100000
            dataObject['fee'] = txFee
            sData = b'\x0c' + \
                    b'\1' + \
                    base58.b58decode(self.publicKey) + \
                    struct.pack(">H", len(data)) + \
                    dataBinary + \
                    struct.pack(">Q", timestamp) + \
                    struct.pack(">Q", txFee)

            dataObject['proofs'] = [ crypto.sign(self.privateKey, sData) ]

            for entry in dataObject['data']:
                if entry['type'] == 'binary':
                    base64Encoded =  base64.b64encode(crypto.str2bytes(entry['value']))
                    entry['value'] = 'base64:' + crypto.bytes2str(base64Encoded)
            dataObjectJSON = json.dumps(dataObject)
            return lunespy.wrapper('/transactions/broadcast', dataObjectJSON)

    def _postOrder(self, amountAsset, priceAsset, orderType, amount, price, maxLifetime=30*86400, matcherFee=lunespy.DEFAULT_MATCHER_FEE, timestamp=0):
        if timestamp == 0:
            timestamp = int(time.time() * 1000)
        expiration = timestamp + maxLifetime * 1000
        asset1 = b'\0' if amountAsset.assetId=='' else b'\1' + base58.b58decode(amountAsset.assetId)
        asset2 = b'\0' if priceAsset.assetId=='' else b'\1' + base58.b58decode(priceAsset.assetId)
        sData = base58.b58decode(self.publicKey) + \
                base58.b58decode(lunespy.MATCHER_PUBLICKEY) + \
                asset1 + \
                asset2 + \
                orderType + \
                struct.pack(">Q", price) + \
                struct.pack(">Q", amount) + \
                struct.pack(">Q", timestamp) + \
                struct.pack(">Q", expiration) + \
                struct.pack(">Q", matcherFee)
        signature = crypto.sign(self.privateKey, sData)
        otype = "buy" if orderType==b'\0' else "sell"
        data = json.dumps({
            "senderPublicKey": self.publicKey,
            "matcherPublicKey": lunespy.MATCHER_PUBLICKEY,
            "assetPair": {
                "amountAsset": amountAsset.assetId,
                "priceAsset": priceAsset.assetId,
                },
            "orderType": otype,
            "price": price,
            "amount": amount,
            "timestamp": timestamp,
            "expiration": expiration,
            "matcherFee": matcherFee,
            "signature": signature
        })
        req = lunespy.wrapper('/matcher/orderbook', data, host=lunespy.MATCHER)
        id = -1
        if 'status' in req:
            if req['status'] == 'OrderRejected':
                logging.error('Order Rejected - %s' % req['message'])
            elif req['status'] == 'OrderAccepted':
                id = req['message']['id']
                logging.info('Order Accepted - ID: %s' % id)
        elif not lunespy.OFFLINE:
            logging.error(req)
        else:
            return req
        return id

    def cancelOrder(self, assetPair, order):
        if not lunespy.OFFLINE:
            if order.status() == 'Filled':
                logging.error("Order already filled")
            elif not order.status():
                logging.error("Order not found")
        sData = base58.b58decode(self.publicKey) + \
                base58.b58decode(order.orderId)
        signature = crypto.sign(self.privateKey, sData)
        data = json.dumps({
            "sender": self.publicKey,
            "orderId": order.orderId,
            "signature": signature
        })
        req = lunespy.wrapper('/matcher/orderbook/%s/%s/cancel' % ('LUNES' if assetPair.asset1.assetId=='' else assetPair.asset1.assetId, 'LUNES' if assetPair.asset2.assetId=='' else assetPair.asset2.assetId), data, host=lunespy.MATCHER)
        if lunespy.OFFLINE:
            return req
        else:
            id = -1
            if req['status'] == 'OrderCanceled':
                id = req['orderId']
                logging.info('Order Cancelled - ID: %s' % id)
            return id

    def cancelOrderByID(self, assetPair, orderId):
        sData = base58.b58decode(self.publicKey) + \
                base58.b58decode(orderId)
        signature = crypto.sign(self.privateKey, sData)
        data = json.dumps({
            "sender": self.publicKey,
            "orderId": orderId,
            "signature": signature
        })
        req = lunespy.wrapper('/matcher/orderbook/%s/%s/cancel' % ('LUNES' if assetPair.asset1.assetId=='' else assetPair.asset1.assetId, 'LUNES' if assetPair.asset2.assetId=='' else assetPair.asset2.assetId), data, host=lunespy.MATCHER)
        if lunespy.OFFLINE:
            return req
        else:
            id = -1
            if req['status'] == 'OrderCanceled':
                id = req['orderId']
                logging.info('Order Cancelled - ID: %s' % id)
            return id

    def buy(self, assetPair, amount, price, maxLifetime=30 * 86400, matcherFee=lunespy.DEFAULT_MATCHER_FEE, timestamp=0):
        assetPair.refresh()
        normPrice = int(pow(10, 8 - assetPair.asset1.decimals) * price)
        id = self._postOrder(assetPair.asset1, assetPair.asset2, b'\0', amount, normPrice, maxLifetime, matcherFee, timestamp)
        if lunespy.OFFLINE:
            return id
        elif id != -1:
            return lunespy.Order(id, assetPair, self)

    def sell(self, assetPair, amount, price, maxLifetime=30 * 86400, matcherFee=lunespy.DEFAULT_MATCHER_FEE, timestamp=0):
        assetPair.refresh()
        normPrice = int(pow(10, 8 - assetPair.asset1.decimals) * price)
        id = self._postOrder(assetPair.asset1, assetPair.asset2, b'\1', amount, normPrice, maxLifetime, matcherFee, timestamp)
        if lunespy.OFFLINE:
            return id
        elif id!=-1:
            return lunespy.Order(id, assetPair, self)

    def tradableBalance(self, assetPair):
        try:
            req = lunespy.wrapper('/matcher/orderbook/%s/%s/tradableBalance/%s' % ('LUNES' if assetPair.asset1.assetId == '' else assetPair.asset1.assetId, 'LUNES' if assetPair.asset2.assetId == '' else assetPair.asset2.assetId, self.address), host=lunespy.MATCHER)
            if lunespy.OFFLINE:
                    return req
            amountBalance = req['LUNES' if assetPair.asset1.assetId == '' else assetPair.asset1.assetId]
            priceBalance = req['LUNES' if assetPair.asset2.assetId == '' else assetPair.asset2.assetId]
        except:
            amountBalance = 0
            priceBalance = 0
        if not lunespy.OFFLINE:
            return amountBalance, priceBalance

    def lease(self, recipient, amount, txFee=lunespy.DEFAULT_LEASE_FEE, timestamp=0):
        if not self.privateKey:
            logging.error('Private key required')
        elif amount <= 0:
            logging.error('Amount must be > 0')
        elif not lunespy.OFFLINE and self.balance() < amount + txFee:
            logging.error('Insufficient Lunes balance')
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\x08' + \
                    base58.b58decode(self.publicKey) + \
                    base58.b58decode(recipient.address) + \
                    struct.pack(">Q", amount) + \
                    struct.pack(">Q", txFee) + \
                    struct.pack(">Q", timestamp)
            signature = crypto.sign(self.privateKey, sData)
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "recipient": recipient.address,
                "amount": amount,
                "fee": txFee,
                "timestamp": timestamp,
                "signature": signature
            })
            req = lunespy.wrapper('/leasing/broadcast/lease', data)
            if lunespy.OFFLINE:
                return req
            else:
                return req['id']

    def leaseCancel(self, leaseId, txFee=lunespy.DEFAULT_LEASE_FEE, timestamp=0):
        if not self.privateKey:
            logging.error('Private key required')
        elif not lunespy.OFFLINE and self.balance() < txFee:
            logging.error('Insufficient Lunes balance')
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\x09' + \
                    base58.b58decode(self.publicKey) + \
                    struct.pack(">Q", txFee) + \
                    struct.pack(">Q", timestamp) + \
                    base58.b58decode(leaseId)
            signature = crypto.sign(self.privateKey, sData)
            data = json.dumps({
                "senderPublicKey": self.publicKey,
                "txId": leaseId,
                "fee": txFee,
                "timestamp": timestamp,
                "signature": signature
            })
            req = lunespy.wrapper('/leasing/broadcast/cancel', data)
            if lunespy.OFFLINE:
                return req
            elif 'leaseId' in req:
                return req['leaseId']

    def getOrderHistory(self, assetPair, timestamp=0):
        if timestamp == 0:
            timestamp = int(time.time() * 1000)
        sData = base58.b58decode(self.publicKey) + \
                struct.pack(">Q", timestamp)
        signature = crypto.sign(self.privateKey, sData)
        data = {
            "Accept": "application/json",
            "Timestamp": str(timestamp),
            "Signature": signature
        }
        req = lunespy.wrapper('/matcher/orderbook/%s/%s/publicKey/%s' % ('LUNES' if assetPair.asset1.assetId=='' else assetPair.asset1.assetId, 'LUNES' if assetPair.asset2.assetId=='' else assetPair.asset2.assetId, self.publicKey), headers=data, host=lunespy.MATCHER)
        return req

    def cancelOpenOrders(self, assetPair):
        orders = self.getOrderHistory(assetPair)
        for order in orders:
            status = order['status']
            orderId = order['id']
            if status=='Accepted' or status=='PartiallyFilled':
                sData = base58.b58decode(self.publicKey) + \
                        base58.b58decode(orderId)
                signature = crypto.sign(self.privateKey, sData)
                data = json.dumps({
                    "sender": self.publicKey,
                    "orderId": orderId,
                    "signature": signature
                })
                lunespy.wrapper('/matcher/orderbook/%s/%s/cancel' % ('LUNES' if assetPair.asset1.assetId == '' else assetPair.asset1.assetId, 'LUNES' if assetPair.asset2.assetId == '' else assetPair.asset2.assetId), data, host=lunespy.MATCHER)

    def deleteOrderHistory(self, assetPair):
        orders = self.getOrderHistory(assetPair)
        for order in orders:
            orderId = order['id']
            sData = base58.b58decode(self.publicKey) + \
                    base58.b58decode(orderId)
            signature = crypto.sign(self.privateKey, sData)
            data = json.dumps({
                "sender": self.publicKey,
                "orderId": orderId,
                "signature": signature
            })
            lunespy.wrapper('/matcher/orderbook/%s/%s/delete' % ('LUNES' if assetPair.asset1.assetId == '' else assetPair.asset1.assetId, 'LUNES' if assetPair.asset2.assetId == '' else assetPair.asset2.assetId), data, host=lunespy.MATCHER)

    def createAlias(self, alias, txFee=lunespy.DEFAULT_ALIAS_FEE, timestamp=0):
        aliasWithNetwork = b'\x02' + crypto.str2bytes(str(lunespy.CHAIN_ID)) + struct.pack(">H", len(alias)) + crypto.str2bytes(alias)
        if not self.privateKey:
            logging.error('Private key required')
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\x0a' + \
                    base58.b58decode(self.publicKey) + \
                    struct.pack(">H", len(aliasWithNetwork)) + \
                    crypto.str2bytes(str(aliasWithNetwork)) + \
                    struct.pack(">Q", txFee) + \
                    struct.pack(">Q", timestamp)
            signature = crypto.sign(self.privateKey, sData)
            data = json.dumps({
                "alias": alias,
                "senderPublicKey": self.publicKey,
                "fee": txFee,
                "timestamp": timestamp,
                "signature": signature
            })
            return lunespy.wrapper('/addresses/alias/broadcast/create', data)

    def sponsorAsset(self, assetId, minimalFeeInAssets, txFee=lunespy.DEFAULT_SPONSOR_FEE, timestamp=0):
        if not self.privateKey:
            logging.error('Private key required')
        else:
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\x0e' + \
                base58.b58decode(self.publicKey) + \
                base58.b58decode(assetId) + \
                struct.pack(">Q", minimalFeeInAssets) + \
                struct.pack(">Q", txFee) + \
                struct.pack(">Q", timestamp)
            signature = crypto.sign(self.privateKey, sData)

            data = json.dumps({
                "type": 14,
                "version": 1,
                "senderPublicKey": self.publicKey,
                "assetId": assetId,
                "fee": txFee,
                "timestamp": timestamp,
                "minSponsoredAssetFee": minimalFeeInAssets,
                "proofs": [
                    signature
                ]
            })

            return lunespy.wrapper('/transactions/broadcast', data)

    def setScript(self, scriptSource, txFee=lunespy.DEFAULT_SCRIPT_FEE, timestamp=0):
        script = lunespy.wrapper('/utils/script/compile', scriptSource)['script'][7:]
        if not self.privateKey:
            logging.error('Private key required')
        else:
            rawScript = base64.b64decode(script)
            scriptLength = len(rawScript)
            if timestamp == 0:
                timestamp = int(time.time() * 1000)
            sData = b'\x0d' + \
                b'\1' + \
                crypto.str2bytes(str(lunespy.CHAIN_ID)) + \
                base58.b58decode(self.publicKey) + \
                b'\1' + \
                struct.pack(">H", scriptLength) + \
                crypto.str2bytes(str(rawScript)) + \
                struct.pack(">Q", txFee) + \
                struct.pack(">Q", timestamp)
            signature = crypto.sign(self.privateKey, sData)

            data = json.dumps({
                "type": 13,
                "version": 1,
                "senderPublicKey": self.publicKey,
                "fee": txFee,
                "timestamp": timestamp,
                "script": 'base64:' + script,
                "proofs": [
                    signature
                ]
            })

            return lunespy.wrapper('/transactions/broadcast', data)

