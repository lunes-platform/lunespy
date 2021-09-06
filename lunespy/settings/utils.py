
def setOffline():
    global OFFLINE
    OFFLINE = True

def setOnline():
    global OFFLINE
    OFFLINE = False

def setChain(chain = CHAIN, chain_id = None):
    global CHAIN, CHAIN_ID

    if chain_id is not None:
        CHAIN = chain
        CHAIN_ID = chain_id
    else:
        if chain.lower()=='mainnet' or chain.lower()=='1':
            CHAIN = 'mainnet'
            CHAIN_ID = '1'
        elif chain.lower()=='hacknet' or chain.lower()=='u':
            CHAIN = 'hacknet'
            CHAIN_ID = 'U'
        else:
            CHAIN = 'testnet'
            CHAIN_ID = '0'

def getChain():
    return CHAIN

def setNode(node = NODE, chain = CHAIN, chain_id = None):
    global NODE, CHAIN, CHAIN_ID
    NODE = node
    setChain(chain, chain_id)

def getNode():
    return NODE

def setMatcher(node = MATCHER):
    global MATCHER, MATCHER_PUBLICKEY
    try:
        MATCHER_PUBLICKEY = wrapper('/matcher', host = node)
        MATCHER = node
        logging.info('Setting matcher %s %s' % (MATCHER, MATCHER_PUBLICKEY))
    except:
        MATCHER_PUBLICKEY = ''

def wrapper(api, postData='', host='', headers=''):
    global OFFLINE
    if OFFLINE:
        offlineTx = {}
        offlineTx['api-type'] = 'POST' if postData else 'GET'
        offlineTx['api-endpoint'] = api
        offlineTx['api-data'] = postData
        return offlineTx
    if not host:
        host = NODE
    if postData:
        req = requests.post('%s%s' % (host, api), data=postData, headers={'content-type': 'application/json'}).json()
    else:
        req = requests.get('%s%s' % (host, api), headers=headers).json()
    return req

def height():
    return wrapper('/blocks/height')['height']

def lastblock():
    return wrapper('/blocks/last')

def block(n):
    return wrapper('/blocks/at/%d' % n)

def tx(id):
    return wrapper('/transactions/info/%s' % id)

def getOrderBook(assetPair):
    orderBook = assetPair.orderbook()
    try:
        bids = orderBook['bids']
        asks = orderBook['asks']
    except:
        bids = ''
        asks = ''
    return bids, asks


def validateAddress(address):
    addr = crypto.bytes2str(base58.b58decode(address))
    if addr[0] != chr(ADDRESS_VERSION):
        logging.error("Wrong address version")
    elif addr[1] != CHAIN_ID:
        logging.error("Wrong chain id")
    elif len(addr) != ADDRESS_LENGTH:
        logging.error("Wrong address length")
    elif addr[-ADDRESS_CHECKSUM_LENGTH:] != crypto.hashChain(crypto.str2bytes(addr[:-ADDRESS_CHECKSUM_LENGTH]))[:ADDRESS_CHECKSUM_LENGTH]:
        logging.error("Wrong address checksum")
    else:
        return True
    return False




