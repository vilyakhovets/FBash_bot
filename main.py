import requests
from bs4 import BeautifulSoup as bs
import telebot
import time

URL = 'https://xn--80abh7bk0c.xn--p1ai/random'
API_KEY = '6289870080:AAFQcLuyRXwYX32heZlAJSYcW6Elzd_1ueY'


def parser(url):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    rand_bash = soup.find_all('div', class_='quote__body')
    return rand_bash[0:5]


def post_out():
    rand_bash_list = parser(URL)
    cnt = 0
    for i in rand_bash_list:
        rand_bash_list[cnt] = str(i)[25:-6].replace('<br/>', '\n').rstrip().lstrip()
        cnt += 1
    output = (('\n\n' + '*' * 30 + '\n\n').join(rand_bash_list)).replace('&lt;', '').replace('&gt;', ':')
    return output


bot = telebot.TeleBot(API_KEY)

user_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
user_markup.row('/старт', '/еще')


@bot.message_handler(commands=['старт'])
def handle_start(message):
    while True:
        bot.send_message(message.chat.id, post_out(), reply_markup=user_markup)
        time.sleep(14400)


@bot.message_handler(commands=['еще'])
def handle_more(message):
    bot.send_message(message.chat.id, post_out(), reply_markup=user_markup)


bot.polling()
