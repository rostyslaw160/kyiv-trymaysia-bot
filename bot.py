from aiogram import Bot, Dispatcher, executor

TOKEN = "ТВІЙ_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Бот працює!")

executor.start_polling(dp)
