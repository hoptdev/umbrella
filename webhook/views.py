from .handlers.courierHandlers.messageHandler import *

from django.http import HttpResponse
from webhook.models.telegram.models import TelegramBot
from django.views.decorators.csrf import csrf_exempt
from umbrella.celery import app
import asyncio
import threading
from webhook.models.telegram.updateModels import *

from .handlers.courierHandlers.messageHandler import *
from .handlers.courierHandlers.callbackHandler import *

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def HandleUpdate(body, botId):
    bot = await TelegramBot.objects.aget(id=botId)
    update = Update(body)

    if update.message:
        await HandleMessage(bot, update.message)
    elif update.callback_query:
        await HandleCallback(bot, update.callback_query)
    return

@app.task(ignore_result=True)
def RunHandleUpdate(body, botId):
    asyncio.get_event_loop().run_until_complete((HandleUpdate(body, botId)))

def process_request_thread(req, botId):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(HandleUpdate(req, botId))

@csrf_exempt
def webhook(request, botId):
    try:
        if request.method == "POST":
            thread = threading.Thread(target=process_request_thread(request.body, botId))
            thread.start()

            #RunHandleUpdate.delay(request.body, botId)
        return HttpResponse("OK")
    except Exception as e:
        print(e)
        return HttpResponse("OK error")
