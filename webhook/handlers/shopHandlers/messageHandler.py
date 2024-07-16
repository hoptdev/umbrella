from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from .actions.messageActions import *

commands = {}
inputHandlers = {}

async def HandleMessage(bot: TelegramBot, mes: Message):
    if mes.text in commands:
        action = commands[mes.text]
        
        p = await Partner.afirst(tgId = mes.from_user.id, shop_id=bot.shop_id)
        if not p:
            p = Partner(title=mes.from_user.first_name, tgId=mes.from_user.id, tgLogin=mes.from_user.username, shop_id=bot.shop_id)
            await p.saveAsync()
        
        if p and ROLE_LEVELS[Role(p.role)] >= ROLE_LEVELS[action.role]:
            await action.Action(bot, mes, p)
        else:
            await bot.sendMessageAsync(mes.chat.id, "У вас нет прав")
    else:
        next = bot.getNextHandler(mes.from_user.id)
        bot.resetNextHandler(mes.from_user.id)
        if next in inputHandlers:
            await inputHandlers[next].Action(bot, mes)

    bot.resetNextHandler(mes.from_user.id)
    return

def RegisterCommands():
    global commands 
    commands = {
        StartCommand.command : StartCommand,
        MenuStart.command: MenuStart,
    }
    return

def RegisterInputHandlers():
    global inputHandlers 
    inputHandlers = {

    }
    return