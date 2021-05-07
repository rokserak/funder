import os
import asyncio
from datetime import datetime
from funder import Funder


async def main():
    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('API_SECRET')
    if api_key is None or api_secret is None:
        print('missing env variables API_KEY and API_SECRET')
        exit(1)

    funder = Funder(api_key, api_secret)
    while True:
        funds = await funder.get_funds()
        rate = await funder.get_min_offer_rate()
        status = await funder.make_offer(funds, rate)
        if status is not None:
            print(datetime.now(), 'Offer made', status)

        await funder.renew_offers()
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
