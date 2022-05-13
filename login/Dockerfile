# syntax=docker/dockerfile:1
FROM ubuntu:latest
WORKDIR /code
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev git \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .