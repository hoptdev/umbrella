from webhook.models.telegram.updateModels import Message
from webhook.models.telegram.models import TelegramBot
from ..models.shop.shopModels import Partner
from ..models.shop.userModels import ROLE_LEVELS, Role

commandActions = {}
inputActions = {}

async def HandleMessageAsync(bot: TelegramBot, mes: Message):
    if not hasattr(mes, 'text'):
        mes.text = ''
    
    actions = commandActions[bot.type]
    if mes.text in actions:
        action = actions[mes.text]
        
        p = await Partner.afirst(tgId = mes.from_user.id, shop_id=bot.shop_id)
        if not p:
            p = Partner(title=mes.from_user.first_name, tgId=mes.from_user.id, tgLogin=mes.from_user.username, shop_id=bot.shop_id)
            await p.saveAsync()
        
        if p and ROLE_LEVELS[Role(p.role)] >= ROLE_LEVELS[action.role]:
            await action.Action(bot, mes, p)
        else:
            await bot.sendMessageAsync(mes.chat.id, "У вас нет прав")
            
        bot.resetNextHandler(mes.from_user.id)
    else:
        next = bot.getNextHandler(mes.from_user.id)
        bot.resetNextHandler(mes.from_user.id)
        if next in inputActions:
            await inputActions[next].Action(bot, mes)
    return