from ...models.shop.shopModels import Partner, Area, City, Pack, Address, Status, PreOrderInfo, Order, OrderStatus
from ...models.payment.models import Wallet, Cryptocurrency
import asyncio
import datetime
from .btcHelper import check
from umbrella.celery import app
import asyncio
from asgiref.sync import async_to_sync

lock = asyncio.Lock()

async def Process():
    while True:
       async for wallet in Wallet.objects.all():
           if wallet.title == Cryptocurrency.BTC:
               info = check(wallet.privateKey) #todo разобраться с комсой
               if info[0]:
                   partner = await Partner.afirst(id=wallet.partner_id)
                   partner.balance += info[1]
                   await partner.asave()
                   
@app.task(name="PaymentHandler")                   
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
                
                info = PreOrderInfo(city=city, area=area, partner=partner, pack=pack, active=True)
                await info.asave()
                await CreateOrderAsync(partner, area, city, pack, OrderStatus.WAIT, None)
                return (False, "Запрос на предзаказ создан.")
            else:
                return (False, "Данный товар отсутствует в выбранном районе")
        
        
async def CreateOrderAsync(partner: Partner, area, city: City, pack: Pack, status: OrderStatus, address):
    order = Order(status=status, partne_idr=partner.id, product_id=pack.product_id, pack_id=pack.id, city_id=city.id, 
                  area=area, price=pack.price, create_time=datetime.datetime.now(), address=address)
    await order.asave()
    return order