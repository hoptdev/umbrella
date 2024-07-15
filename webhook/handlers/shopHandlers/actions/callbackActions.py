from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from webhook.models.shop.shopModels import *
from webhook.models.shop.userModels import *
# callbackData example: my_data, data_test_arg1 etc.. 

class ShopView:
    data = "shop_view"
    role = Role.DEFAULT

    async def Action(bot: TelegramBot, callback: CallbackQuery, p: Partner, args=None):
        pass