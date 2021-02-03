from typing import Awaitable, List, Optional
from bfxapi.rest.bfx_rest import BfxRest
from bfxapi.models.notification import Notification, NotificationError
from bfxapi.models.funding_offer import FundingOffer

class Funder:
  def __init__(self, api_key: str, api_secret: str, symbol: str):
    self.btx = BfxRest(api_key, api_secret)
    self.symbol = symbol
  
  async def get_funds(self) -> Awaitable[Optional[float]]:
    wallets = await self.btx.get_wallets()
    funding_wallet = filter(lambda w: w.type == 'funding' and w.currency in self.symbol, wallets)
    # iterator have no len(), so just return first wallet in loop
    for fw in funding_wallet:
      return fw.balance
    return None

  async def get_min_offer(self) -> Awaitable[List]:
    book = await self.btx.get_public_books(self.symbol)
    # (ORDER_ID, PERIOD, RATE, AMOUNT)
    return min(book, key=lambda x: x[0])
  
  async def make_offer(self, amount: int, rate: float, period: int = 2) -> Awaitable[Notification]:
    notification = await self.btx.submit_funding_offer(self.symbol, amount, rate, period)
    if notification.status != NotificationError.SUCCESS:
      notification = await self.make_offer(amount, rate, period)
    return notification
  
  async def cancel_offer(self, offer_id: int) -> Awaitable[Notification]:
    notification = await self.btx.submit_cancel_funding_offer(offer_id)
    if notification.status != NotificationError.SUCCESS:
      notification = await self.cancel_offer(offer_id)
    return notification

  async def get_offers(self) -> Awaitable[List[FundingOffer]]:
    return await self.btx.get_funding_offers(self.symbol)
