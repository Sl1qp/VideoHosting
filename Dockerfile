FROM python:3.12-alpine

COPY requirements.txt /tmp/requirements.txt
COPY videohosting /videohosting
WORKDIR /videohosting
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /tmp/requirements.txt

RUN adduser --disabled-password app-user

USER app-user
