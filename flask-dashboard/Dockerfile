FROM python:3.7-alpine

COPY requirements.txt /app/

RUN cd /app \
    && pip3 install -r requirements.txt

COPY . /app

ENV FLASK_APP=app.py

ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

WORKDIR /app

CMD [ "flask", "run" ]