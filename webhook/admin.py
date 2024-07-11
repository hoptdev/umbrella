from django.contrib import admin
from .models.telegram.models import TelegramBot
from .models.shop.shopModels import *

# Register your models here.
admin.site.register(TelegramBot)

admin.site.register(Product)
admin.site.register(Pack)
admin.site.register(City)
admin.site.register(Shop)
admin.site.register(Partner)
admin.site.register(Area)
admin.site.register(Address)
admin.site.register(PreOrderInfo)
admin.site.register(Order)