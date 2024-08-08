from django.db import models
from webhook.httpRequests.http import getAsync, postAsync, post
import json, os
from ..shop.shopModels import Shop

class Data:
    def __init__(self, inputs, nextAction=None):
        self.nextAction = nextAction
        self.inputs = inputs
    def setAction(self, action):
        self.nextAction = action
    def removeAction(self):
        self.nextAction = None

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
    
class KeyboardButton:
    def __init__(self, text):
        self.text = text

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
class ReplyKeyboardMarkup:
    def __init__(self, buttons, resize_keyboard):
        self.keyboard = buttons
        self.resize_keyboard = resize_keyboard

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class InputMediaPhoto:
    def __init__(self, media, caption=None):
        self.type = "photo"
        self.media = media
        self.caption = caption

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
    
    def removeData(self, tgId, nameData):
        if not tgId in self.userData:
            self.userData[tgId] = Data({})
        
        del self.userData[tgId].inputs[nameData]
    
    def getFullData(self, tgId) -> Data:
        if not tgId in self.userData:
            self.userData[tgId] = Data({})
        
        return self.userData[tgId]
    
    def getData(self, tgId, nameData):
        if not tgId in self.userData:
            self.userData[tgId] = Data({})
        
        return self.userData[tgId].inputs.get(nameData)
    
    def setData(self, tgId, nameData, value):
        if not tgId in self.userData:
            self.userData[tgId] = Data({})
        
        self.userData[tgId].inputs[nameData] = value

    def setNextHandler(self, tgId, value):
        if not tgId in self.userData:
            self.userData[tgId] = Data({})
        
        self.userData[tgId].inputs["nextInput"] = value

    def getNextHandler(self, tgId):
        if not tgId in self.userData:
            self.userData[tgId] = Data({})
        
        return self.userData[tgId].inputs.get("nextInput")

    def resetNextHandler(self, tgId):
        if not tgId in self.userData:
            self.userData[tgId] = Data({})
        
        self.userData[tgId].inputs["nextInput"] = None

    def getURL(self):
        return f'https://api.telegram.org/bot{self.token}/'

    async def getFileAsync(self, fileId):
        return await self.sendPost("getFile", fileId)

    async def sendGet(self, method):
        return await getAsync(f'{self.getURL()}{method}')
    
    async def sendPost(self, method, data, files=None):
        return await postAsync(f'{self.getURL()}{method}', data, files)

    async def getMeAsync(self):
        return await self.sendGet("getme")
    
    async def answerCallbackQueryAsync(self, callbackId):
        data = {'callback_query_id': callbackId}
        return await self.sendPost("answerCallbackQuery", data)
    
    async def sendMessageAsync(self, chatId, text, reply_markup = None):
        if reply_markup is not None and isinstance(reply_markup, list):
            reply_markup = InlineKeyboardMarkup(reply_markup)

        data = {'chat_id': chatId, 'text': text, 'reply_markup': reply_markup.toJson() if reply_markup is not None else None}
        return await self.sendPost("sendMessage", data)
    
    async def getFileUrlAsync(self, fileId):
        data = {'file_id': fileId}
        result = await self.sendPost("getfile", data)
        return f'https://api.telegram.org/file/bot{self.token}/{result['result']['file_path']}'
    
    async def sendMediaGroup(self, data, files):
        return await self.sendPost("sendMediaGroup", data, files)
    
    async def sendPhoto(self, data, files):
        return await self.sendPost("sendPhoto", data,files)
    
    async def sendLocation(self, chatId, latitude, longitude, reply_markup=None):
        if reply_markup is not None and isinstance(reply_markup, list):
            reply_markup = InlineKeyboardMarkup(reply_markup)
        
        data = {'chat_id': chatId, 'latitude': latitude, 'longitude': longitude, 'reply_markup': reply_markup.toJson() if reply_markup is not None else None}
        return await self.sendPost("sendLocation", data)
    
    async def sendMessageWithFileIdAsync(self, chatId, text, fileId, reply_markup = None):
        files = {'photo': fileId}
        data = {'chat_id': chatId, 'caption': text, 'reply_markup': reply_markup.toJson() if reply_markup is not None else None}
        return await self.sendPost("sendPhoto", data, files)
    
    async def deleteMessageAsync(self, chatId, messageId):
        data = {'chat_id': chatId, 'message_id': messageId}
        return await self.sendPost("deleteMessage", data)
    
    async def sendMessageWithPhotoAsync(self, chatId, text, photoPath: list, reply_markup = None):
        import os
        if len(photoPath) <= 1:
            photo = photoPath[0]
            photo = os.getcwd() + photo

            files = {'photo': open(photo, 'rb')}
            data = {'chat_id': chatId, 'caption': text, 'reply_markup': reply_markup.toJson() if reply_markup is not None else None}
            return await self.sendPhoto(data, files)
        else:
            media = []
            files = {}
            for i, path in enumerate(photoPath):
                media.append({
                    "type": "photo",
                    "media":f"attach://photo-{i}"
                    })
                files[f'photo-{i}'] = open(os.getcwd() + path, 'rb')

            media[0]["caption"] = text
            data = {'chat_id': chatId, 'media': json.dumps(media)}
            res = await self.sendMediaGroup(data, files)
            
            """ todo: close command
            messages = []
            for item in res['result']:
                messages.append(str(item['message_id']))
            
            data = {'chat_id': chatId, 'message_id': messages[0], 'caption': f"{text}\n\nЧтобы закрыть, нажмите: /close_{'_'.join(messages)}", 'reply_markup': reply_markup.toJson() if reply_markup is not None else None}
            res = await self.sendPost("editMessageCaption", data) 
            """
            return res

    
    def setWebhook(self):
        data = {'url': os.getenv('WEBHOOK_URL') + f'/webhook/{self.id}'} #todo in env
        r = post(f'{self.getURL()}setWebhook', data)
        return r