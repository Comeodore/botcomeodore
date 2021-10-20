import telebot
import requests
import time
import schedule
from telebot import types
from telebot.types import Message
from multiprocessing.context import Process

bot = telebot.TeleBot('SECRET')
currency_text = "Курс валют 💰"


@bot.message_handler(commands=['start'])
def start_message(message: Message):
    ans_start = 'Привет, ' + message.chat.first_name + ', для того, чтобы курс валют используйте кнопки снизу или вводите слеш используя команды бота.'
    bot.send_message(message.chat.id, ans_start, reply_markup=keyboard())


@bot.message_handler(commands=['hello'])
def send_welcome(message: Message):
    bot.reply_to(message, 'Приветствую Вас')


@bot.message_handler(commands=['currency'])
def send_currency(message: Message):
    URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    r = requests.get(URL)
    currency = 'Курс валют: Продажа | Покупка\n'
    for i in range(4):
        currency += r.json()[i]['base_ccy'] + ' к ' + r.json()[i]['ccy'] + ': ' + r.json()[i]['buy'] + ' | ' + \
                    r.json()[i]['sale'] + '\n'
    bot.send_message(message.chat.id, currency)



def send_daily_message():
    bot.send_message(509679594,
                     'Some text')

@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def send_echo(message: Message):
    if message.text == currency_text:
        send_currency(message)
        return


@bot.message_handler(content_types=['sticker'])
def sticker_id(message: Message):
    print(message.sticker)

schedule.every().day.at("9:30").do(send_daily_message)


class ScheduleMessage():
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()


def keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_currency = types.KeyboardButton(currency_text)
    markup.add(button_currency)
    return markup


if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass
