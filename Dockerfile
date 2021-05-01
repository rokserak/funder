FROM python:3.10-rc-buster
ENV PYTHONUNBUFFERED 1

ENV API_KEY=your_api_key
ENV API_SECRET=your_api_secret

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# uncomment when running container without docker-compose
#CMD [ "python", "./main.py" ]
