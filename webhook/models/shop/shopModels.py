from django.db import models
from .userModels import *
from asgiref.sync import sync_to_async

class Status(models.TextChoices):
    ONSALE = 'OnSale', 'On Sale'
    SOLD = 'Sold', 'Sold'

class OrderStatus(models.TextChoices):
    COMPLETED = 'Completed', 'Completed'
    WAIT = 'Wait', 'Wait'

class Type(models.TextChoices):
    PREORDER = 'PreOrder', 'Pre Order'
    MOMENT = 'Moment', 'Moment'

class PackChoice(models.TextChoices):
    PROMO = 'PROMO', 'Promo'
    GR05 = '0.5 гр.', '0.5 гр.'
    GR1 = '1 гр.', '1 гр.'
    GR2 = '2 гр.', '2 гр.'
    GR3 = '3 гр.', '3 гр.'
    GR4 = '4 гр.', '4 гр.'
    GR5 = '5 гр.', '5 гр.'
    GR10 = '10 гр.', '10 гр.'
    GR20 = '20 гр.', '20 гр.'

class Product(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=2048, blank=True, null=True) #составляется автоматически из набора главных характеристик категории???
    photo1 = models.ImageField(upload_to ='uploadsProduct/') 
    photo2 = models.ImageField(upload_to ='uploadsProduct/') 

#добавить штрафы
class Pack(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=256, choices=PackChoice.choices, default=PackChoice.GR05, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=100)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    type = models.CharField(max_length=64, choices=Type.choices, default=Type.MOMENT)

class City(models.Model):
    title = models.CharField(max_length=256)

    async def getAsync(*args, **kwargs):
        return await City.objects.aget(**kwargs)

class Shop(models.Model):
    title = models.CharField(max_length=256)
    city = models.ManyToManyField(City, blank=True, null=True)

    @sync_to_async
    def getAllAsync(*args, **kwargs):
        return Shop.objects.filter(**kwargs)
    
    @sync_to_async
    def getFirstAsync(*args, **kwargs):
        return Shop.objects.filter(**kwargs).first()

class Partner(models.Model):
    title = models.CharField(max_length=128)
    tgId = models.IntegerField()
    tgLogin = models.CharField(max_length=1024)
    role = models.CharField(max_length=64, choices=Role.choices, default=Role.DEFAULT)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    @sync_to_async
    def getAllAsync(*args, **kwargs):
        return Partner.objects.filter(**kwargs)
    
    @sync_to_async
    def getFirstAsync(*args, **kwargs):
        return Partner.objects.filter(**kwargs).first()
    
    async def getAsync(*args, **kwargs):
        return await Partner.objects.aget(**kwargs)

class Area(models.Model):
    title = models.CharField(max_length=256)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    photo1 = models.ImageField(upload_to='uploadsArea/')
    photo2 = models.ImageField(upload_to='uploadsArea/')

class Address(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    fromPartner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    data = models.CharField(max_length=2048)
    status = models.CharField(max_length=64, choices=Status.choices, default=Status.ONSALE)

class PreOrderInfo(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

class Order(models.Model):
    status = models.CharField(max_length=64, choices=OrderStatus.choices, default=OrderStatus.WAIT)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    create_time = models.DateTimeField(auto_now_add=True)