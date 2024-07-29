import urllib.request
from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from webhook.models.shop.shopModels import *
from webhook.models.shop.userModels import *
import re
import os
import urllib
from asgiref.sync import sync_to_async
from django.core.files import File 

from .callbackActions import AddressSelectCity, AddressSelectArea, AddressSelectPack, AddressReset

class AddressHandler:
    from .callbackActions import AddressSendInput

    name = "AddressHandler"
    dataLocation = "address_LocationData"
    role = Role.COURIER
    
    pattern = r"\w-?\d+(\.\d+)?\s-?\d+(\.\d+)?\b"

    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Добавить еще адрес", AddressSendInput.data)], [InlineKeyboardButton("Закончить", AddressReset.data)]])

    def is_two_floats(s):
        parts = s.split()
        if len(parts) != 2:
            return False
        try:
            float(parts[0])
            float(parts[1])
            return True
        except ValueError:
            return False
        
    @sync_to_async
    def AddressImageSave(self, address : Address, name, filepath):
        address.file.save(name, File(open(filepath, 'rb')))
    
    async def CreateAddress(bot : TelegramBot, location, data, fileId, _area, _city, _pack, user : Partner):
        url = await bot.getFileUrlAsync(fileId)
        result = urllib.request.urlretrieve(url)
        last = f'.{os.path.basename(url).split('.')[-1]}'
        filename = f'{fileId}{last}'
        
        add = Address(location=location, data=data, area=_area, city=_city, pack=_pack, fromPartner=user)
        await AddressHandler.AddressImageSave(add, filename, result[0])
        await add.asave()
        await AddressHandler.SearchPreorder(add, _area, _city, _pack, user.shop_id)
        
        
    async def SearchPreorder(address: Address, _area, _city, _pack, shopid):
        if _area != None:
            preorder = await PreOrderInfo.afirst(area_id=_area.id, city_id=_city.id, pack_id=_pack.id, shop_id=shopid, active=1)
        else:
            preorder = await PreOrderInfo.afirst(city_id=_city.id, pack_id=_pack.id, shop_id=shopid, active=1)
            
        if preorder != None:
            address.status = Status.SOLD
            await address.asave()
            preorder.active = 0
            await preorder.asave()
            order = await Order.afirst(id=preorder.order_id)
            order.status = OrderStatus.COMPLETED
            order.address_id=address.id
            await order.asave()
            
    async def ParseLocation(bot: TelegramBot, msg: Message):
        data = f'{msg.location.latitude} {msg.location.longitude}'
        
        bot.setData(msg.from_user.id, AddressHandler.dataLocation, data)
        bot.setNextHandler(msg.from_user.id, AddressHandler.name)
        
        await bot.sendMessageAsync(msg.chat.id, "Локация сохранена. Введите информацию о кладе.") 
    
    async def ParseData(bot: TelegramBot, msg: Message):
        if hasattr(msg, 'caption'):
            text = msg.caption
        else:
            text = msg.text
        if hasattr(msg, "photo"):
            photo = msg.photo[-1]['file_id']
        else:
            photo = None
            
        locSearch = re.search(AddressHandler.pattern, text)
        locCache = bot.getData(msg.from_user.id, AddressHandler.dataLocation)
        
        if not locCache and locSearch != None:
            location = locSearch.group()
        else:
            location = locCache
        
        user = await Partner.afirst(tgId = msg.from_user.id, shop_id=bot.shop_id)
        _city = await City.aget(id=bot.getData(msg.from_user.id, AddressSelectCity.data)) 
        _area = await Area.afirst(id=bot.getData(msg.from_user.id, AddressSelectArea.data))
        _pack = await Pack.aget(id=bot.getData(msg.from_user.id, AddressSelectPack.data))
        await AddressHandler.CreateAddress(bot,location, text, photo, _area, _city, _pack, user)
        await bot.sendMessageAsync(msg.chat.id, "Адрес добавлен.", AddressHandler.buttons) 
        return
            
        
    async def Action(bot: TelegramBot, msg: Message):
        if msg.location != None:
            await AddressHandler.ParseLocation(bot, msg)
        else:
            await AddressHandler.ParseData(bot, msg)