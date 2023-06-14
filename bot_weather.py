import os
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from env import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, InputFile

start_i1 = InlineKeyboardButton("Написать вручную", callback_data='start_i1')
start_i2 = InlineKeyboardButton("Геолокация", callback_data='start_i2')
keyboard_location_inline = InlineKeyboardMarkup().insert(start_i1).insert(start_i2)

start_b1 = InlineKeyboardButton("Написать вручную", callback_data='start_i1')
start_b2 = InlineKeyboardButton("Геолокация", callback_data='start_i2')
keyboard_location_Reply = InlineKeyboardMarkup().insert(start_i1).insert(start_i2)

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

code_to_smile = {
    "ясно": "☀",
    "небольшая облачность": "⛅",
    "дождь": "🌧💧☔",
    "небольшой дождь": "💧☔",
    "гроза": "🌩⚡",
    "снег": "🌨❄",
    "туман": "🌫🌫",
    "пасмурно": "☁☁",
    "облачно с прояснениями": "🌤🌤",
    "переменная облачность": "☁☀"
}


@dp.message_handler(commands=['start'], state='*')
async def start(message, state):
    await bot.send_message(message.chat.id, "Привет, я MegaWeatherBot!\nЧтобы узнать погоду,"
                                            " напиши где находишься или подключи геолокацию",
                           reply_markup=keyboard_location_inline)
    await state.set_state("location")
    await bot.send_message(message.chat.id, f'{state}')


@dp.message_handler(state="location_point")
async def get_weather(message: types.Message, state):
    city = message.text.lower()
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?&appid=a009c9ca842efc851186d74154eba196&lang=ru&units=metric&q={city}")
    data = response.json()
    print(data)
    city = city[0].upper() + city[1:]
    if int(str(response)[11:-2]) == 404:
        await bot.send_message(message.chat.id, "Не обнаружено населенного пункта")
    else:
        weather = data["weather"][0]["description"]
        if weather in code_to_smile:
            emodji_weather = code_to_smile[weather]
        else:
            emodji_weather = ""

        text = f'<strong>Погода {city}</strong>' \
               f'\n\n<i>Населенный пункт: {city}\nСтрана: {data["sys"]["country"]}</i>\n\n<strong>' \
               f'Погода</strong>: <b>{data["weather"][0]["description"]}</b>{emodji_weather}' \
               f'\n\n<strong>Температура: {data["main"]["temp"]}</strong>' \
               f'\n<strong>Ощущается как {data["main"]["feels_like"]}°C</strong>' \
               f'\n\nСкорость ветра:  {data["wind"]["speed"]} м/с' \
               f'\n\nДавление:  {data["main"]["pressure"]} мм.рт.ст' \
               f'\n\nВлажность:  {data["main"]["humidity"]} %'
        await bot.send_message(message.chat.id, text=text, parse_mode='HTML')
        if weather == "переменная облачность":
            photo = InputFile(f"погода рисунки/переменная_облачность.jpg")
        elif weather == "облачно с прояснениями":
            photo = InputFile(f"погода рисунки/облачно_с_прояснениями.jpg")
        elif weather == "небольшая облачность":
            photo = InputFile(f"погода рисунки/небольшая_облачность.jpg")
        else:
            photo = InputFile(f"погода рисунки/{weather}.jpg")
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        # await state.set_state("start")


@dp.callback_query_handler(lambda callback: callback.data == "start_i2", state='location')
async def start_i1(callback_query: types.CallbackQuery, state):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Геолокация')
    await state.set_state("geolocation")


@dp.callback_query_handler(lambda callback: callback.data == "start_i1", state='location')
async def start_i1(callback_query: types.CallbackQuery, state):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           'Напиши название любого населенного пункта и я скажу тебе погоду там!')
    await state.set_state("location_point")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
