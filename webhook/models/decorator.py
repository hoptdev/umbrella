from asgiref.sync import sync_to_async
from django.db import models

def async_model_decorator(cls):
    async def afilter(*args, **kwargs):
        return await sync_to_async(list)(cls.objects.filter(**kwargs))

    async def afirst(*args, **kwargs):
        return await sync_to_async(lambda: cls.objects.filter(**kwargs).first())()
    
    async def aget(*args, **kwargs):
        return await cls.objects.aget(**kwargs)

    cls.afilter = afilter
    cls.afirst = afirst
    cls.aget = aget

    return cls

def register_callback(botType):
    from ..handlers.callbackHandler import callbackActions
    def decorator(cls):
        return register(botType, cls, callbackActions)
    return decorator

def register_command(botType):
    from ..handlers.messageHandler import commandActions
    def decorator(cls):
        return register(botType, cls, commandActions)
    return decorator

def register_input(botType):
    from ..handlers.messageHandler import inputActions 
    def decorator(cls):
        return register(botType, cls, inputActions)
    return decorator

def register(botType, cls, dictionary : dict):
    if not dictionary.get(botType):
        dictionary[botType] = {}
    dictionary[botType][cls.data] = cls
    return cls