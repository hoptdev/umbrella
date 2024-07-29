from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from .actions.messageActions import *

commands = {}
inputHandlers = {}

async def HandleMessage(bot: TelegramBot, mes: Message):
    if not hasattr(mes, 'text'):
        mes.text = ''
    
    if mes.text in commands:
        action = commands[mes.text]
        
        p = await Partner.afirst(tgId = mes.from_user.id, shop_id=bot.shop_id)
        if not p:
            p = Partner(title=mes.from_user.first_name, tgId=mes.from_user.id, tgLogin=mes.from_user.username, shop_id=bot.shop_id)
            await p.saveAsync()
        
        if p and ROLE_LEVELS[Role(p.role)] >= ROLE_LEVELS[action.role]:
            await action.Action(bot, mes)
        else:
            await bot.sendMessageAsync(mes.chat.id, "У вас нет прав")
            
        bot.resetNextHandler(mes.from_user.id)
    else:
        next = bot.getNextHandler(mes.from_user.id)
        bot.resetNextHandler(mes.from_user.id)
        if next in inputHandlers:
            await inputHandlers[next].Action(bot, mes)
    return

def RegisterCommands():
    global commands 
    commands = {
        StartCommand.command : StartCommand,
    }
    return

def RegisterInputHandlers():
    from .actions.inputActions import AddressHandler
    
    global inputHandlers 
    inputHandlers = {
        AddressHandler.name : AddressHandler,
    }
    return