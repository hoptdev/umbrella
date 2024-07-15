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