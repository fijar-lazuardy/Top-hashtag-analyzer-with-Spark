FROM python:3.7-alpine

COPY requirements.txt /app/

RUN cd /app \
    && pip3 install -r requirements.txt

COPY . /app

EXPOSE 8989
RUN cd /app
CMD [ "python3", "/app/tweet_stream.py" ]