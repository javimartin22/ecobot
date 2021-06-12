import flask
from flask import request, jsonify
import json
import datetime
import time
import pymongo
import sys

app = flask.Flask(__name__)
db_url="mongodb://host.docker.internal:27017/"



@app.route('/log', methods=['POST'])
def log():
    data = request.json
    myclient = pymongo.MongoClient(db_url)
    mydb = myclient["QR_DATA"]
    mycol = mydb["QR_LOGS"]
    mycol.insert_one(data)
    return 'Done'

@app.route('/saveUser', methods=['POST'])
def saveUser():
    data = request.json
    key = {'chat_id':data['chat_id']}
    update={ "$set" : data }
    myclient = pymongo.MongoClient(db_url)
    mydb = myclient["QR_DATA"]
    mycol = mydb["USERS"]
    mycol.update(key, update, upsert=True);
    return 'Done'

@app.route('/saveAnswer', methods=['POST'])
def saveAnswer():
    data = request.json
    key = {'chat_id':data['chat_id']}
    myclient = pymongo.MongoClient(db_url)
    mydb = myclient["QR_DATA"]
    mycol = mydb["ANSWERS"]
    mycol.insert_one(data)
    return 'Done'

@app.route('/saveTextAnswer', methods=['POST'])
def saveTextAnswer():
    data = request.json
    key = {'chat_id':data['chat_id']}
    myclient = pymongo.MongoClient(db_url)
    mydb = myclient["QR_DATA"]
    mycol = mydb["USERS"]
    user = mycol.find(key)
    update=data
    update['question']=user[0]['last-question']
    ANSWERS = mydb["ANSWERS"]
    ANSWERS.insert_one(update);
    return 'Done'

app.run(host='0.0.0.0',port=5003)
