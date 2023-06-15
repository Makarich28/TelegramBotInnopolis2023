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
from translate import Translator
from aiogram.dispatcher import FSMContext

start_i1 = InlineKeyboardButton("Write it yourself", callback_data='start_i1')
start_i2 = InlineKeyboardButton("Geolocation", callback_data='start_i2')
keyboard_location_inline = InlineKeyboardMarkup().insert(start_i1).insert(start_i2)

image_button_i1 = InlineKeyboardButton("Yes 👍", callback_data='image_button_i1')
image_button_i2 = InlineKeyboardButton("No 👎", callback_data='image_button_i2')
keyboard_image_inline = InlineKeyboardMarkup().insert(image_button_i1).insert(image_button_i2)

music_button_i1 = InlineKeyboardButton("Yes 👍", callback_data='music_button_i1')
music_button_i2 = InlineKeyboardButton("No 👎", callback_data='music_button_i2')
keyboard_music_inline = InlineKeyboardMarkup().insert(music_button_i1).insert(music_button_i2)

lang_i1 = KeyboardButton("Русский 🇷🇺")
lang_i2 = KeyboardButton("English 🇬🇧")
lang_i3 = KeyboardButton("Français 🇫🇷")
lang_i4 = KeyboardButton("Español 🇪🇸")
lang_i5 = KeyboardButton("Deutsch 🇩🇪")
keyboard_lang = ReplyKeyboardMarkup()
keyboard_lang = keyboard_lang.add(lang_i1).add(lang_i2).add(lang_i3).add(lang_i4).add(lang_i5)
# keyboard_lang = ReplyKeyboardRemove()

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

starting_users = []

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
    "переменная облачность": "☁☀",
    "cielo claro": "☀",
    "2": "⛅",
    "3": "🌧💧☔",
    "4": "💧☔",
    "5": "🌩⚡",
    "6": "🌨❄",
    "7": "🌫🌫",
    "8": "☁☁",
    "9": "🌤🌤",
    "10": "☁☀"
}


@dp.message_handler(commands=['start'], state='*')
async def start(message, state):
    await state.update_data({"chat_id": message.chat.id})
    await bot.send_message(message.chat.id, "Hi, I'm MegaWeatherBot, let's set me up"
                                            "\n You can change the settings at any time")
    starting_users.append(message.from_user.id)
    await bot.send_message(message.chat.id, "Choose the language in which I will speak to you.",
                           reply_markup=keyboard_lang)
    await state.set_state("lang")


@dp.message_handler(commands=["change_language"], state='*')
async def change_language(message, state):
    data_state = await state.get_data()
    translator = Translator(to_lang=data_state["lang"])
    await bot.send_message(message.chat.id, translator.translate("Change the language"),
                           reply_markup=keyboard_lang)
    await state.set_state("lang_change")


@dp.message_handler(state="lang_change")
async def change_lang(message, state):
    if message.text == 'Русский 🇷🇺':
        await bot.send_message(message.chat.id, "Язык успешно изменён на Русский", reply_markup=ReplyKeyboardRemove())
        await state.update_data({"lang": 'ru'})
    elif message.text == 'English 🇬🇧':
        await bot.send_message(message.chat.id, "Language successfully changed to English",
                               reply_markup=ReplyKeyboardRemove())
        await state.update_data({"lang": 'en'})
    elif message.text == 'Français 🇫🇷':
        await bot.send_message(message.chat.id, "La langue a été changée avec succès en français",
                               reply_markup=ReplyKeyboardRemove())
        await state.update_data({"lang": 'fr'})
    elif message.text == 'Español 🇪🇸':
        await bot.send_message(message.chat.id, "Idioma cambiado correctamente a español",
                               reply_markup=ReplyKeyboardRemove())
        await state.update_data({"lang": 'es'})
    elif message.text == 'Deutsch 🇩🇪':
        await bot.send_message(message.chat.id, "Sprache erfolgreich auf Deutsch umgestellt",
                               reply_markup=ReplyKeyboardRemove())
        await state.update_data({"lang": 'de'})
    else:
        await bot.send_message(message.chat.id, "Please select a language from the list of suggested languages")
    await state.set_state("location_point")


@dp.message_handler(commands=["change_settings"], state='*')
async def change_settings(message, state):
    await bot.send_message(message.chat.id, "Choose the language in which I will speak to you.",
                           reply_markup=keyboard_lang)
    await state.set_state("lang")


