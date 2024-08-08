from ...models.shop.shopModels import Partner, Area, City, Pack, Address, Status, PreOrderInfo, Order, OrderStatus
from ...models.payment.models import Wallet, Cryptocurrency
import asyncio
import datetime
from .btcHelper import check
from umbrella.celery import app
import asyncio
from asgiref.sync import async_to_sync
import decimal
import os
from .ltcHelper import getAllBalance, sendAll
from .rateHelper import getUSDfromLTCAsync

lock = asyncio.Lock()


LTC_MAINWALLET = os.getenv('LTC_WALLET')

async def Process():
    while True:
        try: 
            await LitecoinHandler()
            
            async for wallet in Wallet.objects.all():
                if wallet.title == Cryptocurrency.BTC:
                    info = check(wallet.privateKey) 
                    if info[0]:
                        partner = await Partner.afirst(id=wallet.partner_id)
                        partner.balance += info[1]
                        await partner.asave()
        except Exception as e:
            print(e)

async def LitecoinHandler():
    wallets = getAllBalance()
    for walletInfo in wallets:
        for wallet in walletInfo:
            if wallet[1] != 0.0:
                tx = sendAll(wallet[0], LTC_MAINWALLET) #todo save transactions
                async with lock:
                    partner = await Partner.afirst(id=int(wallet[2]))
            
                    balanceLTC = wallet[1]
                    balanceUSD = await getUSDfromLTCAsync(balanceLTC)
                    partner.balance += decimal.Decimal(balanceUSD)
                    await partner.asave()
            
            
    print(wallets)
                   
@app.task(name="PaymentHandler", ignore_result=True)                   
def PaymentHandler():
    async_to_sync(Process)()
               

async def BuyPackAsync(partner: Partner, area, city: City, pack: Pack, preorder):
    async with lock:
        if(partner.balance < pack.price):
            return (False, "Недостаточно средств.")
        
        if area is not None:
            address = await Address.afirst(area_id=area.id, city_id=city.id, pack_id=pack.id, status=Status.ONSALE)
        else:
            address = await Address.afirst(city_id=city.id, pack_id=pack.id, status=Status.ONSALE)
        
        if address:
            address.status = Status.SOLD
            await address.asave()
            
            partner.balance -= pack.price
            await partner.asave()
            
            await CreateOrderAsync(partner, area, city, pack, OrderStatus.COMPLETED, address)
            
            return (True, address.data, address.id)
        else:
            if preorder:
                partner.balance -= pack.price
                await partner.asave()     
            
                order = await CreateOrderAsync(partner, area, city, pack, OrderStatus.WAIT, None)
                
                await CreatePreOrderAsync(city, area, partner, pack, order.id)
                
                return (False, "Запрос на предзаказ создан.")
            else:
                return (False, "Данный товар отсутствует в выбранном районе")
        
        
async def CreateOrderAsync(partner: Partner, area, city: City, pack: Pack, status: OrderStatus, address):
    order = Order(status=status, partner_id=partner.id, product_id=pack.product_id, pack_id=pack.id, city_id=city.id, 
                  area=area, price=pack.price, create_time=datetime.datetime.now(), address=address)
    await order.asave()
    return order

async def CreatePreOrderAsync(city, area, partner: Partner, pack, orderId):
    info = PreOrderInfo(city=city, area=area, partner=partner, pack=pack, active=True, order_id=orderId, shop_id=partner.shop_id)
    await info.asave()
    return info