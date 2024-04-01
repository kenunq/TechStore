FROM python:3.11

RUN apt-get update && apt-get install -y ncat

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /TechStore
WORKDIR /TechStore

COPY requirements.txt /TechStore/

RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /TechStore/
