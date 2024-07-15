from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from webhook.models.shop.shopModels import *
from webhook.models.shop.userModels import *

from .callbackActions import ShopView

class StartCommand:
    command = "/start"
    replyCommand = "ℹ️ Меню"

    role = Role.DEFAULT

    replyButtons = ReplyKeyboardMarkup([[KeyboardButton(replyCommand, ShopView.data)]], True)
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🛒 Магазин", ShopView.data)]])

    async def SendProfile(bot: TelegramBot, msg: Message, p: Partner):
        await bot.sendMessageAsync(msg.chat.id, f"🛒 Магазин\n\n💰 Ваш баланс: {p.balance}$", StartCommand.buttons) 

    async def Action(bot: TelegramBot, msg: Message, p: Partner):
        await bot.sendMessageAsync(msg.chat.id, f"🛒 Приветствие", StartCommand.replyButtons) 

class MenuStart:
    command = StartCommand.replyCommand
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, msg: Message, p: Partner):
        await StartCommand.SendProfile(bot, msg, p)