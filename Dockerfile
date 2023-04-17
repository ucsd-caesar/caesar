# app/Dockerfile

FROM python:3.8-slim

WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
# Install dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000