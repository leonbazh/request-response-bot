import telebot
from telebot import types
import filterx
import datetime
import aiogram


token = ''

bot = telebot.TeleBot(token)

date = ""
name = ""
phone = ""
time = ""
zone = ""
count = ""

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Забронировать")
    item2 = types.KeyboardButton("Посмотреть зоны")
    markup.add(item1, item2)
    bot.send_photo(message.from_user.id, 'https://sun9-32.userapi.com/impg/UZOK2C_1V9wW35duluOe6qzd-Cvylq6b7Adx7A/l03lNyuSbi0.jpg?size=1080x1080&quality=95&sign=5dd987c7fe760a8d8533915e3f26c211&type=album')
    bot.send_message(message.chat.id, "Привет ✌️. Я бот компьютерного клуба CyberX Community. Хотели бы забронировать место?", reply_markup=markup)



@bot.message_handler(content_types='text')
def reserve_message(message):
    if message.text == 'Забронировать':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "Напишите ваше имя. Например: Иван", reply_markup=markup)
        bot.register_next_step_handler(message, get_name)
    if message.text == 'Посмотреть зоны':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Забронировать')
        markup.add(item1)
        media =  ['https://cloud.mail.ru/public/Gv1J/feTWLvRyE','https://cloud.mail.ru/public/RGoS/LB1KmbKsP','https://cloud.mail.ru/public/28Vv/vfquKer5u' , 'https://cloud.mail.ru/public/Md3g/yh83Y66ZE']
        media1 = [types.InputMediaPhoto(photo) for photo in media]
        bot.send_media_group(message.from_user.id, media1)
        bot.send_message(message.from_user.id, "К вашему вниманию 4 зоны: Standart, BootCamp, VIP, Lounge", reply_markup=markup)
    

def get_name(message):
    global name
    flag = filterx.filter_bad_words(message.text)
    if flag == True:
        name = message.text
        bot.send_message(message.from_user.id, "Введите ваш номер телефона по форме: +79*********")
        bot.register_next_step_handler(message, get_number)
    else:
        bot.send_message(message.from_user.id, "Некорректный ввод. Введите повторно свое имя")
        bot.register_next_step_handler(message, get_name)

def get_number(message):
    global phone
    flag = filterx.filter_number(message.text)
    if flag == True:
        phone = message.text
        now = datetime.datetime.now()
        formatted_date = now.strftime("%d.%m")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(formatted_date)
        markup.add(item1)
        bot.send_message(message.from_user.id, "Введите дату когда хотели бы придти по форме. Например: {}".format(formatted_date), reply_markup=markup)
        bot.register_next_step_handler(message, get_date)
    else:
        bot.send_message(message.from_user.id, "Некорректный номер телефона. Попробуйте еще раз и по форме")
        bot.register_next_step_handler(message, get_number)
        

def get_date(message):
    global date
    flag = filterx.filter_date(message.text)
    if flag == True:
        date = message.text
        now = datetime.datetime.now()
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if int(hour) == 23 and int(minute) < 30:
            item1 = types.KeyboardButton(f"00:00")
        elif int(hour) == 23 and int(minute) >= 30:
            item1 = types.KeyboardButton(f"00:30")
        elif int(hour) + 1 < 10 and int(minute) < 30:
            item1 = types.KeyboardButton(f"0{int(hour)+1}:00")
        elif int(hour) + 1 < 10 and int(minute) >= 30:
            item1 = types.KeyboardButton(f"0{int(hour)+1}:30")
        elif int(hour) + 1 >=10 and int(minute) >= 30:
            item1 = types.KeyboardButton(f"{int(hour)+1}:30")
        else:
            item1 = types.KeyboardButton(f"{int(hour)+1}:00")
        markup.add(item1)
        bot.send_message(message.from_user.id, "Введите время когда хотели бы придти по форме. Например: 09:30", reply_markup=markup)
        bot.register_next_step_handler(message, get_time)
    else:
        bot.send_message(message.from_user.id, "Некорректная дата. Попробуйте еще раз по форме")
        bot.register_next_step_handler(message, get_date)


def get_time(message):
    global time, date
    flag = filterx.filter_time(message.text, date)
    if flag == True:
        time = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Standart')
        item2 = types.KeyboardButton('Bootcamp')
        item3 = types.KeyboardButton('VIP')
        item4 = types.KeyboardButton('Lounge')
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.from_user.id, 'Выберите в какой зоне хотели бы забронировать', reply_markup=markup)
        bot.register_next_step_handler(message, get_zone)
    else:
        bot.send_message(message.from_user.id, "Некорректная время. Попробуйте еще раз по форме")
        bot.register_next_step_handler(message, get_time)
        
def get_zone(message):
    global zone
    zones = ['Standart', 'Bootcamp', 'VIP', 'Lounge']
    if not message.text in(zones):
        bot.send_message(message.from_user.id, 'Выберите, нажав кнопку ниже')
        bot.register_next_step_handler(message, get_zone)
    else:
        zone = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('1')
        item2 = types.KeyboardButton('3')
        item3 = types.KeyboardButton('5')
        markup.add(item1, item2, item3)
        bot.send_message(message.from_user.id, 'Укажите на какое количество человек бронь', reply_markup=markup)
        bot.register_next_step_handler(message, get_count)

def get_count(message):
    global count
    flag = filterx.filter_count(message.text)
    if flag == True:
        count = message.text
        get_total(message)
    else:
        bot.send_message(message.from_user.id, 'Некорректный ввод. Попробуйте снова')
        bot.register_next_step_handler(message, get_count)
    
def get_total(message):
    global time, name, date, phone, zone, count
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Забронировать")
    item2 = types.KeyboardButton("Посмотреть зоны")
    markup.add(item1, item2)
    bot.send_message(message.from_user.id, f'''Ваше имя и номер телефона: {name} {phone}
Дата и время: {date} {time}''')
    bot.send_message(message.from_user.id, '''Спасибо за использование бота 😁
Ваши данные все сохранены 👌. В скором времени с вами свяжется администратор для подтверждения записи. Для дальнейших бронирований, можете нажать на кнопку "Забронировать" ниже 👇''', reply_markup=markup)
    bot.send_message('7037710515', f'''Имя: {name}
Номер телефона: {phone}
Дата и время брони: {date} {time}
Зона: {zone}
Кол-во человек: {count}''')
bot.infinity_polling()
