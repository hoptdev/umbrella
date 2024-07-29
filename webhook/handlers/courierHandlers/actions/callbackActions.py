from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from webhook.models.shop.shopModels import *
from webhook.models.shop.userModels import *
# callbackData example: my_data, data_test_arg1 etc.. 

class AddressAdd:
    data = "address_add"
    role = Role.COURIER

    async def Action(bot: TelegramBot, callback: CallbackQuery, args=None):
        buttons = []
        shop = await Shop.afirst(id=bot.shop_id)

        async for city in shop.city.all():
            buttons.append([InlineKeyboardButton(city.title, f"{AddressSelectCity.data}_{city.id}")])
        
        await bot.sendMessageAsync(callback.chat.id, "Выберите город:", InlineKeyboardMarkup(buttons)) 

class AddressSelectCity:
    data = "address_selectCity"
    role = Role.COURIER

    async def Action(bot: TelegramBot, c: CallbackQuery, args=None):
        buttons = []

        bot.setData(c.from_user.id, AddressSelectCity.data, args[0])
        city = await City.aget(id=args[0])

        areas = await Area.afilter(city_id=city.id)
        
        if areas:
            for area in areas:
                buttons.append([InlineKeyboardButton(area.title, f"{AddressSelectArea.data}_{area.id}")])

            await bot.sendMessageAsync(c.chat.id, f"Выберите район:", InlineKeyboardMarkup(buttons))
        else:
            products = await Product.afilter(shop_id=bot.shop_id)
            for product in products:
                pack = await Pack.afirst(product_id=product.id)
                if pack:
                    buttons.append([InlineKeyboardButton(product.title, f"{AddressSelectProduct.data}_{product.id}")])

            await bot.sendMessageAsync(c.chat.id, f"Выберите товар:", InlineKeyboardMarkup(buttons))

class AddressSelectArea:
    data = "address_selectArea"
    role = Role.COURIER

    async def Action(bot: TelegramBot, c: CallbackQuery, args=None):
        buttons = []

        bot.setData(c.from_user.id, AddressSelectArea.data, args[0])
        
        products = await Product.afilter(shop_id=bot.shop_id)
        for product in products:
            pack = await Pack.afirst(product_id=product.id)
            if pack:
                buttons.append([InlineKeyboardButton(product.title, f"{AddressSelectProduct.data}_{product.id}")])
        
        await bot.sendMessageAsync(c.chat.id, f"Выберите товар:", InlineKeyboardMarkup(buttons))

class AddressSelectProduct:
    data = "address_selectProduct"
    role = Role.COURIER

    async def Action(bot: TelegramBot, c: CallbackQuery, args=None):
        buttons = []

        bot.setData(c.from_user.id, AddressSelectProduct.data, args[0])

        packs = await Pack.afilter(product_id=args[0])

        for pack in packs:
            buttons.append([InlineKeyboardButton(pack.size, f"{AddressSelectPack.data}_{pack.id}")])
        
        await bot.sendMessageAsync(c.chat.id, f"Выберите фасовку:", InlineKeyboardMarkup(buttons))

class AddressSelectPack:
    data = "address_selectPack"
    role = Role.COURIER

    async def Action(bot: TelegramBot, c: CallbackQuery, args=None):
        buttons = []

        bot.setData(c.from_user.id, AddressSelectPack.data, args[0])
        
        await AddressSelectPack.SendInput(bot, c, args)

    async def SendInput(bot: TelegramBot, c: CallbackQuery, args=None):
        from .inputActions import AddressHandler

        bot.setNextHandler(c.from_user.id, AddressHandler.name)

        city = await City.aget(id=bot.getData(c.from_user.id, AddressSelectCity.data)) 
        area = await Area.afirst(id=bot.getData(c.from_user.id, AddressSelectArea.data))
        product = await Product.aget(id=bot.getData(c.from_user.id, AddressSelectProduct.data))
        pack = await Pack.aget(id=bot.getData(c.from_user.id, AddressSelectPack.data))

        await bot.sendMessageAsync(c.chat.id, f"Город: {city.title}\nРайон: {area}\nТовар: {product.title} | {pack.size}\n\nВведите адрес.")

class AddressSendInput:
    data = "address_sendInput"
    role = Role.COURIER

    async def Action(bot: TelegramBot, c: CallbackQuery, args=None):
        await AddressSelectPack.SendInput(bot, c, args)
        
class AddressReset:
    data = "address_reset"
    role = Role.COURIER

    async def Reset(bot: TelegramBot, tgId):
        for key in list(bot.getFullData(tgId).inputs.keys()):
            if key.startswith('address_'):
                bot.removeData(tgId, key)

    async def Action(bot: TelegramBot, c: CallbackQuery, args=None):
        await AddressReset.Reset(bot, c.chat.id)
        await bot.deleteMessageAsync(c.chat.id, c.message.message_id)
        