from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import json
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Assalomu alaykum! Chayla botga xush kelibsiz.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
