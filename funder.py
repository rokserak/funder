from typing import Awaitable, List, Optional
from bfxapi.rest.bfx_rest import BfxRest
from bfxapi.models.notification import Notification, NotificationError
from bfxapi.models.funding_offer import FundingOffer
from bfxapi.models.funding_credit import FundingCredit


class Funder:
    SYMBOL = 'fUSD' # USD funding
    MIN_FUND_OFFER = 50 # 50 USD is min amount you can offer
    RENEW_DIFF = 3 # max diff between current rate and offered rate in % so we do not renew offer

    def __init__(self, api_key: str, api_secret: str):
        self.bfx = BfxRest(api_key, api_secret)

    async def get_all_funds(self) -> Awaitable[Optional[float]]:
        """
        get all funds in funding wallet
        """
        wallets = await self.bfx.get_wallets()
        funding_wallet = filter(lambda w: w.type == 'funding' and w.currency in self.SYMBOL, wallets)
        # iterator have no len(), so just return first wallet in loop
        for fw in funding_wallet:
            return fw.balance
        return None

    async def get_funds(self) -> Awaitable[Optional[float]]:
        """
        get available funds
        """
        all_funds = await self.get_all_funds()
        if all_funds is None:
            return None
        offers = await self.get_offers()
        offered_funds = sum(o.amount for o in offers)
        provided = await self.get_provided()
        provided_funds = sum(p.amount for p in provided)
        return all_funds - offered_funds - provided_funds

    async def get_min_offer_rate(self) -> Awaitable[float]:
        """
        current min offer rate
        """
        book = await self.bfx.get_public_books(self.SYMBOL)
        return min(book, key=lambda x: x[0])[0]

    async def make_offer(self, amount: int, rate: float, period: int = 2) -> Awaitable[Optional[Notification]]:
        """
        make offer of specified amount and at specified interest rate
        """
        if amount is None or amount < self.MIN_FUND_OFFER:
            return None
        notification = await self.bfx.submit_funding_offer(self.SYMBOL, amount, rate, period)
        print('Offer made', notification)
        return notification

    async def cancel_offer(self, offer_id: int) -> Awaitable[Notification]:
        """
        cancel specified offer
        """
        notification = await self.bfx.submit_cancel_funding_offer(offer_id)
        print('Offer canceled', notification)
        return notification

    async def get_offers(self) -> Awaitable[List[FundingOffer]]:
        """
        get offered funds
        """
        return await self.bfx.get_funding_offers(self.SYMBOL)

    async def get_provided(self) -> Awaitable[List[FundingCredit]]:
        """
        get provided funds
        """
        return await self.bfx.get_funding_credits(self.SYMBOL)

    async def renew_offers(self):
        """
        renew offers whose rate is way higher that current rate
        """
        rate = await self.get_min_offer_rate()
        offers = await self.get_offers()
        for o in offers:
            if (o.rate / rate) - 1 > self.RENEW_DIFF:
                notification = await self.cancel_offer(o.id)
                if notification.status == NotificationError.SUCCESS:
                    funds = await self.get_funds()
                    notification = await self.make_offer(funds, rate)
                    if notification is not None:
                        print('Offer renewed', notification)
