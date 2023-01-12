from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import certifi
ca = certifi.where()

from pymongo import MongoClient
client = MongoClient("mongodb+srv://bongdroid:qhdrbs88!@cluster0.hecgbmx.mongodb.net/Cluster0?retryWrites=true&w=majority", tlsCAFile = ca)

db = client.pracdb

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc = {
        'num':count,
        'bucket':bucket_receive,
        'done':0
    }
    db.bucket.insert_one(doc)

    return jsonify({'msg': '리스트 등록 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done':1}})

    return jsonify({'msg': '버킷 완료!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))

    return jsonify({'buckets': bucket_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)