import os
import asyncio
from src.funder import Funder

print('api key =', os.getenv('API_KEY'))
print('api secret =', os.getenv('API_SECRET'))

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
if api_key is None or api_secret is None:
  print('missing env variables API_KEY and API_SECRET')
  exit(1)

symbol = 'fUSD'

async def main():
  funder = Funder(api_key, api_secret, symbol)
  offer = await funder.get_min_offer()
  print('offer', offer)

  offers = await funder.get_offers()
  for i, o in enumerate(offers):
    print('offer', i, o)

  wallet = await funder.get_funds()
  print(wallet)

if __name__ == '__main__':
  asyncio.run(main())
