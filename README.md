# Funder

Funder automates funding on Bitfinex trading platform.

Funder makes sure that we are always offering our funds at the lowest market interest rate.
We want the loan rate to be the lowest so our funds are provided as soon as possible.
The main reason for that is because dividends on Bitfinex are being paid daily, which gives us compound
interest rates, by adding dividends to our funds daily, that can be offer immediately.

Bitfinex already offers similar feature called `Auto-renew` feature, but it uses `FFR` as interest rate, that is
often way above market, which makes your funds just sit on your account sometimes for whole days, not earning
any dividends.

## Usage

### Development with pipenv

First make sure you create `.env` file with API key and secret, check `.env.example` for necessary variables.

```sh
pipenv install
pipenv shell
python main.py
```

### Development with docker-compose

Make sure to add API key and secret to `Dockerfile`.

```sh
docker-compose build
docker-compose up -d
docker-compose exec funder bash
python main.py
```


### Deployment

Make sure to add API key and secret to `Dockerfile` and uncomment last line.

```sh
docker build -t funder .
docker run --detach --restart unless-stopped funder
```
