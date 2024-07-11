from django.db import models
from webhook.httpRequests.http import getAsync, postAsync
import json
from ..shop.shopModels import Shop
from json import JSONEncoder

class InlineKeyboardButton:
    def __init__(self, text, callback_data):
        self.text = text
        self.callback_data = callback_data

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
class InlineKeyboardMarkup:
    def __init__(self, buttons):
        self.inline_keyboard = buttons

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Type(models.TextChoices):
    ShopBot = 'ShopBot', 'ShopBot'
    CourierBot = 'CourierBot', 'CourierBot'

class TelegramBot(models.Model):
    token = models.CharField(max_length=50)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=64, choices=Type.choices, default=Type.CourierBot)

    userData = {}

    def getURL(self):
        return f'https://api.telegram.org/bot{self.token}/'

    async def sendGet(self, method):
        return await getAsync(f'{self.getURL()}{method}')
    
    async def sendPost(self, method, data):
        return await postAsync(f'{self.getURL()}{method}', data)

    async def getMeAsync(self):
        return await self.sendGet("getme")
    
    async def answerCallbackQueryAsync(self, callbackId):
        data = {'callback_query_id': callbackId}
        return await self.sendPost("answerCallbackQuery", data)
    
    async def sendMessageAsync(self, chatId, text, reply_markup: InlineKeyboardMarkup = None):
        data = {'chat_id': chatId, 'text': text, 'reply_markup': reply_markup.toJson() if reply_markup is not None else None}
        return await self.sendPost("sendMessage", data)
    
    async def setWebhook(self):
        data = {'url': 'https://9af8-31-28-113-222.ngrok-free.app' + f'/webhook/{self.id}'}
        r = await postAsync(f'{self.getURL()}setWebhook', data)
        return r
    
class Data:
    def __init__(self, inputs, nextAction=None):
        self.nextAction = nextAction
        self.inputs = inputs
    def setAction(self, action):
        self.nextAction = action
    def removeAction(self):
        self.nextAction = None