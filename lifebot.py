import time
import json
import telebot
from telebot import types

#main variables
TOKEN = "5844896817:AAFqEWkdO27X6w13h5bzOBxFYhgJ58MBr80"
bot = telebot.TeleBot(TOKEN)

# Load the data from the json file
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.loads(file.read())

# Welcoming words
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Hello, I'm your personal advisor")
    print(message.chat.id)
    

@bot.message_handler(commands=['find'])
def finder(message):
    chat_id = message.chat.id

    # Check if the user is new
    # If they are new, add them to the "database"
    try:
        data["users"][message.chat.id]
        print("User found")
    except KeyError:
        print("New user")
        data["users"][message.chat.id] = { "minutes": None, "gigabytes": None }

    bot.send_message(chat_id, 'I will help you to find your optimal tariff plan that best suits your needs.')
    time.sleep(1)
    bot.send_message(chat_id, 'First, you have to answer some questions')
    time.sleep(1)
    bot.send_message(chat_id, 'How often do you call other people?')

    msg = bot.send_message(chat_id, 'Tell me how much do you talk (mins)')
    bot.register_next_step_handler(msg, Input_user_minutes)

def Input_user_minutes(message):
    text = message.text
    chat_id = message.chat.id

    if not message.text.isdigit():
        msg = bot.send_message(chat_id, 'please input a number')
        bot.register_next_step_handler(msg, Input_user_minutes)
        return
    
    bot.send_message(chat_id, 'You speak for ' + str(text) + " minutes")
    data["users"][message.chat.id]["minutes"] = text
    

    print(f"User {message.chat.id} talks for {text} minutes")
    msg = bot.send_message(chat_id, 'Tell me how much do you use internet (Gigabites)')
    bot.register_next_step_handler(msg, Input_user_gigabites)

def Input_user_gigabites(message):
    text = message.text
    chat_id = message.chat.id

    if not message.text.isdigit():
        msg = bot.send_message(chat_id, 'please input a number')
        bot.register_next_step_handler(msg, Input_user_minutes)
        return
    
    data["users"][message.chat.id]["gigabytes"] = text
    print(f"User {message.chat.id} uses {text} gb of internet")
    bot.send_message(chat_id, 'You use ' + str(text) + " gigabytes of internet")
    msg = bot.send_message(chat_id, "Saving your data...")
    
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))
        

def tariff_choser():
    pass

def check_data():
    pass


bot.polling()

