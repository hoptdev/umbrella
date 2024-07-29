import json
from ...httpRequests.http import sendRpc

WALLET_NAME = 'umbrella'
RPC_USER = 'user'
RPC_PASSWORD = 'pass'
RPC_PORT = 19332 
RPC_URL = f'http://127.0.0.1:{RPC_PORT}/wallet/{WALLET_NAME}'
FEE_RATE = 0.0000001 

def rpcRequest(method, params=[]):
    payload = json.dumps({
        "jsonrpc": "1.0",
        "id": "python-client",
        "method": method,
        "params": params
    })
    response = sendRpc(RPC_URL, (RPC_USER, RPC_PASSWORD), payload)
    if response.status_code == 200:
        return response.json()['result']
    else:
        return []

def getAllBalance():
    return rpcRequest('listaddressgroupings')

def getWallets():
    return rpcRequest('listwallets')

def createWallet(name):
    if name not in getWallets():
         return rpcRequest('createwallet', [name])
    
    return 'Wallet exists'

def getNewAddress(name):
    return rpcRequest('getnewaddress', [name])

def getAddressesByLabel(name):
    return rpcRequest('getaddressesbylabel', [name])

def getPrivateKey(address):
    return rpcRequest('dumpprivkey', [address])

def createFullKey(name):
    addresses = getAddressesByLabel(str(name))
    if addresses != []:
        return 'Key exists'
    
    address = getNewAddress(str(name))
    privkey = getPrivateKey(address)
    return (address, privkey)

def sendAll(fromAddress, toAddress):
    utxos = rpcRequest('listunspent', [1, 9999999, [fromAddress]])

    if not utxos:
        return "No UTXOs available"
    total_amount = sum(utxo['amount'] for utxo in utxos)

    num_inputs = len(utxos)
    num_outputs = 1 
    estimated_size = (num_inputs * 180) + (num_outputs * 34) + 10
    fee = estimated_size * FEE_RATE

    amount_to_send = round((total_amount - fee), 14)

    if amount_to_send <= 0:
        return "Not enough balance to cover the fee"
        
    tx_inputs = [{"txid": utxo['txid'], "vout": utxo['vout']} for utxo in utxos]
    tx_outputs = [{toAddress: amount_to_send}]
    raw_tx = rpcRequest('createrawtransaction', [tx_inputs, tx_outputs])
    signed_tx = rpcRequest('signrawtransactionwithwallet', [raw_tx])
    txid = rpcRequest('sendrawtransaction', [signed_tx['hex']])
    return txid


createWallet(WALLET_NAME)