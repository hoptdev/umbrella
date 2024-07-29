from django.apps import AppConfig
import threading
import asyncio

class WebhookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webhook'


    def callProcess():
        from webhook.handlers.paymentHandler.handler import Process
        asyncio.run(Process())
        
    def ready(self):
        from .handlers.courierHandlers.messageHandler import RegisterCommands, RegisterInputHandlers
        from .handlers.courierHandlers.callbackHandler import RegisterActions
        from .handlers.shopHandlers.messageHandler import RegisterCommands as RegisterCommandsShop, RegisterInputHandlers as RegisterInputHandlersShop
        from .handlers.shopHandlers.callbackHandler import RegisterActions as RegisterActionsShop
        RegisterCommands()
        RegisterActions()
        RegisterInputHandlers()

        RegisterCommandsShop()
        RegisterActionsShop()
        RegisterInputHandlersShop()
        
        #PaymentHandler.delay() todo ?
        _thread = threading.Thread(target=WebhookConfig.callProcess)
        _thread.start()