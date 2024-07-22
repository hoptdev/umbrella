from webhook.models.telegram.updateModels import *
from webhook.models.telegram.models import *
from .actions.callbackActions import *
import re

pattern = r"(([^_]+)_([^_]+))_(.*)"

actions = {}

async def HandleCallback(bot: TelegramBot, query: CallbackQuery):
    action = next((v for k, v in actions.items() if query.data.startswith(k)), {})
    if not action:
        return
    
    match = re.match(pattern,query.data)
    if match:
        args = match.group(4).split("_")
    else:
        args = []

    p = await Partner.afirst(tgId = query.from_user.id, shop_id=bot.shop_id)

    if p and ROLE_LEVELS[Role(p.role)] >= ROLE_LEVELS[action.role]:
        await action.Action(bot, query, p, args)
    else:
        await bot.sendMessageAsync(query.chat.id, "У вас нет прав")
    return

def RegisterActions():
    global actions
    actions = {
        ShopSelectCity.data: ShopSelectCity,
        ShopView.data: ShopView,
        ShopProductInfo.data: ShopProductInfo,
        ShopSelectProduct.data: ShopSelectProduct,
        ShopSelectPack.data: ShopSelectPack,
        ShopSelectArea.data: ShopSelectArea,
        ShopBuyConfirm.data: ShopBuyConfirm,
        AddressPhotoView.data: AddressPhotoView,
        PartnerHistoryView.data: PartnerHistoryView,
        OrderInfoView.data: OrderInfoView,
        PaymentInfoView.data: PaymentInfoView
    }
    return
