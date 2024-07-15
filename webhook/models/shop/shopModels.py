from django.db import models
from .userModels import *
from ..decorator import async_model_decorator

class Status(models.TextChoices):
    ONSALE = 'OnSale', 'On Sale'
    SOLD = 'Sold', 'Sold'

class OrderStatus(models.TextChoices):
    COMPLETED = 'Completed', 'Completed'
    WAIT = 'Wait', 'Wait'

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

@async_model_decorator
class City(models.Model):
    title = models.CharField(max_length=256)
    
@async_model_decorator
class Shop(models.Model):
    title = models.CharField(max_length=256)
    city = models.ManyToManyField(City, blank=True, null=True)

@async_model_decorator
class Product(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=2048, blank=True, null=True) #составляется автоматически из набора главных характеристик категории???
    photo1 = models.ImageField(upload_to ='uploadsProduct/') 
    photo2 = models.ImageField(upload_to ='uploadsProduct/') 
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

#todo: добавить штрафы
@async_model_decorator
class Pack(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=256, choices=PackChoice.choices, default=PackChoice.GR05, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=100)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    preorder = models.BooleanField(default=False)

@async_model_decorator
class Partner(models.Model):
    title = models.CharField(max_length=128)
    tgId = models.IntegerField()
    tgLogin = models.CharField(max_length=1024)
    role = models.CharField(max_length=64, choices=Role.choices, default=Role.DEFAULT)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0) #usd <- btc/ltc 

@async_model_decorator
class Area(models.Model):
    title = models.CharField(max_length=256)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    photo1 = models.ImageField(upload_to='uploadsArea/')
    photo2 = models.ImageField(upload_to='uploadsArea/')

@async_model_decorator
class Address(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    fromPartner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    data = models.CharField(max_length=2048)
    status = models.CharField(max_length=64, choices=Status.choices, default=Status.ONSALE)
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)

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