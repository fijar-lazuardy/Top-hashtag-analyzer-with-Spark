import requests
import os
import json
from dotenv import load_dotenv, find_dotenv
import socket
import sys
import time
# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        print(headers)
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "context:54.* has:hashtags -is:retweet lang:in", "tag": "musican with hashtag tweeted in indonesian"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(headers, set, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,
    )
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    # for response_line in response.iter_lines():
    #     if response_line:
    #         json_response = json.loads(response_line)
    #         print(json.dumps(json_response, indent=4, sort_keys=True))
    return response

def send_tweets_to_spark(http_resp, tcp_connection):
    for line in http_resp.iter_lines():
        try:
            full_tweet = json.loads(line)
            print('masuk sini')
            # print(json.dumps(full_tweet['data']['text'], indent=4, sort_keys=True))
            # tweet_text = full_tweet['data']['text'].encode("utf-8") + '\n' # pyspark can't accept stream, add '\n'
            tweet_text = full_tweet['data']['text'] # pyspark can't accept stream, add '\n'
            print('Tweet: ' + tweet_text)
            print(type(tweet_text))

            # print("Tweet Text: " + tweet_text.decode())

            print ("------------------------------------------")
            tcp_connection.send(tweet_text.encode('utf-8'))
            print("------ KALO BERHASIL MASUK SINI-------")
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e.__str__)

def main():
    load_dotenv(find_dotenv())
    bearer_token = os.environ.get("BEARER_TOKEN")
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set_rule = set_rules(headers, delete, bearer_token)
    # TCP_IP = "localhost"
    TCP_PORT = 5678
    conn = None
    s = socket.socket()
    s.bind(('0.0.0.0', TCP_PORT))
    s.listen(1)
    print("Waiting for TCP connection...")
    conn, addr = s.accept()

    while True:
        print("Connected... Starting getting tweets.")
        resp = get_stream(headers, set_rule, bearer_token)
        send_tweets_to_spark(resp, conn)
        time.sleep(5)


if __name__ == "__main__":
    main()
