import telebot
import db
from db.dbproc import Database

# Токен вашего бота
TOKEN = '2101819294:AAGeDOJaOWpUcsxjGV8X6Z7JS4RbBX0j7qs'

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Инициализация базы данных
db = Database('db/users.db')
db.create_table()

# Команда /add_user для добавления пользователя
@bot.message_handler(commands=['add_user'])
def add_user(message):
    try:
        _, username, email = message.text.split(maxsplit=2)
        db.add_user(message.chat.id, username, email, 1)
        bot.reply_to(message, f"Пользователь {username} добавлен.")
    except ValueError:
        bot.reply_to(message, "Не удалось добавить пользователя. Проверьте формат команды.")

# Команда /get_users для получения списка пользователей
@bot.message_handler(commands=['get_users'])
def get_users(message):
    users = db.get_users()
    response = "\n".join([f"{u[0]} - {u[1]} ({u[2]})" for u in users])
    bot.reply_to(message, response or "Пользователи отсутствуют.")

# Запуск бота
if __name__ == '__main__':
    bot.polling()
    db.close()