from django.apps import AppConfig
import asyncio

def SetWebhooks():
    from webhook.models.telegram.models import TelegramBot
    bots = TelegramBot.objects.all()

    for bot in bots:
        asyncio.run(bot.setWebhook())

class WebhookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webhook'

    def ready(self):
        from .handlers.courierHandlers.messageHandler import RegisterCommands
        from .handlers.courierHandlers.callbackHandler import RegisterActions
        SetWebhooks()
        RegisterCommands()
        RegisterActions()