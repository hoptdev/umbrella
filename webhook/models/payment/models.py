from django.db import models
from ..decorator import async_model_decorator

from ..shop.shopModels import Partner
from ...handlers.paymentHandler.btcHelper import getKey
from ...handlers.paymentHandler.ltcHelper import createFullKey

class PaymentType(models.TextChoices):
    PAYMENT = 'PAYMENT', 'Payment'
    FUNDING = 'FUNDING', 'Funding'
    COMPENSATION = 'COMPENSATION', 'Compensation'

class Cryptocurrency(models.TextChoices):
    BTC = 'BTC', 'BTC'
    LTC = 'LTC', 'LTC'

class AddBalance(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=64, choices=PaymentType.choices)
    source = models.CharField(max_length=1024)

@async_model_decorator
class Wallet(models.Model):
    title = models.CharField(max_length=64, choices=Cryptocurrency.choices)
    publicKey = models.CharField(max_length=1024)
    privateKey = models.CharField(max_length=1024)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)

    async def createForPartnerAsync(self, partner, type : Cryptocurrency):
        self.title = type
        self.partner = partner
        if type is Cryptocurrency.BTC:
            data = getKey()
            self.publicKey = data[0]
            self.privateKey = data[1]

            await self.asave()
        elif type is Cryptocurrency.LTC:
            data = createFullKey(partner.id)
            self.publicKey = data[0]
            self.privateKey = data[1]
            await self.asave()
        else:
            pass