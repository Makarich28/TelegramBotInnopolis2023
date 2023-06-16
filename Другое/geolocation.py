import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
API_TOKEN = "6048084971:AAFGBmbKfQiRyezaoEB1AfpxmFJMI3v6TwA"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Define the handler for the /start command
@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    location_button = InlineKeyboardButton(text="Отправить геолокацию", callback_data="send_location")
    keyboard.add(location_button)
    await message.reply("Нажмите на кнопку, чтобы отправить свою геолокацию.", reply_markup=keyboard)


# Define the handler for the Inline button
@dp.callback_query_handler(lambda callback_query: True)
async def process_callback_location(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # Get the user's current location
    location = callback_query.from_user.location
    latitude = location.latitude
    longitude = location.longitude

    # Send the location to the user
    await bot.send_message(
        callback_query.from_user.id,
        f"Ваша геолокация: {latitude}, {longitude}.",
        parse_mode=ParseMode.HTML
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)