import telebot
import sqlite3

TOKEN = '2101819294:AAGeDOJaOWpUcsxjGV8X6Z7JS4RbBX0j7qs'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой новый бот.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Вы написали: {message.text}")

if __name__ == '__main__':
    bot.polling()
def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('PyCharm')