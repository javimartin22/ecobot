from durable.lang import *
import pymongo
import random
import sys

from telegram import *
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import time

TOKEN = "1673875747:AAFOY1F-tLAt_rFHnX4UskdKN5HwcZNrgzo"

myclient = pymongo.MongoClient("mongodb://host.docker.internal:27017/")
QR_DATA = myclient["QR_DATA"]
QUESTIONS = QR_DATA["QUESTIONS"]
USERS = QR_DATA["USERS"]

bot=Bot(TOKEN)
updater = Updater(TOKEN, request_kwargs={'read_timeout': 20, 'connect_timeout': 20}, use_context=True)
dp = updater.dispatcher

state='green'

time_now=datetime.datetime.now()
today08 = time_now.replace(hour=8, minute=0, second=0, microsecond=0)
today10 = time_now.replace(hour=10, minute=0, second=0, microsecond=0)
today13 = time_now.replace(hour=13, minute=0, second=0, microsecond=0)
today14 = time_now.replace(hour=14, minute=0, second=0, microsecond=0)
today18 = time_now.replace(hour=18, minute=0, second=0, microsecond=0)
today22 = time_now.replace(hour=22, minute=0, second=0, microsecond=0)
today23 = time_now.replace(hour=23, minute=0, second=0, microsecond=0)
today00 = time_now.replace(hour=00, minute=0, second=0, microsecond=0)

with ruleset('time'):
    @when_any((m.time >= str(today00)) & (m.time <= str(today08)))
    def green(c):
        global state
        state='green'
        
    @when_any(((m.time > str(today08)) & (m.time <= str(today10)))|((m.time > str(today14)) & (m.time <= str(today18)))|(m.time > str(today22)))
    def orange(c):
        global state
        state='orange'
        
    @when_any(((m.time >= str(today10)) & (m.time <= str(today14)))|((m.time >= str(today18)) & (m.time <= str(today22))))
    def red(c):
        global state
        state='red'

def match_complete_callback(e, state):
    print(e.message)
    
with ruleset('electronics'):
    @when_all((m.type == 'air_conditioner'))
    def air_conditioner(c):
        c.m['load']='heavy'
        finish_callback(c.m)

    @when_all((m.type == 'cooking_appliance'))
    def cooking_appliance(c):
        c.m['load']='heavy'
        finish_callback(c.m)

    @when_all((m.type == 'dishwasher'))
    def dishwasher(c):
        c.m['load']='heavy'
        finish_callback(c.m)

    @when_all((m.type == 'heater'))
    def heater(c):
        c.m['load']='heavy'
        finish_callback(c.m)

    @when_any((m.type == 'light')|( m.type == 'bulb')|(m.type == 'lamp'))
    def light_bulb_lamp(c):
        c.m['load']='light'
        finish_callback(c.m)

    @when_all((m.type == 'space_heater'))
    def space_heater(c):
        c.m['load']='heavy'
        finish_callback(c.m)
        
    @when_any((m.type == 'fridge')|(m.type == 'freezer'))
    def fridge_freezer(c):
        c.m['load']='light'
        finish_callback(c.m)

    @when_any((m.type == 'electronic_display')|(m.type == 'display')|(m.type == 'television')|(m.type == 'lcd')|(m.type == 'tv')|(m.type == 'screen'))
    def screens(c):
        c.m['load']='light'
        finish_callback(c.m)

    @when_all((m.type == 'tumble_drier'))
    def tumble_drier(c):
        c.m['load']='heavy'
        finish_callback(c.m)

    @when_all((m.type == 'ventilation_unit')|(m.type == 'ventilation'))
    def ventilation(c):
        c.m['load']='heavy'
        finish_callback(c.m)

    @when_all((m.type == 'washing_machine'))
    def washing_machine(c):
        c.m['load']='heavy'
        finish_callback(c.m)

    @when_all((m.type == 'ev_charger')|(m.type == 'car_charger')|(m.type == 'bike_charger')|(m.type == 'motorbike_charger'))
    def charger(c):
        c.m['load']='heavy'
        finish_callback(c.m)

    @when_all(+m.type)
    def output(c):
        print('here...')
        msg=c.m
        msg['unknown']='true'
        finish_callback(msg)
        
def finish_callback(message):
    if 'unknown' in message:
        print("Tipo no registrado")
        bot.sendMessage(chat_id='1364830330',text="Tipo no registrado")
    else:
        try:
            print("state:",state)
            myquery = { "chat_id": message.chat_id}
            user=list(USERS.find(myquery))
            myquery = { "supported_appliances": message.type,
                        "state":state,
                        "load_type":message.load
                        }
            res=list(QUESTIONS.find(myquery))

            post=res[random.randint(0,len(res)-1)]
            lan=user[0]['language']
            question=post['question-'+lan]
            postID=post['postID']
            
            print("updating last question...")
            print("Question:",question)
            key = { "chat_id": message.chat_id }
            update={"$set":{"last-question":question}}
            USERS.update(key, update, upsert=True)
            print("Last question updated...")
            
            postID=post['postID']
            options=post['options-'+lan]
            keyboard = []
            for option in options:
                keyboard.append([InlineKeyboardButton(option, callback_data="update:::"+postID+":::"+option)])
            keyboard.append([InlineKeyboardButton('Comentarios/Comments', login_url=LoginUrl('http://127.0.0.1/bot/login_main.php?postID='+postID))])
            print("here....")
            try:
                print("message['chat_id']:",message['chat_id'])
                print("question:",question)
                print("keyboard:",keyboard)
                bot.sendMessage(chat_id=message['chat_id'], text=question, reply_markup=InlineKeyboardMarkup(keyboard))
            except:
                print(sys.exc_info())
        except:
            print(sys.exc_info())

