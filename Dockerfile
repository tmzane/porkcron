FROM python:3.10-alpine
WORKDIR /app

COPY script.py .
COPY crontab /etc/crontabs/root

CMD [ "crond", "-f" ]
