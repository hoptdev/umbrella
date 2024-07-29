import time
from ...httpRequests.http import getAsync

URL = 'https://bitpay.com/rates'
CACHE = {} 
CACHE_EXPIRATION_TIME = 60 * 5 #todo -> env

async def calculateAsync(fromC, toC, amount):
    key = f'{fromC}_{toC}'
    current_time = time.time()
    
    if key in CACHE:
        rate_info = CACHE[key]
        if current_time - rate_info['timestamp'] < CACHE_EXPIRATION_TIME:
            return amount * rate_info['rate']
    
    rates = await getAsync(f'{URL}/{fromC}/{toC}')
    rate = rates['data']['rate']
    
    CACHE[key] = {
        'rate': rate,
        'timestamp': current_time
    }
    
    return amount * rate
    

async def getUSDfromLTCAsync(ltc):
    return await calculateAsync('LTC', 'USD', ltc)