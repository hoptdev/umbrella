from django.apps import AppConfig

def SetWebhooks():
    from webhook.models.telegram.models import TelegramBot
    bots = TelegramBot.objects.all()

    for bot in bots:
        bot.setWebhook()

class WebhookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webhook'

    def ready(self):
        from .handlers.courierHandlers.messageHandler import RegisterCommands, RegisterInputHandlers
        from .handlers.courierHandlers.callbackHandler import RegisterActions
        from webhook.handlers.paymentHandler.handler import PaymentHandler
        from .handlers.shopHandlers.messageHandler import RegisterCommands as RegisterCommandsShop, RegisterInputHandlers as RegisterInputHandlersShop
        from .handlers.shopHandlers.callbackHandler import RegisterActions as RegisterActionsShop
        SetWebhooks()
        RegisterCommands()
        RegisterActions()
        RegisterInputHandlers()

        RegisterCommandsShop()
        RegisterActionsShop()
        RegisterInputHandlersShop()
        
        PaymentHandler.delay()