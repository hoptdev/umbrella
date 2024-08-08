from webhook.models.telegram.updateModels import CallbackQuery
from webhook.models.telegram.models import TelegramBot
from ..models.shop.shopModels import Partner
from ..models.shop.userModels import ROLE_LEVELS, Role
import re

pattern = r"(([^_]+)_([^_]+))_(.*)"

callbackActions = {}

async def HandleCallbackAsync(bot: TelegramBot, query: CallbackQuery):
    action = next((v for k, v in callbackActions.get(bot.type).items() if query.data.startswith(k)), {})
    if not action:
        return
    
    match = re.match(pattern,query.data)
    if match:
        args = match.group(4).split("_")
    else:
        args = []

    p = await Partner.afirst(tgId = query.from_user.id, shop_id=bot.shop_id)

    if p and ROLE_LEVELS[Role(p.role)] >= ROLE_LEVELS[action.role]:
        await action.Action(bot, query, p, args)
    else:
        await bot.sendMessageAsync(query.chat.id, "У вас нет прав")
    return
