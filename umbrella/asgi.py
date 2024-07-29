"""
ASGI config for umbrella project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

def SetWebhooks():
    from webhook.models.telegram.models import TelegramBot
    bots = TelegramBot.objects.all()

    for bot in bots:
        print(f'set webhook for {bot.id}')
        bot.setWebhook()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'umbrella.settings')

application = get_asgi_application()

SetWebhooks()
