from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from webhook.models.shop.shopModels import *
from webhook.models.shop.userModels import *

from .callbackActions import ShopView, PartnerHistoryView, PaymentInfoView

class StartCommand:
    command = "/start"
    replyCommand = "ℹ️ Меню"

    role = Role.DEFAULT

    replyButtons = ReplyKeyboardMarkup([[KeyboardButton(replyCommand)]], True)
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🛒 Магазин", ShopView.data)],
         [InlineKeyboardButton("💳 Пополнение", PaymentInfoView.data), InlineKeyboardButton("🛍 Покупки", PartnerHistoryView.data)]
         ]
        )

    async def SendProfile(bot: TelegramBot, msg: Message, p: Partner):
        await bot.sendMessageAsync(msg.chat.id, f"🛒 Магазин\n\n💰 Ваш баланс: {p.balance}$", StartCommand.buttons) 

    async def Action(bot: TelegramBot, msg: Message, p: Partner):
        await bot.sendMessageAsync(msg.chat.id, f"🛒 Приветствие", StartCommand.replyButtons) 

class MenuStart:
    command = StartCommand.replyCommand
    async def Action(bot: TelegramBot, msg: Message, p: Partner):
        await StartCommand.SendProfile(bot, msg, p)
    role = Role.DEFAULT
  