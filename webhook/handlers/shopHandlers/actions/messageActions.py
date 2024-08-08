from webhook.models.telegram.updateModels import Message
from webhook.models.telegram.models import TelegramBot, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, Type
from webhook.models.shop.shopModels import Partner
from webhook.models.shop.userModels import Role
from webhook.models.decorator import register_command
from .callbackActions import ShopView, PartnerHistoryView, PaymentInfoView

@register_command(Type.ShopBot)
class StartCommand:
    data = "/start"
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

@register_command(Type.ShopBot)
class MenuStart:
    data = StartCommand.replyCommand
    role = Role.DEFAULT
    
    async def Action(bot: TelegramBot, msg: Message, p: Partner):
        await StartCommand.SendProfile(bot, msg, p)
    
  