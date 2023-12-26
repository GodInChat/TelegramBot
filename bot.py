import telebot

bot = telebot.TeleBot("6687358452:AAGr0lOmafiFeFthkzkpMq8QnoLuoM8REKE")

# Показати список команд
def show_commands(message):
    bot.reply_to(message, "/upload - завантажити файл контексту")
    bot.reply_to(message, "/delete - видалити файл контексту")
    bot.reply_to(message, "/ask - задати питання")
    bot.reply_to(message, "/history - переглянути історію запитань")
    bot.reply_to(message, "/clear_history - очистити історію запитань")
    bot.reply_to(message, "/exit - завершити роботу")
    bot.reply_to(message, "/restart - рестарт спілкування")

# Обробник команди /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Вас вітає бот. Оберіть команду:")
    show_commands(message)

# Обробник команди /upload
@bot.message_handler(commands=['upload'])
def upload_file(message):
    # Реалізуйте логіку завантаження файлу тут
    bot.reply_to(message, "Виберіть файл для завантаження.")

# Обробник команди /restart
@bot.message_handler(commands=['restart'])
def restart_conversation(message):
    bot.reply_to(message)

bot.infinity_polling()