import telebot
import db
import mathmodule
from mathmodule import MathModule
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

# Команда /first
# Команда /first
@bot.message_handler(commands=['first'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id in current_state:
        bot.reply_to(message, "Вы уже начали ввод данных. Продолжайте, пожалуйста.")
        return

    bot.send_message(chat_id, "Отправьте мне название города.")
    current_state[chat_id] = {
        'state': 'city',
        'data': {}
    }

# Команда /cancel для отмены текущего процесса ввода данных
@bot.message_handler(commands=['cancel'])
def cancel_process(message):
    chat_id = message.chat.id
    if chat_id in current_state:
        del current_state[chat_id]
        bot.send_message(chat_id, "Процесс ввода данных отменен.")

# Команда /test
@bot.message_handler(commands=['test'])
def test_command(message):
    chat_id = message.chat.id
    res_list = MathModule.first_chapter(db.get_values()[0][1], db.get_values()[0][2], db.get_values()[0][3])
    print(res_list)
    bot.send_message(chat_id, f"Считаем строительную площадь камер хранения по формуле: `Fк.хр = Вк / (b * hгр * qv)`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Получается: `{res_list[0]} м^2 = {db.get_values()[0][2]} т / (0,75 * {res_list[1]} м * {res_list[10]} т/м^3)`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Считаем площадь вспомогательных помещений по формуле : `Fвсп = 0,25..0,4 * Fкхр`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Получается: `{res_list[1]} м^2 = 0,25 * {res_list[0]} м^2`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Считаем площадь холодильника в контуре изоляции по формуле  : `Fхол = Fк.хр + Fвсп`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Получается: `{res_list[2]} м^2 = {res_list[0]} м^2 + {res_list[1]} м^2`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Считаем площадь машинного отделения по формуле  : `Fмо = (0,05..0,35 * Fхол)`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Получается: `{res_list[3]} м^2 = 0,05 + {res_list[2]} м^2`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Считаем площадь служебных помещений по формуле   : `Fсп = (0,2..0,5 * Fхол)`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Получается: `{res_list[4]} м^2 = 0,2 * {res_list[2]} м^2`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Число строительных прямоугольников камер хранения: `{res_list[0]} / 144 = {res_list[5]}`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Число строительных прямоугольников вспомогательного помещения: `{res_list[1]} / 144 = {res_list[6]}`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Число строительных прямоугольников холодильника:  `{res_list[2]} / 144 = {res_list[7]}`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Число строительных прямоугольников машинного отделения:  `{res_list[3]} / 144 = {res_list[8]}`", parse_mode='Markdown')
    bot.send_message(chat_id, f"Число строительных прямоугольников служебного помещения:  `{res_list[4]} / 144 = {res_list[9]}`", parse_mode='Markdown')

# Основная логика обработки сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    if chat_id not in current_state:
        bot.send_message(chat_id, "Сначала начните ввод данных с помощью команды /first.")
        return

    state = current_state[chat_id]['state']
    data = current_state[chat_id]['data']

    if state == 'city':
        city = message.text.strip().capitalize()
        data['city'] = city
        bot.send_message(chat_id, f"Вы указали город {city}. Теперь пришлите объем товара.")
        current_state[chat_id]['state'] = 'weight'
    elif state == 'weight':
        try:
            weight = float(message.text)
            data['weight'] = weight
            bot.send_message(chat_id, f"Теперь пришлите название товара.")
            current_state[chat_id]['state'] = 'product'
        except ValueError:
            bot.send_message(chat_id, "Пожалуйста, введите корректное значение объема.")
            return
    elif state == 'product':
        product = message.text.strip().capitalize()
        data['product'] = product

        # Сохранение данных в БД
        db.add_values(chat_id, data['city'], data['weight'], product)

        bot.send_message(chat_id, f"Данные сохранены: Город {data['city']}, Объем {data['weight']}, Товар {product}")
        del current_state[chat_id]
        return

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
    db.close()
    dbMath.close()