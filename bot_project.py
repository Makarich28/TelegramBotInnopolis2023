import os
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from env import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

code_to_smile = {
"ясно": "\U00002600",
"небольшая облачность": "\U00002601",
"дождь": "\U00002614",
"небольшой дождь": "\U00002614",
"Thunderstorm": "\U000026A1",
"Snow": "\U0001F328",
"Mist": "\U0001F32B"
}

@dp.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, "Привет, я megaBot!")


@dp.message_handler()
async def get_weather(message: types.Message):
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
        if weather == "ясно":
            emodji_weather = code_to_smile['ясно']
        text = f'<strong>Погода {city}</strong>'\
            f'\n\n<i>Населенный пункт: {city}\nСтрана: {data["sys"]["country"]}</i>\n\n<strong>Погода</strong>: <b>{data["weather"][0]["description"]}</b>' \
               f'\n\n<strong>Ощущается как {data["main"]["feels_like"]}°C</strong>' \
               f'\nМинимальная температура: {data["main"]["temp_min"]}°C' \
               f'\nМаксимальная температура: {data["main"]["temp_max"]}°C' \
               f'\n\nСкорость ветра:  {data["wind"]["speed"]} м/с' \
               f'\n\nДавление:  {data["main"]["pressure"]} мм.рт.ст' \
               f'\n\nВлажность:  {data["main"]["humidity"]} %'
        await bot.send_message(message.chat.id, text=text, parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# Нас. Пункт
# Страна
# Погода (эмодзи)
# Мин. Температура
# Макс. Температура
# Ощущается
# Скорость ветра
# Давление
# Влажность

# пасмурно
# ясно
# небольшая облачность
# небольшой снег
# облачно с прояснениями
#снег
#дождь
