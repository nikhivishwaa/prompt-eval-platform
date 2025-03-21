FROM python:3.11.1-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential
    
RUN mkdir -p /home/app

WORKDIR /home/app

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8080

COPY aichallenge .

ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8080"]

