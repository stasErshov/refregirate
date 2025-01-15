import telebot
import db
from db.mathdb import MathDatabase
from db.dbproc import Database

from telebot import types

TOKEN = '2101819294:AAGeDOJaOWpUcsxjGV8X6Z7JS4RbBX0j7qs'

bot = telebot.TeleBot(TOKEN)

db = Database('db/users.db')
db.create_table()

dbMath = MathDatabase('db/mathdb.db')
dbMath.create_tablemath()

# Команда /add_user для добавления пользователя
@bot.message_handler(commands=['add_user'])
def add_user(message):
    try:
        _, username, email = message.text.split(maxsplit=2)
        bo = db.add_user(message.chat.id, username, email, 1)
        if bo:
            bot.reply_to(message, f"Пользователь {username} добавлен.")
        else:
            bot.reply_to(message, f"Такой пользователь уже существует.")
    except ValueError:
        bot.reply_to(message, "Не удалось добавить пользователя. Проверьте формат команды.")

# Команда /get_users для получения списка пользователей
@bot.message_handler(commands=['get_users'])
def get_users(message):
    users = db.get_users()
    response = "\n".join([f"{u[0]} - {u[1]} ({u[2]})" for u in users])
    bot.reply_to(message, response or "Пользователи отсутствуют.")

current_state = {}

# Обработка команды /first
@bot.message_handler(commands=['first'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Отправьте мне название города.")
    current_state[message.chat.id] = {'state': 'city'}

# Основная логика обработки сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    if chat_id not in current_state:
        current_state[chat_id] = {'state': 'city'}

    state = current_state[chat_id]['state']

    if state == 'city':
        city = message.text.strip().capitalize()
        current_state[chat_id]['city'] = city
        bot.send_message(chat_id, f"Вы указали город {city}. Теперь пришлите объем товара.")
        current_state[chat_id]['state'] = 'weight'
    elif state == 'weight':
        try:
            weight = float(message.text)
        except ValueError:
            bot.send_message(chat_id, "Пожалуйста, введите корректное значение объема.")
            return

        current_state[chat_id]['weight'] = weight
        bot.send_message(chat_id, f"Теперь пришлите название товара.")
        current_state[chat_id]['state'] = 'product'
    elif state == 'product':
        product = message.text.strip().capitalize()

        # Сохранение данных в БД
        db.add_values(chat_id, current_state[chat_id]['city'], current_state[chat_id]['weight'], product)

        bot.send_message(chat_id, f"Данные сохранены: Город {current_state[chat_id]['city']}, Объем {current_state[chat_id]['weight']}, Товар {product}")
        del current_state[chat_id]

# Запуск бота
if __name__ == '__main__':
    bot.polling()
    db.close()
    dbMath.close()