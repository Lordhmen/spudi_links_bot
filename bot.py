from aiogram import types
from aiogram.types import WebAppInfo
from aiogram.utils import executor
import sqlite3
from config import dp, bot

DATABASE_NAME = "users_bd"


def create_database():
    conn = sqlite3.connect(f"{DATABASE_NAME}.sqlite")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, username TEXT, first_name TEXT)''')
    conn.commit()
    conn.close()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Получаем информацию о пользователе
    user_id = str(message.from_user.id)
    username = message.from_user.username
    first_name = message.from_user.first_name

    # Подключаемся к базе данных
    conn = sqlite3.connect(f"{DATABASE_NAME}.sqlite")
    cursor = conn.cursor()

    # Проверяем, есть ли пользователь в базе данных
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        # Добавляем пользователя в базу данных
        cursor.execute("INSERT INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
                       (user_id, username, first_name))
        conn.commit()

    # Закрываем соединение с базой данных
    conn.close()

    keyboard = types.InlineKeyboardMarkup()
    schedule_button = types.InlineKeyboardButton(text="Schedule",
                                                 web_app=WebAppInfo(
                                                     url="https://www.geckoterminal.com/ton/pools/EQAvvszNFKz8pJJqLTBR3wq7oHgkDlRYmVMu-TmPB7tR2PUh"))
    chanel_button = types.InlineKeyboardButton(text="SPUDI", url="https://t.me/spuditon")
    ru_chat_button = types.InlineKeyboardButton(text="RU Chat", url="https://t.me/spudichatru")
    eng_chat_button = types.InlineKeyboardButton(text="ENG Chat", url="https://t.me/spudichat")
    site_button = types.InlineKeyboardButton(text="Site", web_app=WebAppInfo(url="https://spudi.me/"))
    x_button = types.InlineKeyboardButton(text="X (Twitter)", url="https://x.com/spuditon")
    fairlaunch_button = types.InlineKeyboardButton(text="Fairlaunch", web_app=WebAppInfo(url="https://tonraffles.app/jetton/fairlaunch/$SPUDI"))
    keyboard.add(schedule_button)
    keyboard.add(chanel_button)
    keyboard.add(ru_chat_button, eng_chat_button)
    keyboard.add(site_button, x_button)
    keyboard.add(fairlaunch_button)

    await message.answer("Navigation menu", reply_markup=keyboard)


async def startup(dp):
    create_database()
    print("Бот запущен!")


async def shutdown(dp):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
