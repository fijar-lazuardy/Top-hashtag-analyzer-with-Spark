import requests
import time
import random
import json


def get_random_number():
    return random.randint(0, 2000)


def main():
    while True:
        body = {
            "#indonesiajuara": get_random_number(),
            "#shopee1212": get_random_number(),
            "#demonslayermovie": get_random_number(),
            "#apadehbingung": get_random_number(),
            "#animeindo": get_random_number(),
            "#tokopediabts": get_random_number(),
            "#attackontitanfinalseason": get_random_number(),
            "#lazada1212": get_random_number(),
            "#haikyuufinal": get_random_number(),
            "#blackpinkcomeback2021": get_random_number()
        }
        try:
            requests.post(
                "http://127.0.0.1:5000/update-data", json=body)
            print("success")
        except Exception as e:
            print(e)
            print("failed")
        time.sleep(1)


if __name__ == "__main__":
    main()
