from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from webhook.models.shop.shopModels import *
from webhook.models.shop.userModels import *
from asgiref.sync import sync_to_async

class AddressAdd:
    data = "address_add"
    role = Role.COURIER

    async def Action(bot: TelegramBot, callback: CallbackQuery):
        buttons = []
        shop = await Shop.getFirstAsync(id=bot.shop_id)

        async for city in shop.city.all():
            buttons.append([InlineKeyboardButton(city.title, f"address_selectCity_{city.id}")])
        
        await bot.sendMessageAsync(callback.chat.id, "Выберите город:", InlineKeyboardMarkup(buttons)) 