import os
import asyncio
from bfxapi.rest.bfx_rest import BfxRest

print('api key =', os.getenv('API_KEY'))
print('api secret =', os.getenv('API_SECRET'))

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
if api_key is None or api_secret is None:
  print('missing env variables API_KEY and API_SECRET')
  exit(1)

symbol = 'fUSD'

async def get_loan():
  btx = BfxRest(api_key, api_secret, logLevel='DEBUG')
  loans = await btx.get_funding_credits(symbol=symbol)
  print(loans[0])

asyncio.run(get_loan())
