# app/Dockerfile

FROM python:3.8-slim

WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

# Install pip requirements
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# copy app
COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "caesar.wsgi"]