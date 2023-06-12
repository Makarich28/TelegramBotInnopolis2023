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
        text = f'Населенный пункт: {city}\nСтрана: {data["sys"]["country"]}\nПогода: {data["weather"][0]["description"]}' \
               f'\nМинимальная температура: {data["main"]["temp_min"]}°C;' \
               f'\nМаксимальная температура: {data["main"]["temp_max"]}°C;\nОщущается как {data["main"]["feels_like"]}°C' \
               f'Скорость ветра: ' \
               f'\nДавление: {data["main"]["pressure"]} мм.рт.ст' \
               f'\nВлажность: {data["main"]["humidity"]} %'
        await bot.send_message(message.chat.id, text=text)

print(1234567890)

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


# code_to_smile = {
# "Clear": "Ясно \U00002600",
# "Clouds": "Облачно \U00002601",
# "Rain": "Дождь \U00002614",
# "Drizzle": "Дождь \U00002614",
# "Thunderstorm": "Гроза \U000026A1",
# "Snow": "Снег \U0001F328",
# "Mist": "Туман \U0001F32B"
# }
