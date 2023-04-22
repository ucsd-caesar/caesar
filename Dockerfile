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

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Adds permissions for entrypoint to execute on start
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod u+x entrypoint.sh
CMD [ "./entrypoint.sh" ]