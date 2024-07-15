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

        bot.setData(c.from_user.id, "AddressSelectCity", args[0])
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

        bot.setData(c.from_user.id, "AddressSelectArea", args[0])
        
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

        bot.setData(c.from_user.id, "AddressSelectProduct", args[0])

        packs = await Pack.afilter(product_id=args[0])

        for pack in packs:
            buttons.append([InlineKeyboardButton(pack.size, f"{AddressSelectPack.data}_{pack.id}")])
        
        await bot.sendMessageAsync(c.chat.id, f"Выберите фасовку:", InlineKeyboardMarkup(buttons))

class AddressSelectPack:
    data = "address_selectPack"
    role = Role.COURIER

    async def Action(bot: TelegramBot, c: CallbackQuery, args=None):
        buttons = []

        bot.setData(c.from_user.id, "AddressSelectPack", args[0])
        
        await AddressSelectPack.SendInput(bot, c, args)

    async def SendInput(bot: TelegramBot, c: CallbackQuery, args=None):
        from .inputActions import AddressHandler

        bot.setNextHandler(c.from_user.id, AddressHandler.name)

        city = await City.aget(id=bot.getData(c.from_user.id, "AddressSelectCity")) 
        area = await Area.afirst(id=bot.getData(c.from_user.id, "AddressSelectArea"))
        product = await Product.aget(id=bot.getData(c.from_user.id, "AddressSelectProduct"))
        pack = await Pack.aget(id=bot.getData(c.from_user.id, "AddressSelectPack"))

        await bot.sendMessageAsync(c.chat.id, f"Город: {city.title}\nРайон: {area}\nТовар: {product.title} | {pack.size}\n\nВведите адрес.\n\n Для массового ввода используйте два перевода строки. Пример:\n\"address1\n\naddress2\"")

class AddressSendInput:
    data = "address_sendInput"
    role = Role.COURIER

    async def Action(bot: TelegramBot, c: CallbackQuery, args=None):
        await AddressSelectPack.SendInput(bot, c, args)