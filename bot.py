import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from collections import defaultdict
import time

TOKEN = "ВСТАВ_СВІЙ_TOKEN"
ADMIN_ID = 123456789  # <-- твій Telegram ID

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

# --- антиспам ---
user_last_message = defaultdict(int)
SPAM_DELAY = 10  # секунд

# --- /start ---
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Вітаємо!\n\n"
        "Це бот зворотного звʼязку «Київ / Київщина — тримайся! 🇺🇦»\n\n"
        "✍️ Напишіть ваше повідомлення.\n"
        "ℹ️ Ми відповідаємо особисто.\n"
        "🚫 Без координат і оперативної інформації."
    )

# --- прийом повідомлень ---
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    now = time.time()

    # антиспам
    if now - user_last_message[message.from_user.id] < SPAM_DELAY:
        await message.answer("⏳ Будь ласка, не надсилайте повідомлення надто часто.")
        return

    user_last_message[message.from_user.id] = now

    # пересилаємо адміну
    text = (
        f"📩 <b>Нове повідомлення</b>\n\n"
        f"👤 <b>ID:</b> {message.from_user.id}\n"
        f"👤 <b>Імʼя:</b> {message.from_user.full_name}\n\n"
        f"{message.text}"
    )

    await bot.send_message(ADMIN_ID, text)
    await message.answer("✅ Повідомлення отримано. Ми відповімо вам особисто.")

# --- відповідь адміну ---
@dp.message_handler(commands=["reply"])
async def reply_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        _, user_id, reply_text = message.text.split(" ", 2)
        await bot.send_message(int(user_id), reply_text)
        await message.answer("✅ Відповідь надіслано.")
    except:
        await message.answer("❌ Формат: /reply USER_ID текст")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)
