from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from webhook.models.shop.shopModels import *
from webhook.models.shop.userModels import *


class AddressHandler:
    from .callbackActions import AddressSendInput

    name = "AddressHandler"
    role = Role.COURIER

    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Добавить еще", AddressSendInput.data)]])

    async def Action(bot: TelegramBot, msg: Message):
        print('-----> add')
        user = await Partner.afirst(tgId = msg.from_user.id, shop_id=bot.shop_id)

        _city = await City.aget(id=bot.getData(msg.from_user.id, "AddressSelectCity")) 
        _area = await Area.afirst(id=bot.getData(msg.from_user.id, "AddressSelectArea"))
        _pack = await Pack.aget(id=bot.getData(msg.from_user.id, "AddressSelectPack"))

        for address in msg.text.split('\n\n'):
            add = Address(data=address, area=_area, city=_city, pack=_pack, fromPartner=user)
            await add.asave()

        await bot.sendMessageAsync(msg.chat.id, "Адрес добавлен.") 