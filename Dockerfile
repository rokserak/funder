FROM python:3.8.7-buster

ENV API_KEY=your_api_key
ENV API_SECRET=your_api_secret

WORKDIR /usr/src/app

COPY . .

RUN pip install pipenv
RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]
