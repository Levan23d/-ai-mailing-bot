import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = OpenAI(api_key=OPENAI_API_KEY)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 PPV")],
        [KeyboardButton(text="💋 Флирт")],
        [KeyboardButton(text="💰 Кастом")]
    ],
    resize_keyboard=True
)

def generate(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты пишешь продающие рассылки."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "AI генератор рассылок",
        reply_markup=menu
    )


@dp.message(F.text == "🔥 PPV")
async def ppv(message: Message):
    text = generate("продающая рассылка для продажи горячего видео")
    await message.answer(text)


@dp.message(F.text == "💋 Флирт")
async def flirt(message: Message):
    text = generate("флиртующая рассылка")
    await message.answer(text)


@dp.message(F.text == "💰 Кастом")
async def custom(message: Message):
    text = generate("предложение кастомного видео за 100$")
    await message.answer(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
