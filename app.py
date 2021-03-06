#install flask => pip install flask

import logging
from flask import Flask,request
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters 
from telegram.ext import Dispatcher
import os
from telegram import Bot
from telegram import Update
from dia1 import get_reply
from dia1 import fetch_news
from dia1 import topics_keyboards

#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
                    )

logger=logging.getLogger(__name__)

TOKEN="1487310155:AAFOuRJaZ92CWQtBEt9rSdM7BHnfEHgHwGc" #from telegram provided stored in ~/.bash_profile


app=Flask(__name__)

@app.route("/")
def index():
    return "Hello world!"


@app.route("/{}".format(TOKEN),methods=['GET','POST'])
def webhook():
    update=Update.de_json(request.get_json(),bot)
    dp.process_update(update)
    return "ok"


def start(update,bot):
    author=update.message.chat.first_name
    reply="Hi, {}!".format(author)
    update.message.reply_text(text=reply)

def _help(update,bot):
    help_text="Hi, This is a help text!"
    update.message.reply_text(help_text)
    #bot.send_message(chat_id=update.message.chat_id,text=help_text)

def news(update,bot):
    markup=ReplyKeyboardMarkup(keyboard=topics_keyboards,one_time_keyboard=True)
    update.message.reply_text(text="Choose a Category!",reply_markup=markup)

#Echoing
def echo_text(update,bot):
    reply=update.message.text
    update.message.reply_text(text=reply)

def echo_sticker(update,bot):
    #print(update)
    #bot.send_sticker(chat_id=update.message.chat_id,sticker=update.message.sticker.file_id)
    update.message.reply_sticker(sticker=update.message.sticker.file_id)


#General Replying with the help of dia1.py
def reply_text(update,bot):
    print("Hello!!")
    intent,reply=get_reply(update.message.text,update.message.chat.id)
    if intent=="get_news":
        reply_text="Ok, Here are the news: \n\n\n"  
        update.message.reply_text(text=reply_text)
        newes=fetch_news(reply)   
        for news in newes:
            update.message.reply_text(text=news['link'])
    else:
        update.message.reply_text(text=reply)
    #update.message.reply_text(text="Hii")

def error(update,bot):
    logger.error("Update {} has caused error: ".format(update.message.chat.id))


bot=Bot(TOKEN)
bot.set_webhook("https://newsbot2216.herokuapp.com/"+TOKEN)    #from heroku app
dp=Dispatcher(bot,None)
dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("help",_help))
dp.add_handler(CommandHandler("news",news))
#dp.add_handler(MessageHandler(Filters.text,echo_text))
dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
dp.add_handler(MessageHandler(Filters.text,reply_text))
dp.add_error_handler(error)
app.run(port=8443)


   
  



