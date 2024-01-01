import asyncio
import logging
import sys
import aiohttp
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold


# Тимчасова надбудова поки я не знаю наш FastAPI
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Припустимо, що у вас є модель Question та функція для взаємодії з базою даних
from models import Question
from database import SessionLocal

app = FastAPI()
# Припустимо, що у FastAPI є endpoint для завантаження файлу, який має URL '/upload_file'
FASTAPI_UPLOAD_URL = 'https://InChat.pp.ua:8000/upload_file'
# Припустимо, що у FastAPI є endpoint для видалення файлу, який має URL '/delete_file'
FASTAPI_DELETE_URL = 'https://InChat.pp.ua:8000/delete_file'
# Припустимо, що у FastAPI є endpoint для прийому питань, який має URL '/ask_question'
FASTAPI_ASK_QUESTION_URL = 'https://InChat.pp.ua:8000/ask_question'


# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6687358452:AAGr0lOmafiFeFthkzkpMq8QnoLuoM8REKE"

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}! \n /upload - завантажити файл контексту \n /delete - видалити файл контексту \n/ask - задати питання \n/history - переглянути історію запитань \n/clear_history - очистити історію запитань\n/exit - завершити роботу \n/restart - рестарт спілкування")
  
@dp.message_handler(Command("upload"))
async def upload_file_command(message: types.Message):
    # Відправляємо запит на сервер FastAPI для отримання посилання на завантаження файлу
    async with aiohttp.ClientSession() as session:
        async with session.post(FASTAPI_UPLOAD_URL) as response:
            if response.status == 200:
                # Отримуємо посилання на завантаження файлу з відповіді сервера
                upload_url = await response.text()
                await message.answer(f"Оберіть файл для завантаження. Використайте посилання: {upload_url}")
            else:
                await message.answer("Сталася помилка при отриманні посилання на завантаження файлу.")

@dp.message_handler(Command("delete"))
async def delete_file_command(message: types.Message):
    # Відправляємо запит на сервер FastAPI для видалення файлу
    async with aiohttp.ClientSession() as session:
        async with session.post(FASTAPI_DELETE_URL) as response:
            if response.status == 200:
                await message.answer("Файл контексту успішно видалено.")
            else:
                await message.answer("Сталася помилка при видаленні файлу контексту.")

@dp.message_handler(Command("ask"))
async def ask_question_command(message: types.Message):
    await message.answer("Введіть ваше питання:")

    # Додаємо фільтр, який відповідає на текстові повідомлення від користувача
    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def process_question(message: types.Message):
        # Відправляємо питання на сервер FastAPI
        question_text = message.text
        async with aiohttp.ClientSession() as session:
            async with session.post(FASTAPI_ASK_QUESTION_URL, json={'question': question_text}) as response:
                if response.status == 200:
                    await message.answer("Ваше питання успішно відправлено.")
                else:
                    await message.answer("Сталася помилка при відправленні питання.")

        # Скасовуємо фільтр, щоб більше не обробляти повідомлення про питання
        dp.message_handlers.unregister(process_question)

@dp.message_handler(Command("history"))
async def history_command(message: types.Message, db: Session = Depends(get_db)):
    # Отримуємо історію питань з бази даних
    questions = db.query(Question).all()

    if questions:
        history_text = "\n".join(question.text for question in questions)
        await message.answer("Історія запитань:\n" + history_text)
    else:
        await message.answer("Історія запитань порожня.")                



async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())