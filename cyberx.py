import telebot
from telebot import types
import test

token = '7032134012:AAGebBM3NygRmsIXaWW1grUcahAvdssjX6U'

bot = telebot.TeleBot(token)

date = ""
name = ""
phone = ""
oclock = ""

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Забронировать")
    markup.add(item1)
    photo = open('photo_2024-04-16_16-58-43.jpg', 'rb')
    bot.send_photo(message.from_user.id, photo)
    bot.send_message(message.chat.id, "Привет ✌️. Я бот компьютерного клуба CyberX Community. Хотели бы забронировать место?", reply_markup=markup)

@bot.message_handler(content_types='text')
def reserve_message(message):
    if message.text == 'Забронировать':
        bot.send_message(message.from_user.id, "Напишите ваше имя. Например: Иван")
        bot.register_next_step_handler(message, get_date)
    

def get_date(message):
    global date
    ejen = test.filter_bad_words(message.text)
    if ejen == True:
        name = message.text
        bot.send_message(message.from_user.id, "Введите ваш номер телефона")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "Не матерись пожалуйста. Введи повторно свое имя")
        bot.register_next_step_handler(message, get_date)
        
    
def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Во сколько хотели бы прийти")
    bot.register_next_step_handler(message, get_oclock)
    
def get_oclock(message):
    global oclock, name, date
    oclock = message.text
    bot.send_message(message.from_user.id, "Спасибо что используете нашего бота. Ваши данные все сохранены. В скором времени с вами свяжется администратор для подтверждения записи.")
    bot.send_message(message.from_user.id, f"Ваше имя и номер телефона {name}, Дата брони {date}, Время брони {oclock}")


bot.infinity_polling()