@dp.message_handler(commands=["place"], state='*')
async def weather(message, state: FSMContext):
    data_state = await state.get_data()
    translator = Translator(to_lang=data_state["lang"])
    await state.set_state("location")
    await bot.send_message(data_state["chat_id"],
                           translator.translate("To find out the weather, send geolocation or text where you are"),
                           reply_markup=keyboard_location_inline)


@dp.message_handler(commands=["help"], state='*')
async def help(message, state):
    data_state = await state.get_data()
    translator = Translator(to_lang=data_state["lang"])
    await bot.send_message(message.chat.id, f'/start - {translator.translate("Getting the bot up and running")}\n\n'
                                            f'/place - {translator.translate("Change how the location is sent (e.g. if you do not want to write the location manually, but send geolocation and vice versa)")}\n\n'
                                            f'/change_language - {translator.translate("Change the language in which I will communicate with you")}\n\n'
                                            f'/change_settings - {translator.translate("Change all settings (send images or not, send playlist or not, change language)")}')


@dp.message_handler(state="location_point")
async def get_weather(message: types.Message, state):
    city = message.text.lower()
    data_state = await state.get_data()
    translator = Translator(to_lang=data_state["lang"])
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?&appid=a009c9ca842efc851186d74154eba196&lang=en&units=metric&q={city}")
    data = response.json()
    print(data)
    city = city[0].upper() + city[1:]
    if int(str(response)[11:-2]) == 404:
        await bot.send_message(message.chat.id, translator.translate("Location not found"))
    else:
        response_emodji = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?&appid=a009c9ca842efc851186d74154eba196&lang=ru&units=metric&q={city}")
        data_emodji = response_emodji.json()
        print(data_emodji)
        weather = data_emodji["weather"][0]["description"]
        print(weather)
        if weather in code_to_smile:
            emodji_weather = code_to_smile[weather]
        else:
            emodji_weather = ""

        text = f'<strong>Weather {city}</strong>' \
               f'\n\n<i>Locality: {city}\nCountry: {data["sys"]["country"]}</i>\n\n<strong>' \
               f'Weather</strong>: <b>{data["weather"][0]["description"]}{emodji_weather}</b>' \
               f'\n\n<strong>Temperature: {data["main"]["temp"]}</strong>' \
               f'\n<strong>Feels like {data["main"]["feels_like"]}°C</strong>\n\n' \
               f'Wind speed:  {data["wind"]["speed"]} m/s' \
               f'\n\nPressure:  {data["main"]["pressure"]} mm Hg' \
               f'\n\nHumidity:  {data["main"]["humidity"]} %'
        translator = Translator(to_lang=data_state["lang"])
        text = translator.translate(text)
        await bot.send_message(message.chat.id, text=text, parse_mode='HTML')
        if data_state["image"]:
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?&appid=a009c9ca842efc851186d74154eba196&lang=ru&units=metric&q={city}")
            data = response.json()
            if weather == "переменная облачность":
                photo = InputFile(f"погода рисунки/переменная_облачность.jpg")
            elif weather == "облачно с прояснениями":
                photo = InputFile(f"погода рисунки/облачно_с_прояснениями.jpg")
            elif weather == "небольшая облачность":
                photo = InputFile(f"погода рисунки/небольшая_облачность.jpg")
            else:
                photo = InputFile(f"погода рисунки/{data['weather'][0]['description']}.jpg")
            await bot.send_photo(chat_id=message.chat.id, photo=photo)


@dp.message_handler(state="geolocation")
async def _(message: types.Message, state):
    latitude = message.location.latitude
    longitude = message.location.longitude
    print(123)
    print(latitude)
    print(longitude)
    await bot.send_location(message.chat.id, latitude=latitude, longitude=longitude)
    data = await state.get_data()


@dp.callback_query_handler(lambda callback: callback.data == "start_i2", state='location')
async def start_i2(callback_query: types.CallbackQuery, state):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Geolocation')
    await state.set_state("geolocation")


@dp.callback_query_handler(lambda callback: callback.data == "start_i1", state='location')
async def start_i1(callback_query: types.CallbackQuery, state):
    await bot.answer_callback_query(callback_query.id)
    data_state = await state.get_data()
    translator = Translator(to_lang=data_state["lang"])
    await bot.send_message(data_state["chat_id"],
                           translator.translate("Write the name of any locality and I'll tell you the weather there!"))
    await state.set_state("location_point")


