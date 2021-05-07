import math
from typing import List, Optional
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

    async def get_all_funds(self) -> float:
        """
        get all funds in funding wallet
        """
        wallets = await self.bfx.get_wallets()
        wallet_type = 'funding'
        funding_wallet = filter(lambda w: w.type == wallet_type and w.currency in self.SYMBOL, wallets)
        return next(funding_wallet).balance

    async def get_funds(self) -> float:
        """
        get available funds
        """
        api_route = 'auth/calc/order/avail'
        offer_type = 'FUNDING'
        funds = await self.bfx.post(api_route, dict(symbol=self.SYMBOL,
                                                    type=offer_type))

        def truncate(number: float, digits: int) -> float:
            stepper = 10.0 ** digits
            return math.trunc(stepper * number) / stepper

        funds = abs(funds[0])
        # Bitfinex likes to round numbers up which sucks when order amount is 0.000001 to high
        return truncate(funds, 5)

    async def get_min_offer_rate(self) -> float:
        """
        current min offer rate
        """
        book = await self.bfx.get_public_books(self.SYMBOL)
        return min(book, key=lambda x: x[0])[0]

    async def make_offer(self, amount: float, rate: float, period: int=2) -> Optional[Notification]:
        """
        make offer of specified amount and at specified interest rate
        """
        if amount is None or amount < self.MIN_FUND_OFFER:
            return None
        return await self.bfx.submit_funding_offer(self.SYMBOL, amount, rate, period)

    async def cancel_offer(self, offer_id: int) -> Notification:
        """
        cancel specified offer
        """
        return await self.bfx.submit_cancel_funding_offer(offer_id)

    async def get_offers(self) -> List[FundingOffer]:
        """
        get offered funds
        """
        return await self.bfx.get_funding_offers(self.SYMBOL)

    async def get_provided(self) -> List[FundingCredit]:
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
                    await self.make_offer(funds, rate)
