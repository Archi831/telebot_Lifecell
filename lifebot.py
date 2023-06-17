import time
import json
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

#main variables
TOKEN = "5844896817:AAFqEWkdO27X6w13h5bzOBxFYhgJ58MBr80"
bot = telebot.TeleBot(TOKEN)

# Load the data from the json file
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Welcoming words
@bot.message_handler(commands=['start'])
def start_handler(message):
    global data
    global chat_id
    chat_id = str(message.chat.id)
    bot.send_message(chat_id, "Привіт, я ваш персональний помічник! натискай команду /find ")
    print(chat_id)
    

#initialize data mining :)
@bot.message_handler(commands=['find'])
def finder(message):
    global chat_id
    chat_id = str(message.chat.id)

    # Check if the user is new
    # If they are new, add them to the "database"
    try:
        data["users"][chat_id]
        print("User found")
    except KeyError:
        print("New user")
        data["users"][chat_id] = { "minutes": None, "gigabytes": None, "Type" : None, "number" : None}

    #Sends messages
    bot.send_message(chat_id, 'Я допоможу вам знайти тариф який найбільше підійде вашим потребам')
    time.sleep(1)
    bot.send_message(chat_id, 'Але для цього ви повинні відповісти на декілька запитань')
    time.sleep(1)

    inline_btnTransfer = types.InlineKeyboardButton('Перенести ', callback_data='any1')
    inline_btnPersonalize = types.InlineKeyboardButton('Персоналізувати ', callback_data='any2')
    inline_btnStandart = types.InlineKeyboardButton('Стандартний', callback_data='any3')

    inline_keyboard1 = types.InlineKeyboardMarkup().add(inline_btnTransfer, inline_btnPersonalize, inline_btnStandart)

    bot.send_message(chat_id, "Скажіть, як ви хочете отримати номер?", reply_markup=inline_keyboard1)
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # Handle button callbacks here
    if call.data == 'any1':
        data['users'][str(chat_id)]['number'] = 'Transfered'
        inline_btnPhone = types.InlineKeyboardButton('Телефону', callback_data='1')
        inline_btnGadget = types.InlineKeyboardButton('Гаджету', callback_data='2')

        inline_keyboard1 = types.InlineKeyboardMarkup().add(inline_btnPhone, inline_btnGadget)

        bot.send_message(chat_id, "Вам потрібен тариф для телефону чи якогось гаджету?", reply_markup=inline_keyboard1)
    elif call.data == 'any2':
        data['users'][str(chat_id)]['number'] = 'Personalized'
        inline_btnPhone = types.InlineKeyboardButton('Телефону', callback_data='1')
        inline_btnGadget = types.InlineKeyboardButton('Гаджету', callback_data='2')

        inline_keyboard1 = types.InlineKeyboardMarkup().add(inline_btnPhone, inline_btnGadget)

        bot.send_message(chat_id, "Вам потрібен тариф для телефону чи якогось гаджету?", reply_markup=inline_keyboard1)
    elif call.data == 'any3':
        data['users'][str(chat_id)]['number'] = 'Standart'
        inline_btnPhone = types.InlineKeyboardButton('Телефону', callback_data='1')
        inline_btnGadget = types.InlineKeyboardButton('Гаджету', callback_data='2')

        inline_keyboard1 = types.InlineKeyboardMarkup().add(inline_btnPhone, inline_btnGadget)

        bot.send_message(chat_id, "Вам потрібен тариф для телефону чи якогось гаджету?", reply_markup=inline_keyboard1)
    elif call.data == '1':
        bot.answer_callback_query(call.id, "Your choice: Phone")
        data["users"][str(chat_id)]['Type'] = 'Phone'

        inline_btnLessPhoneCalls = types.InlineKeyboardButton('500-1600 хвилин', callback_data='6')
        inline_btnMorePhoneCalls = types.InlineKeyboardButton('0-500 хвилин', callback_data='4')
        inline_btnPhoneCalls = types.InlineKeyboardButton("3000 хвилин", callback_data='5')

        inline_keyboard1 = types.InlineKeyboardMarkup().add(inline_btnLessPhoneCalls, inline_btnMorePhoneCalls, inline_btnPhoneCalls)

        bot.send_message(call.message.chat.id, "Скільки часу ви балакаєте по телефону?", reply_markup=inline_keyboard1)
        
    elif call.data == '4':
        bot.answer_callback_query(call.id, "Less than 500 minutes")
        data["users"][str(chat_id)]['minutes'] = '0-500'
        inline_btnNoData = types.InlineKeyboardButton('0', callback_data='00+')
        inline_btn8GB = types.InlineKeyboardButton('8', callback_data='8+')
        inline_btnUnlim = types.InlineKeyboardButton('Unlimited', callback_data='999+')

        inline_keyboard1 = types.InlineKeyboardMarkup().add(inline_btnNoData, inline_btn8GB, inline_btnUnlim)

        bot.send_message(call.message.chat.id, "Скільки б ви хотіли мати гігабайт мобільного інтернету?", reply_markup=inline_keyboard1)

    elif call.data == '00+':
        data["users"][str(chat_id)]['gigabytes'] = '0'
        bot.answer_callback_query(call.id, "No data")
        with open('Pictures/ДзвінкийБезмеж.png', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption='Я підібрав тариф який найбільше вам підходить - Дзвінкий Безмеж \n З ним ви отримаєте: \n Безліміт на lifecell \n 250 хв на номери інших мобільних операторів по Україні')
            inline_btn = types.InlineKeyboardButton('Click here', url='https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/dzvinkiy/')
            inline_keyboard = types.InlineKeyboardMarkup().add(inline_btn)
            bot.send_message(call.message.chat.id, "Ось Дзвінкий Безмеж", reply_markup=inline_keyboard)
    elif call.data == '8+':
        data["users"][str(chat_id)]['gigabytes'] = '8'
        bot.answer_callback_query(call.id, "8gb")
        with open('Pictures\ПростоЛайф.png', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption='Я підібрав тариф який найбільше вам підходить - Просто Лайф\n З ним ви отримаєте: \n 8 ГБ інтернету \n 300 хв на всі мобільні номери по Україні (вкл. lifecell) \n Безліміт на lifecell після використання хвилин на всі мобільні номери')
            inline_btn = types.InlineKeyboardButton('Click here', url='https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/prosto-life-2021/')
            inline_keyboard = types.InlineKeyboardMarkup().add(inline_btn)
            bot.send_message(call.message.chat.id, "Ось Просто Лайф", reply_markup=inline_keyboard)
    elif call.data == '999+':
        data["users"][str(chat_id)]['gigabytes'] = 'Unlimited'
        bot.answer_callback_query(call.id, "Unlimited")
        with open('Pictures\інтернетБезмеж.png', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption='Я підібрав тариф який найбільше вам підходить - Інтернет без меж\n З ним ви отримаєте: \n Безлімітний інтернет \n 250 хв на номери інших мобільних операторів по Україні \n Безліміт на lifecell')
            inline_btn = types.InlineKeyboardButton('Click here', url='https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/int-bezmezh-2021/')
            inline_keyboard = types.InlineKeyboardMarkup().add(inline_btn)
            bot.send_message(call.message.chat.id, "Ось Інтернет Безмеж", reply_markup=inline_keyboard)


    elif call.data == '6':
        bot.answer_callback_query(call.id, "Less than 500 minutes")
        data["users"][str(chat_id)]['minutes'] = '500-1600'
        inline_btn25GB = types.InlineKeyboardButton('25', callback_data='25-')
        inline_btn40GB = types.InlineKeyboardButton('40', callback_data='40-')
        inline_btnUnlim = types.InlineKeyboardButton('Unlimited', callback_data='999-')

        inline_keyboard1 = types.InlineKeyboardMarkup().add(inline_btn25GB, inline_btn40GB, inline_btnUnlim)

        bot.send_message(call.message.chat.id, "Скільки б ви хотіли мати гігабайт мобільного інтернету?", reply_markup=inline_keyboard1)

    elif call.data == '25-':
        data["users"][str(chat_id)]['gigabytes'] = '25'
        bot.answer_callback_query(call.id, "25gb")
        with open('Pictures\CvfhnKfqa.png', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption='Я підібрав тариф який найбільше вам підходить - Смарт Лайф!.\n Ось що у нього входить:\n  25 ГБ інтернету\n 800 хв на всі мобільні номери по Україні (вкл. lifecell)\n Безліміт на lifecell після використання хвилин на всі мобільні номери \nБезліміт на соціальні мережі \nБезкоштовна роздача інтернету через пристрої')
            inline_btn = types.InlineKeyboardButton('Click here', url='https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/smart-life-2021/')
            inline_keyboard = types.InlineKeyboardMarkup().add(inline_btn)
            bot.send_message(call.message.chat.id, "Ось Смарт Лайф", reply_markup=inline_keyboard)

    elif call.data == '40-':
        data["users"][str(chat_id)]['gigabytes'] = '40'
        bot.answer_callback_query(call.id, "40gb")
        with open('Pictures\Потужний.png', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption='Я підібрав тариф який найбільше вам підходить - Потужний!.\n Ось що у нього входить:\n 40 ГБ \n Безлімітний інтернет з акцією «Потужний безліміт» \n 800 хв на всі мобільні номери по Україні (вкл. lifecell) \n Безліміт на lifecell після використання хвилин на всі мобільні номери \n Безкоштовна роздача інтернету через пристрої')
            inline_btn = types.InlineKeyboardButton('Click here', url='https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/potuzhnyy/')
            inline_keyboard = types.InlineKeyboardMarkup().add(inline_btn)
            bot.send_message(call.message.chat.id, "Ось тариф Потужний його вартість 165 грн", reply_markup=inline_keyboard)
    elif call.data == '5':
        data["users"][str(chat_id)]['gigabytes'] = 'Unlimited'
        data["users"][str(chat_id)]['minutes'] = '3000'
        bot.answer_callback_query(call.id, "Best tariff")
        with open('Pictures\PlatinumLife.png', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption='Я підібрав тариф який найбільше вам підходить - Platinum Life!.\n Ось що у нього входить:\n Безлімітний інтернет. \n 3000 хв на всі номери по Україні (міські, мобільні, lifecell). \n Безліміт на lifecell після використання хвилин на всі номери. \n Міжнародні дзвінки в країнах 1 та 2 груп: 50 хв. \n Інтернет у роумінгу в країнах 1 та 2 груп: 500 МБ.')
            inline_btn = types.InlineKeyboardButton('Click here', url='https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/platinum-life-2021/')
            inline_keyboard = types.InlineKeyboardMarkup().add(inline_btn)
            bot.send_message(call.message.chat.id, "Ось тариф Platinum Life його вартість 450 грн", reply_markup=inline_keyboard)
    elif call.data == '999-':
        data["users"][str(chat_id)]['gigabytes'] = 'Unlimited'
        bot.answer_callback_query(call.id, "Unlimited")
        with open('Pictures\ВільнийРегіон.png', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption='Я підібрав тариф який найбільше вам підходить - Вільний Лайф!.\n Ось що у нього входить:\n Безлімітний інтернет \n 1600 хв на всі номери по Україні (міські, мобільні, lifecell) \n Безліміт на lifecell після використання хвилин на всі номери')
            inline_btn = types.InlineKeyboardButton('Click here', url='https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/vilniy-life-2021/')
            inline_keyboard = types.InlineKeyboardMarkup().add(inline_btn)
            bot.send_message(call.message.chat.id, "Ось тариф Вільний Лайф його вартість 270 грн", reply_markup=inline_keyboard)
         

