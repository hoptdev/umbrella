from webhook.models.telegram.updateModels import Message
from webhook.models.telegram.models import Type, TelegramBot, InlineKeyboardButton, InlineKeyboardMarkup
from webhook.models.shop.shopModels import Partner
from webhook.models.shop.userModels import Role
from webhook.models.decorator import register_command
from .callbackActions import AddressAdd

@register_command(Type.CourierBot)
class StartCommand:
    data = "/start"
    role = Role.COURIER

    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Добавить адерес", AddressAdd.data)]])

    async def Action(bot: TelegramBot, msg: Message, p : Partner):
        user = await Partner.afirst(tgId = msg.from_user.id, shop_id=bot.shop_id)

        await bot.sendMessageAsync(msg.chat.id, "☀️ Приветствие", StartCommand.buttons) 