from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import os
import json
app = Flask(__name__)


username = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
password = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
#client = MongoClient('mongodb://127.0.0.1:27017/')
client = MongoClient('mongodb://mongo:pdbtim7@34.70.144.224:27017/')

db = client['tweets']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    collection = db['tweets']
    result = collection.find_one({
        "_id": 1
    })
    return jsonify(
        result
    )


@app.route('/update-data', methods=['POST'])
def update_data():
    global db
    files = request.get_json()
    collection = db['tweets']
    result = []
    for k, v in files.items():
        result.append({k: v})
    updates = {
        "$set": {
            "data": result
        }
    }
    collection.update_many({"_id": 1}, updates, upsert=True)
    return jsonify(
        message="Halo, kamu pasti capek ngoding"
    )


@app.route('/test-db', methods=['GET'])
def test_conn():
    global db
    collection = db['test']
    collection.insert_one({'text': 'This is just a test'})
    return jsonify(
        message='Test success'
    )


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=5000)