#gadget
    elif call.data == '2':
        bot.answer_callback_query(call.id, "Youe choice: Gadget")
        #data["users"][str(chat_id)]['Type'] = '2'
    
        inline_btnSmartWatch = types.InlineKeyboardButton('Smart Watch', callback_data='SW')
        inline_btnTablet = types.InlineKeyboardButton('Tablet', callback_data='Tablet')
        inline_btnRouter = types.InlineKeyboardButton('Router', callback_data='Router')

        inline_keyboard1 = types.InlineKeyboardMarkup().add(inline_btnSmartWatch, inline_btnTablet, inline_btnRouter)

        bot.send_message(call.message.chat.id, "What is your gadget type?", reply_markup=inline_keyboard1)

    elif call.data == 'SW':
        bot.answer_callback_query(call.id, "Your Gadget is Smart Watch")
        data["users"][str(chat_id)]['Type'] = 'Smart Watch'
        inline_btnSmartWatchPlus = types.InlineKeyboardButton('Smart Watch Plus', callback_data='SW+')
        inline_btnSmartWatchMinus = types.InlineKeyboardButton('Smart Watch Minus', callback_data='SW-')

        inline_keyboard1 = types.InlineKeyboardMarkup().add(inline_btnSmartWatchPlus, inline_btnSmartWatchMinus)

        bot.send_message(call.message.chat.id, "Which data plan suits you best?", reply_markup=inline_keyboard1)

    elif call.data == 'SW-':
        bot.answer_callback_query(call.id, "Your Gadget is Smart Watch Minus")
        bot.send_message(call.message.chat.id, "your best plan is this one")
        #complete
    elif call.data == 'SW+':
        bot.answer_callback_query(call.id, "Your Gadget is Smart Watch Plus")
        bot.send_message(call.message.chat.id, "your best plan is this one")
        #complete
    elif call.data == 'Tablet':
        data["users"][str(chat_id)]['Type'] = 'Tablet'
        bot.answer_callback_query(call.id, "Your Gadget is Tablet")
        bot.send_message(call.message.chat.id, "your best plan is this one")
        #complete
    elif call.data == 'Router':
        data["users"][str(chat_id)]['Type'] = 'Router'
        bot.answer_callback_query(call.id, "Your Gadget is Router")
        bot.send_message(call.message.chat.id, "your best plan is this one")
        #complete
    
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

bot.polling()
