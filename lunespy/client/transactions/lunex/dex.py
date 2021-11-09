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
