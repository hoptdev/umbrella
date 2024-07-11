from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from .messageCommands import *

commands = {}

async def HandleMessage(bot: TelegramBot, mes: Message):
    if mes.text in commands:
        action = commands[mes.text]

        p = await Partner.getFirstAsync(tgId = mes.from_user.id, shop_id=bot.shop_id)
        if not p:
            p = Partner(title=mes.from_user.first_name, tgId=mes.from_user.id, tgLogin=mes.from_user.username, shop_id=bot.shop_id)
            await p.asave()
        
        if p and ROLE_LEVELS[Role(p.role)] >= ROLE_LEVELS[action.role]:
            await action.Action(bot, mes)
        else:
            await bot.sendMessageAsync(mes.chat.id, "У вас нет прав")
    return

def RegisterCommands():
    global commands 
    commands = {
        '/start' : StartCommand,
    }
    return