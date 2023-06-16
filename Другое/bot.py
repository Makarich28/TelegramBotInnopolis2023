from aiogram import Bot, Dispatcher, executor, types
import logging
# from aiogram.utils import executor
from aiogram.types import Message
from env import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start", "help"], state='*')
async def start_command_handler(message: Message, state: FSMContext):
    await message.reply(f"Hi, I'm echo bot.\nPlease, say your name")
    await state.set_state("q1")


@dp.message_handler(state="q1")
async def process_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data({"name": name})
    await state.set_state("q2")
    await message.answer("Say your age, please")


@dp.message_handler(state="q2")
async def process_age(message: Message, state: FSMContext):
    age = message.text
    if age.isdigit() and int(age) >= 18:
        age = int(age)
        await state.update_data({"age": int(age)})
        await state.set_state("echo")
        data = await state.get_data()
        if age % 10 == 1 and not age % 100 == 11:
            await bot.send_message(chat_id=message.chat.id, text=f'Hello {data["name"]}, {data["age"]} год')
            await message.answer("Now I'm echo-bot")
        elif age % 10 == 2 or age % 10 == 3 or age % 10 == 4 and not age % 100 == 12 and not age % 100 == 13 and not age % 100 == 14:
            await bot.send_message(chat_id=message.chat.id, text=f'Hello {data["name"]}, {data["age"]} года')
            await message.answer("Now I'm echo-bot")
        else:
            await bot.send_message(chat_id=message.chat.id, text=f'Hello {data["name"]}, {data["age"]} лет')
            await message.answer("Now I'm echo-bot")
    elif age.isdigit() and int(age) < 18:
        await message.answer("you are under 18 years old")
    else:
        await message.answer("This is not number. Try again")


@dp.message_handler(state='echo')
async def dont_know(message: types.Message):
    await message.answer(f'{message.text}, {message.from_user["username"]}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
