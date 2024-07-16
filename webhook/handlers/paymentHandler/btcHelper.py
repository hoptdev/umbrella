from bit import *
from bit.network import get_fee, get_fee_cached

confirmations = 1 #todo -> env
minimalUSD = 10
walletMain = 'mtMHJaWoVnQCxhjVFFbdHHB52WaZRecHPC'

def getKey():
    key = PrivateKeyTestnet()
    #key.segwit_address
    return (key.address, key.to_wif())

def getKeyFromWif(priv):
    key = PrivateKeyTestnet(priv)
    return key

def getConfirmedUnspents(key):
    confirmedUnspents = []
    for unspent in key.get_unspents():
        if unspent.confirmations >= confirmations:
            confirmedUnspents.append(unspent)
    return confirmedUnspents

def getBalance(key: Key, unspents, currency='btc'):
    key.balance = sum(unspent.amount for unspent in unspents)
    return (key.balance_as(currency))

def getFullInfo(key: Key, currency='btc'):
    unspents = getConfirmedUnspents(key)

    return (getBalance(key, unspents, currency), unspents)

def sendAll(key, _unspents):
    key.send([], unspents=_unspents, leftover=walletMain)

def check(privKey):
    key = getKeyFromWif(privKey)
    info = getFullInfo(key, 'usd')
    balanceUSD = info[0]

    if balanceUSD <= minimalUSD:
        return (False, balanceUSD)
    else:
        sendAll(key, info[1])
        return (True, balanceUSD)
    