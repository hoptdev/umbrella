from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from .callbackActions import *

actions = {}

async def HandleCallback(bot: TelegramBot, query: CallbackQuery):
    if query.data in actions:
        action = actions[query.data]

        p = await Partner.getFirstAsync(tgId = query.from_user.id, shop_id=bot.shop_id)

        if p and ROLE_LEVELS[Role(p.role)] >= ROLE_LEVELS[action.role]:
            await action.Action(bot, query)
        else:
            await bot.sendMessageAsync(query.chat.id, "У вас нет прав")

        # await bot.answerCallbackQueryAsync(query.id)
    return

def RegisterActions():
    global actions 
    actions = {
        'address_add' : AddressAdd,
    }
    return
