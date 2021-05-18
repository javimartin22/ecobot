from kraken import binarization

from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol

from PIL import Image,ImageEnhance

import flask
from flask import request, jsonify
import json
import datetime
import time
import sys
import os

app = flask.Flask(__name__)
UPLOAD_FOLDER = 'images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/qr_decode', methods=['POST'])
def QR_decode():
    try:
        file = request.files['file']
        filename = file.filename
        print("Saving :",filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        result=[]
        img=Image.open(UPLOAD_FOLDER+filename)
        result.append(decode(img))
        bw_im = binarization.nlbin(img,zoom=0.5) #1.binarizacion
        result.append(decode(bw_im, symbols=[ZBarSymbol.QRCODE]))
        imgb = ImageEnhance.Brightness(img).enhance(2.0)#2.aumentar brillo
        result.append(decode(imgb))
        imgc = ImageEnhance.Contrast(img).enhance(3.0)#3.aumentar contraste
        result.append(decode(imgc))
        imgs = ImageEnhance.Sharpness(img).enhance(17.0)#4.sharp turn
        result.append(decode(imgs))
        img = imgc.convert('L') #5.convertir escala de grises
        result.append(decode(img))
        result = decode(img)
        print(result)
        if len(result)>0:
            return result[0].data.decode("utf-8").lower()
        else:
            return None
    except:
        print(sys.exc_info())
        return None
    return None

app.run(host='0.0.0.0',port=5001)
