from django.apps import AppConfig
import threading
import asyncio
from dotenv import load_dotenv, dotenv_values

class WebhookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webhook'

    def callProcess():
        from webhook.handlers.paymentHandler.handler import Process
        asyncio.run(Process())
        
    def ready(self):
        from .handlers.init import init
        init()
        
        #PaymentHandler.delay() celery
        _thread = threading.Thread(target=WebhookConfig.callProcess)
        _thread.start()