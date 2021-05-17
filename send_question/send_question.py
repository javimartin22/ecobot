import flask
from flask import request, jsonify
import json
import datetime
import time
import pymongo
import bot_rules as durTest
import sys

app = flask.Flask(__name__)

@app.route('/getQuestion', methods=['POST'])
def getQuestion():
    try:
        json_command = request.json
        json_command['type']=json_command['tipo_de_electrodoméstico']
        durTest.post('time', json_command)
        durTest.post('electronics', json_command)
    except Exception as e:
        print("Error:",e)
        print(sys.exc_info())
    return 'done'

app.run(host='0.0.0.0',port=5002)
