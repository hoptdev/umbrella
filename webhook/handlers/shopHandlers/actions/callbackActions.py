from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from webhook.models.shop.shopModels import *
from webhook.models.shop.userModels import *
# callbackData example: my_data, data_test_arg1 etc.. 
from ...paymentHandler.handler import BuyPackAsync

class ShopView:
    data = "shop_view"
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, callback: CallbackQuery, p: Partner, args=None):
        shop = await Shop.afirst(id=bot.shop_id)
        buttons = []

        async for city in shop.city.all():
            buttons.append([InlineKeyboardButton(city.title, f"{ShopSelectCity.data}_{city.id}")])
        
        await bot.sendMessageAsync(callback.chat.id, "🧾 Start order\n\nВыберите, пожалуйста, в каком городе вы хотите получить заказ.", InlineKeyboardMarkup(buttons))  #todo: change -> delete + send

class ShopSelectCity:
    data = "shop_selectCity"
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        bot.setData(c.from_user.id, ShopSelectCity.data, args[0])
        buttons = []
        
        products = await Product.afilter(shop_id=bot.shop_id)
        for product in products:
            pack =  await Pack.afirst(product_id=product.id)
            if pack is not None:
                buttons.append([InlineKeyboardButton(product.title, f"{ShopSelectProduct.data}_{product.id}"), InlineKeyboardButton("INFO", f"{ShopProductInfo.data}_{product.id}")])

        await bot.sendMessageAsync(c.chat.id, "🧾 Select product\n\nВыберите, пожалуйста, товар, который желаете приобрести:", InlineKeyboardMarkup(buttons)) 

class ShopProductInfo:
    data = "shop_productInfo"
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        product = await Product.afirst(id=args[0])

        if product is None:
            await bot.sendMessageAsync(c.chat.id, "Товар не сущетсвует.") 


        await bot.sendMessageWithPhotoAsync(c.chat.id, product.description, [product.photo1.url, product.photo2.url]) 

class ShopSelectProduct:
    data = "shop_selectProduct"
    role = Role.DEFAULT

    async def AddressesExistsAsync(packId):
        address = await Address.afirst(pack_id=packId, status=Status.ONSALE)
        return address is not None 

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        packs = await Pack.afilter(product_id=args[0])
        bot.setData(c.from_user.id, ShopSelectProduct.data, args[0])
        buttons = []

        for pack in packs:
            packVisible = await ShopSelectProduct.AddressesExistsAsync(pack.id)
            if packVisible:
                buttons.append([InlineKeyboardButton(f"{pack.size} | Moment | {pack.price}$", f"{ShopSelectPack.data}_{pack.id}_moment")])
            elif pack.preorder:
                buttons.append([InlineKeyboardButton(f"{pack.size} | PreOrder | {pack.price}$", f"{ShopSelectPack.data}_{pack.id}_preorder")])
        await bot.sendMessageAsync(c.chat.id, "Выберите фасовку:", InlineKeyboardMarkup(buttons)) 

class ShopSelectPack:
    data = "shop_selectPack"
    type = "shop_selectPackType"
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        bot.setData(c.from_user.id, ShopSelectPack.data, args[0])
        bot.setData(c.from_user.id, f"{ShopSelectPack.type}", args[1])
        
        areas = await Area.afilter(city_id=bot.getData(c.from_user.id, ShopSelectCity.data))
        buttons = []
        
        if areas is not [] and areas is not None:
            for area in areas:
                buttons.append([InlineKeyboardButton(f"{area.title}", f"{ShopSelectArea.data}_{area.id}")])
            await bot.sendMessageAsync(c.chat.id, "Выберите район:", buttons)
        else:
            bot.setData(c.from_user.id, ShopSelectArea.data, None)
            await ShopSelectArea.BuyRequest(bot, c, args)
                
class ShopSelectArea:
    data = "shop_selectArea"
    role = Role.DEFAULT

    def GetBuyMessage(area: Area, city: City, pack: Pack, packType, product : Product):
        return f"🧾 PreCheck:\n\n🏙 Location (Локация): {city.title}/ {area.title if area else ""}\n📦 Product (Товар): {product.title} / {pack.size} | {packType}\n\n💲 Price (Стоимость): {pack.price}$"

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        bot.setData(c.from_user.id, ShopSelectArea.data, args[0])
        await ShopSelectArea.BuyRequest(bot, c, p, args)
        
    async def BuyRequest(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        area = await Area.afirst(id=bot.getData(c.from_user.id, ShopSelectArea.data))
        city = await City.afirst(bot.getData(c.from_user.id, ShopSelectCity.data))
        pack = await Pack.afirst(bot.getData(c.from_user.id, ShopSelectPack.data))
        packType = bot.getData(c.from_user.id, ShopSelectPack.type)
        product = await Product.afirst(bot.getData(c.from_user.id, ShopSelectProduct.data))
        
        #todo проверка на preordeer etc!!! await BuyPack(p, area, city, pack)
        buttons = [
            [InlineKeyboardButton("Подтвердить", f"{ShopBuyConfirm.data}_{area.id}_{city.id}_{pack.id}")]
        ]
        
        await bot.sendMessageAsync(c.chat.id, ShopSelectArea.GetBuyMessage(area, city, pack, packType, product), InlineKeyboardMarkup(buttons))
                
class ShopBuyConfirm:
    data = "shop_buyConfirm"
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        area = await Area.afirst(id=args[0])
        city = await City.afirst(id=args[1])
        pack = await Pack.afirst(id=args[2])
        
        result = await BuyPackAsync(p, area, city, pack)
        await bot.sendMessageAsync(c.chat.id,  result) 