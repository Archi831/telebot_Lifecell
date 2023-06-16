import telebot

#main variables
TOKEN = "5844896817:AAFqEWkdO27X6w13h5bzOBxFYhgJ58MBr80"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Hello')
bot.polling()