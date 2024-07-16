from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from webhook.models.shop.shopModels import *
from webhook.models.shop.userModels import *
# callbackData example: my_data, data_test_arg1 etc.. 

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
        bot.setData(c.from_user.id, "ShopSelectCity", args[0])
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
        address = await Address.afirst(pack_id=packId)
        return address is not None 

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        packs = await Pack.afilter(product_id=args[0])
        bot.setData(c.from_user.id, "ShopSelectProduct", args[0])
        buttons = []

        for pack in packs:
            packVisible = await ShopSelectProduct.AddressesExistsAsync(pack.id)
            if packVisible:
                buttons.append(InlineKeyboardButton(f"{pack.size} | Moment", f"{ShopSelectPack.data}_{pack.id}"))
            elif pack.preorder:
                buttons.append(InlineKeyboardButton(f"{pack.size} | PreOrder", f"{ShopSelectPack.data}_{pack.id}"))

class ShopSelectPack:
    data = "shop_selectPack"
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, c: CallbackQuery, p: Partner, args=None):
        packs = await Pack.afilter(product_id=args[0])
        bot.setData(c.from_user.id, "ShopSelectPack", args[0])
        buttons = []

        for pack in packs:
            packVisible = ShopSelectProduct.AddressesExists(pack.id)
            if packVisible:
                buttons.append(InlineKeyboardButton(f"{pack.size} | Moment", f"{ShopSelectProduct.data}_{pack.id}"))
            elif pack.preorder:
                buttons.append(InlineKeyboardButton(f"{pack.size} | PreOrder", f"{ShopSelectProduct.data}_{pack.id}"))
                
    