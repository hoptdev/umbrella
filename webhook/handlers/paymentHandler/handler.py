from ...models.shop.shopModels import Partner, Area, City, Pack, Address, Status
from ...models.payment.models import Wallet
import asyncio

lock = asyncio.Lock()

async def BuyPackAsync(partner: Partner, area: Area, city: City, pack: Pack):
    async with lock:
        if(partner.balance < pack.price):
            return "Недостаточно средств."
        
        address = await Address.afirst(area_id=area.id, city_id=city.id, pack_id=pack.id, status=Status.ONSALE)
        
        if address:
            address.status = Status.SOLD
            await address.asave()
            
            partner.balance -= pack.price
            await partner.asave()
            
            return address.data
            
            
        await partner.asave()
        
        
        
        
    