@dp.callback_query_handler(lambda callback: callback.data == "image_button_i1", state='image')
async def image_i1(callback_query: types.CallbackQuery, state):
    await bot.answer_callback_query(callback_query.id)
    await state.update_data({"image": True})
    data_state = await state.get_data()
    translator = Translator(to_lang=data_state["lang"])
    await bot.send_message(data_state["chat_id"], translator.translate("You have agreed to receive images"))
    await bot.send_message(data_state["chat_id"], translator.translate(
        "Do you want me to send you a playlist of music depending on the weather?"),
                           reply_markup=keyboard_music_inline)
    await state.set_state("music")


@dp.callback_query_handler(lambda callback: callback.data == "image_button_i2", state='image')
async def image_i2(callback_query: types.CallbackQuery, state):
    await bot.answer_callback_query(callback_query.id)
    await state.update_data({"image": False})
    data_state = await state.get_data()
    translator = Translator(to_lang=data_state["lang"])
    await bot.send_message(data_state["chat_id"], translator.translate("You did not agree to receive images"))
    await bot.send_message(data_state["chat_id"], translator.translate(
        "Do you want me to send you a playlist of music depending on the weather?"),
                           reply_markup=keyboard_music_inline)
    await state.set_state("music")


@dp.callback_query_handler(lambda callback: callback.data == "music_button_i1", state='music')
async def start_i1(callback_query: types.CallbackQuery, state):
    await bot.answer_callback_query(callback_query.id)
    data_state = await state.get_data()
    translator = Translator(to_lang=data_state["lang"])
    await bot.send_message(data_state["chat_id"],
                           translator.translate("You have agreed to receive a playlist of music"))
    await state.update_data({"music": "True"})
    await bot.send_message(data_state["chat_id"], translator.translate("To find out the weather, send geolocation or text where you are"),
                           reply_markup=keyboard_location_inline)
    await state.set_state("location")


@dp.callback_query_handler(lambda callback: callback.data == "music_button_i2", state='music')
async def start_i1(callback_query: types.CallbackQuery, state):
    await bot.answer_callback_query(callback_query.id)
    data_state = await state.get_data()
    translator = Translator(to_lang=data_state["lang"])
    await bot.send_message(data_state["chat_id"],
                           translator.translate("You have agreed to receive a playlist of music"))
    await state.update_data({"music": "False"})
    await bot.send_message(data_state["chat_id"],
                           translator.translate("To find out the weather, send geolocation or text where you are"),
                           reply_markup=keyboard_location_inline)
    await state.set_state("location")


@dp.message_handler(state="lang")
async def choose_lang(message, state):
    if message.text == 'Русский 🇷🇺':
        await bot.send_message(message.chat.id, "Язык успешно изменён на Русский", reply_markup=ReplyKeyboardRemove())
        await state.update_data({"lang": 'ru'})
    elif message.text == 'English 🇬🇧':
        await bot.send_message(message.chat.id, "Language successfully changed to English",
                               reply_markup=ReplyKeyboardRemove())
        await state.update_data({"lang": 'en'})
    elif message.text == 'Français 🇫🇷':
        await bot.send_message(message.chat.id, "La langue a été changée avec succès en français",
                               reply_markup=ReplyKeyboardRemove())
        await state.update_data({"lang": 'fr'})
    elif message.text == 'Español 🇪🇸':
        await bot.send_message(message.chat.id, "Idioma cambiado correctamente a español",
                               reply_markup=ReplyKeyboardRemove())
        await state.update_data({"lang": 'es'})
    elif message.text == 'Deutsch 🇩🇪':
        await bot.send_message(message.chat.id, "Sprache erfolgreich auf Deutsch umgestellt",
                               reply_markup=ReplyKeyboardRemove())
        await state.update_data({"lang": 'de'})
    else:
        await bot.send_message(message.chat.id, "Please select a language from the list of suggested languages")
    data_state = await state.get_data()
    translator = Translator(to_lang=data_state["lang"])
    await bot.send_message(message.chat.id, translator.translate("Do you need me to send you pictures depending on the weather?"),
                           reply_markup=keyboard_image_inline)
    await state.set_state("image")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
