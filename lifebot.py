import time
import json
import telebot
from telebot import types

#main variables
TOKEN = "5844896817:AAFqEWkdO27X6w13h5bzOBxFYhgJ58MBr80"
bot = telebot.TeleBot(TOKEN)

data = {"user" : [], "minutes" : [], "gigabytes" : []}

# Welcoming words
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Hello, I'm your personal advisor")
    print(message.chat.id)
    data['user'].append(message.chat.id)

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
    global data
    text = message.text
    chat_id = message.chat.id
    if not message.text.isdigit():
        msg = bot.send_message(chat_id, 'please input a number')
        bot.register_next_step_handler(msg, InputAnswer)
        return
    bot.send_message(chat_id, 'You speak for ' + str(text) + " minutes")
    data['minutes'].append(text)
    

    print(f"User {message.chat.id} talks for {text} minutes")
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
    data['gigabytes'].append(text)
    print(f"User {message.chat.id} uses {text} gb of internet")
    bot.send_message(chat_id, 'You use ' + str(text) + " gigabytes of internet")
    msg = "Saving your data..."
    bot.register_next_step_handler(msg, write_json)

def write_json(new_data, filename='data.json'):
    with open(filename,'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        file_data["users"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

def tariff_choser():
    pass

def check_data():
    pass


bot.polling()

