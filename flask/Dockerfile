FROM python:alpine3.7

LABEL author="Tom Burge"
LABEL author_email="tburge@vmware.com"

ENV REDIS_HOST redis
ENV REDIS_PORT 6379

COPY . /app
WORKDIR /app

RUN apk update && apk add bash && rm -rf /var/cache/apk/*
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD bash ./wrapper.sh

