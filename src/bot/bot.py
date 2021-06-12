#Telegram
from telegram import *
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Librerias del sistema
import os

from io import BytesIO
from random import randint
import json
import datetime

import requests

log_url = 'http://192.168.50.10:5003/log'
user_save_url = 'http://192.168.50.10:5003/saveUser'
answer_save_url = 'http://192.168.50.10:5003/saveAnswer'
text_answer_save_url = 'http://192.168.50.10:5003/saveTextAnswer'
qr_decode_url = 'http://192.168.50.11:5001/qr_decode'
ques_url = 'http://192.168.50.12:5002/getQuestion'


TOKEN = "1673875747:AAFOY1F-tLAt_rFHnX4UskdKN5HwcZNrgzo"

def image_handler(update: Update, context: CallbackContext):
        #Comprobacion si el mensaje contiene imagen
        if update.message.photo:
                id_img = update.message.photo[-1].file_id
        else:
                return

        #Obtener datos usuario
        chat_id = update.message.chat_id
        first_name = update.message.chat.first_name
        last_name = update.message.chat.last_name
        username = update.message.chat.username

        #Descarga imagen
        img = context.bot.getFile(id_img)
        img_file = context.bot.get_file(img.file_id)
        img_filename='images/'+str(chat_id)+'.png'
        img_file.download(img_filename)
        
        #Envio confirmacion de recepcion de imagen al usuario
        context.bot.sendMessage(chat_id=chat_id, text="Decodificando, espera por favor...")

        #Envio de imagen a la API del escanerQR
        files = {'file': open(img_filename,'rb')}
        res = requests.post(qr_decode_url, files=files)
        data=json.loads(res.text) #datos obtenidos a partir del escaneo del QR

        #Añadir datos del usuario a los datos obtenidos del QR
        data['time']=str(datetime.datetime.now())
        data['chat_id']=chat_id
        data['first_name']=first_name
        data['last_name']=last_name
        data['username']=username
        print(data)

        #Envio de datos a la API de gestor de datos y respuesta
        res = requests.post(log_url, json = data)
        print("Respuesta API gestor datos:",res.text)
        
        #Envio de datos a la API del motor de reglas-envio de pregunta
        try:
                res = requests.post(ques_url, json = data)
                print("Respuesta API envio pregunta:",res.text)
        except:
                print(sys.exec_info())

        

        
def setup(update: Update, context: CallbackContext):
        print("Starting Setup...")
        keyboard=[[InlineKeyboardButton("Select English as my default language", callback_data='set-lang-eng')],
                  [InlineKeyboardButton("Seleccione Español como mi idioma predeterminado", callback_data='set-lang-esp')],
                  [InlineKeyboardButton("Aukeratu Euskara nire hizkuntza lehenetsi gisa", callback_data='set-lang-eusk')]
                  ]
        first_msg="Language Setup:"
        context.bot.sendMessage(chat_id=update.effective_chat.id,text=first_msg,reply_markup=InlineKeyboardMarkup(keyboard))
        
def saveTextAnswer(update: Update, context: CallbackContext):
        print("Answer received...")
        print(update)
        try:
                dataToBeSaved={"chat_id":update.message.chat.id,
                               "answer":update.message.text,
                               "time":str(datetime.datetime.now())}
                res = requests.post(text_answer_save_url, json = dataToBeSaved)
                print("Answer Save Response:",res.text)
        except:
                print("Can't Save Answer")
        context.bot.sendMessage(chat_id=update.effective_chat.id,text="Thanks for feedback!")

        
def setLanguage(update: Update, context: CallbackContext):
        print("Setting Language...")
        query = update.callback_query
        query.answer()
        choice = query.data
        print(query)
        chat_id=query.message.chat.id
        if query.message.chat.first_name:
                first_name=query.message.chat.first_name
        else:
                first_name=""

        if query.message.chat.last_name:
                last_name=query.message.chat.last_name
        else:
                last_name=""
        
        if query.message.chat.username:
                username=query.message.chat.username
        else:
                username=""
        
        user={"chat_id":chat_id,
              "first_name":first_name,
              "last_name":last_name,
              "username":username
              }
        if choice == "set-lang-eng":
                reply_msg="Welcome "+first_name+" "+last_name+"!\nEnglish is your default language now.\nThis is Javi's QR Bot.\nPlease send a photo of QR code to me.\nSelect /langSetup to change language."
                user['language']='eng'
        elif choice == "set-lang-esp":
                reply_msg="Bienvenidos "+first_name+" "+last_name+"!\nEl español es su idioma predeterminado ahora.\nEste es el QR bot de Javi.\nPor favor envíeme una foto del código QR.\nSeleccione /langSetup para cambiar el idioma."
                user['language']='esp'
        elif choice == "set-lang-eusk":
                reply_msg="Ongi etorri "+first_name+" "+last_name+"!\nEuskara da zure hizkuntza lehenetsia orain.\nHau da javiren QR bot-a.\nMesedez, bidali QR kodearen argazkia.\nAukeratu /langSetup hizkuntza aldatzeko."
                user['language']='eusk'
        user['last-question']='none'
        try:
                res = requests.post(user_save_url, json = user)
                print("Add User Response:",res.text)
        except:
                print("Can't add user")

        context.bot.sendMessage(chat_id=update.effective_chat.id,text=reply_msg)
        
def saveAnswer(update: Update, context: CallbackContext):
        print("Saving Answer...")
        query = update.callback_query
        query.answer()
        data = query.data
        postID=data.split(":::")[1]
        answer=data.split(":::")[2]
        dataToBeSaved={"chat_id":query.message.chat.id,
                       "postID":postID,
                       "answer":answer,
                       "time":str(datetime.datetime.now())}
        try:
                res = requests.post(answer_save_url, json = dataToBeSaved)
                print("Answer Save Response:",res.text)
        except:
                print("Can't add user")
        context.bot.sendMessage(chat_id=update.effective_chat.id,text="Feedback recibido")
        
def main():
        bot=Bot(TOKEN)
        updater = Updater(TOKEN, request_kwargs={'read_timeout': 20, 'connect_timeout': 20}, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(MessageHandler(Filters.photo, image_handler))
        dp.add_handler(CommandHandler("start", setup))
        dp.add_handler(CommandHandler("langSetup", setup))
        dp.add_handler(CallbackQueryHandler(setLanguage, pattern='^set-lang-'))
        dp.add_handler(CallbackQueryHandler(saveAnswer, pattern='^update:::'))
        dp.add_handler(MessageHandler(Filters.text, saveTextAnswer))


        updater.start_polling()
        updater.idle()

if __name__ == '__main__':
        main()
        print("done")
