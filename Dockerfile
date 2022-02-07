FROM python:3.10.1-slim
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y wget gnupg2
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main" > /etc/apt/sources.list.d/postgresql.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update && apt-get upgrade && apt install -y postgresql-14 gcc python3-dev libpq-dev

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
