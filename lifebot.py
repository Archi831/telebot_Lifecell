import time
import json
import telebot
from telebot import types

#main variables
TOKEN = "token"
bot = telebot.TeleBot(TOKEN)

minutes = 0
gigabytes = 0

# Welcoming words
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Hello, I'm your personal advisor")
    print(message.chat.id)
    

@bot.message_handler(commands=['find'])
def finder(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'I will help you to find your optimal tariff plan that best suits your needs.')
    time.sleep(1)
    bot.send_message(chat_id, 'First, you have to answer some questions')
    time.sleep(1)
    bot.send_message(chat_id, 'How often do you call other people?')
    msg = bot.send_message(chat_id, 'Tell me how much do you talk (mins)')
    bot.register_next_step_handler(msg, InputAnswer)

def InputAnswer(message):
    global minutes
    text = message.text
    chat_id = message.chat.id
    if not message.text.isdigit():
        msg = bot.send_message(chat_id, 'please input a number')
        bot.register_next_step_handler(msg, InputAnswer)
        return
    bot.send_message(chat_id, 'You speak for ' + str(text) + " minutes")
    minutes = text
    print(f"User {message.chat.id} talks for {minutes} minutes")
    msg = bot.send_message(chat_id, 'Tell me how much do you use internet (Gigabites)')
    bot.register_next_step_handler(msg, InputAnswer2)

def InputAnswer2(message):
    global gigabytes
    text = message.text
    chat_id = message.chat.id
    if not message.text.isdigit():
        msg = bot.send_message(chat_id, 'please input a number')
        bot.register_next_step_handler(msg, InputAnswer)
        return
    gigabytes = text
    print(f"User {message.chat.id} uses {gigabytes} gb of internet")
    bot.send_message(chat_id, 'You use ' + str(text) + " gigabytes of internet")

def tariff_choser():
    pass

def check_data():
    pass


bot.polling()

