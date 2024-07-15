from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from webhook.models.shop.shopModels import *
from webhook.models.shop.userModels import *

from .callbackActions import AddressAdd

class StartCommand:
    command = "/start"
    role = Role.COURIER

    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Добавить адерес", AddressAdd.data)]])

    async def Action(bot: TelegramBot, msg: Message):
        user = await Partner.afirst(tgId = msg.from_user.id, shop_id=bot.shop_id)

        await bot.sendMessageAsync(msg.chat.id, "☀️ Приветствие", StartCommand.buttons) 