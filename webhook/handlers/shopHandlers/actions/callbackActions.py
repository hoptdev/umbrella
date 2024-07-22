from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from webhook.models.shop.shopModels import *
from webhook.models.shop.userModels import *
from webhook.handlers.paymentHandler.btcHelper import minimalUSD
from webhook.models.payment.models import Wallet
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

    async def AddressesExistsAsync(packId, cityId):
        address = await Address.afirst(pack_id=packId, city_id = cityId, status=Status.ONSALE)
        return address is not None 

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        packs = await Pack.afilter(product_id=args[0])
        bot.setData(c.from_user.id, ShopSelectProduct.data, args[0])
        cityId = bot.getData(c.from_user.id, ShopSelectCity.data)
        
        buttons = []

        for pack in packs:
            packVisible = await ShopSelectProduct.AddressesExistsAsync(pack.id, cityId)
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
        areaData = bot.getData(c.from_user.id, ShopSelectArea.data)
        area = await Area.afirst(id=areaData) if areaData else None
        city = await City.afirst(bot.getData(c.from_user.id, ShopSelectCity.data))
        pack = await Pack.afirst(bot.getData(c.from_user.id, ShopSelectPack.data))
        packType = bot.getData(c.from_user.id, ShopSelectPack.type)
        product = await Product.afirst(bot.getData(c.from_user.id, ShopSelectProduct.data))
        
        preorder = packType is 'preorder'
        #todo проверка на preordeer etc!!! 
        buttons = [
            [InlineKeyboardButton("Подтвердить", f"{ShopBuyConfirm.data}_{(area.id if area else '-1')}_{city.id}_{pack.id}_{preorder}")]
        ]
        
        await bot.sendMessageAsync(c.chat.id, ShopSelectArea.GetBuyMessage(area, city, pack, packType, product), InlineKeyboardMarkup(buttons))
                
class ShopBuyConfirm:
    data = "shop_buyConfirm"
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        area = await Area.afirst(id=args[0])
        city = await City.afirst(id=args[1])
        pack = await Pack.afirst(id=args[2])
        preorder = args[3] is 'True'
        
        result = await BuyPackAsync(p, area, city, pack, preorder)
        text = result[1]
        
        if result[0]:
            coords = text.split()
            buttons = [
                [InlineKeyboardButton("Показать фото", f"{AddressPhotoView.data}_{result[2]}")]
            ]
            
            await bot.sendLocation(c.chat.id, coords[0], coords[1], buttons)
        else:
            await bot.sendMessageAsync(c.chat.id, text) 
        
class AddressPhotoView:
    data = "address_photoView"
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        pass
    
class PartnerHistoryView:
    data = "partner_historyView"
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        orders = await Order.afilter(partner_id=p.id)
        buttons = []
        #todo pagination
        for order in orders:
            buttons.append([InlineKeyboardButton(f"{order.status}|{order.create_time}", f'{OrderInfoView.data}_{order.id}')])
            
        await bot.sendMessageAsync(c.chat.id, "История покупок:", buttons)
            
class OrderInfoView:
    data = "order_InfoView"
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        order = await Order.afirst(id=args[0])
        product = await Product.afirst(id=order.product_id)
        pack = await Pack.afirst(id=order.pack_id)
        address = await Address.afirst(id=order.address_id)
        
        coords = address.data.split()
        text = f'Заказ #{order.id}\n\nТовар: {product.title} | {pack.size}\nСтоимость: {order.price}\nДата: {order.create_time}\nСтатус: {order.status}'
        
        await bot.sendMessageAsync(c.chat.id, text)
        await bot.sendLocation(c.chat.id, coords[0], coords[1])

class PaymentInfoView:
    data = "payment_infoView"
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        wallets = await Wallet.afilter(partner_id=p.id)
        
        text = 'Кошельки для пополения:\n\n'
        for wallet in wallets:
            text += f'{wallet.title} - {wallet.publicKey}\n'
        text += f"\nСистема автоматически обнаружит подтвержденное пополнение и пополнит баланс в USD по курсу на момент зачисления.\n\nСумма пополнения от {minimalUSD}$"
        
        await bot.sendMessageAsync(c.chat.id, text)