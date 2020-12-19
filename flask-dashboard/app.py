from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import os
import json
app = Flask(__name__)


username = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
password = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
client = MongoClient('mongodb://%s:%s@35.226.114.12:27017/' % (username, password))

db = client['tweets']

@app.route('/')
def index():
    data = {}
    collection = db['positive']
    # Fetch data from mongodb here
    print(client)
    item = collection.insert_one({
        "tweet": "This is an example tweet"
    })
    return render_template('index.html', data=data)

@app.route('/fetch-data')
def fetch_data():
    return 0


@app.route('/update-data', methods=['POST'])
def update_data():
    global db
    files = request.json()
    collection = db['tweets']
    print(files)
    collection.update({
        "halo":"hai"
    }, upsert=True)
    jsonify(
        message="Halo, kamu pasti capek ngoding"
    )

if __name__ == "__main__":
    app.run(port=5000)