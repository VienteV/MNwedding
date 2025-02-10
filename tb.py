import telebot
from telebot import types
from telebot.types import InlineKeyboardButton

bot = telebot.TeleBot("7547727034:AAGvbLkIymSkrpUYHHKQzLH2fsNKOfsuKhU")

@bot.message_handler(commands=['start'])
def start_comand(message):
    print(message.chat.id)
    bot.send_message(message.chat.id, 'text')
bot.infinity_polling(none_stop=True)
5856006175