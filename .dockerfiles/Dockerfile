FROM python:3.6.7-alpine3.8

EXPOSE 5000

RUN mkdir /srv/app

COPY . /srv/app
WORKDIR /srv/app

ENV FLASK_APP=virtuagym_api/app.py
RUN apk add --update gcc make g++ openssl-dev libffi-dev
RUN pip install -r requirements/dev-requirements.txt --user

CMD python -m flask run --port 5000 --host 0.0.0.0