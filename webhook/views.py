from django.http import HttpResponse
from webhook.models.telegram.models import TelegramBot
from django.views.decorators.csrf import csrf_exempt
from umbrella.celery import app
import asyncio
from webhook.models.telegram.updateModels import *

from webhook.models.telegram.models import Type

from .handlers.courierHandlers.messageHandler import HandleMessage as CourierHandlerMessage
from .handlers.courierHandlers.callbackHandler import HandleCallback as CourierHandleCallback

from .handlers.shopHandlers.messageHandler import HandleMessage as ShopHandlerMessage
from .handlers.shopHandlers.callbackHandler import HandleCallback as ShopHandleCallback

async def HandleUpdate(body, botId):
    print(body) #todo dev

    bot = await TelegramBot.objects.aget(id=botId)
    update = Update(body)

    if bot.type == Type.CourierBot:
        if update.message:
            await CourierHandlerMessage(bot, update.message)
        elif update.callback_query:
            await CourierHandleCallback(bot, update.callback_query)
    else:
        if update.message:
            await ShopHandlerMessage(bot, update.message)
        elif update.callback_query:
            await ShopHandleCallback(bot, update.callback_query)
    return

@app.task(ignore_result=True)
def RunHandleUpdate(body, botId):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run((HandleUpdate(body, botId)))

@csrf_exempt
def webhook(request, botId):
    try:
        if request.method == "POST":
            RunHandleUpdate(request.body, botId)
            #RunHandleUpdate.delay(request.body, botId)
        return HttpResponse("OK")
    except Exception as e:
        print(e)
        return HttpResponse("OK error")