import os
import asyncio
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
    print('Available funds', funds)

    rate = await funder.get_min_offer_rate()
    print('Min offer rate', rate)

    status = await funder.make_offer(funds, rate)
    print('Offer made', status)

    offers = await funder.get_offers()
    for i, o in enumerate(offers):
      print('Offer', i, o)

    provided = await funder.get_provided()
    for i, p in enumerate(provided):
      print('Provided', i, p)

    await funder.renew_offers()
    await asyncio.sleep(60)

if __name__ == '__main__':
  asyncio.run(main())
