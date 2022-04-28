from datetime import datetime

import requests
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

import config
from db import DataBaseManager

try:
    db = DataBaseManager()
except Exception as ex:
    print('[INFO] Error while working with PostgreSQL', ex)

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    reg = State()


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) in db.get_user(user_id):
        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True,
            input_field_placeholder='Введите название города: '
        )
        button = 'Москва'
        keyboard.add(button)
        await message.answer('В каком городе Вы хотите узнать погоду?',
                             reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )
        buttons = ['Согласен', 'Не согласен']
        keyboard.add(*buttons)
        await message.answer('Сначала нужно зарегистрироваться.')
        await message.answer('Вы согласны на обработку персональных данных?',
                             reply_markup=keyboard)
        await Form.reg.set()


@dp.message_handler(state=Form.reg)
async def register(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['reg'] = message.text
        if proxy['reg'] == 'Согласен':
            db.add_user(message.from_user.id, message.from_user.first_name,
                        message.from_user.username)
            await message.reply('Всё готово, Вы зарегистрированы!\n'
                                'Выполните комманду /start ещё раз.')
            await state.finish()
        elif proxy['reg'] == 'Не согласен':
            await message.reply('В таком случае, Вы не можете узнать погоду.\n'
                                'Если передумаете, повторно введите /start')
            await state.finish()
        else:
            await message.reply('Введите "Согласен", либо "Не согласен"')


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}'
            f'&appid={config.WEATHER_TOKEN}&units=metric'
        )
        data = r.json()

        city = data['name']
        current_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = ''

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        await message.reply(
            f'Сегодня: {datetime.now().strftime("%d-%m-%Y %H:%M")}\n'
            f'Погода в городе: {city}\nТемпература: {current_weather}°C {wd}\n'
            f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n'
            f'Ветер: {wind}м/с\nВосход солнца: {sunrise_timestamp}\n'
            f'Закат солнца: {sunset_timestamp}\n'
            f'Продолжительность дня: {length_of_the_day}\n'
        )
    except Exception as e:
        print('[INFO] The user entered an invalid city name', e)
        await message.reply("\U00002620 Проверьте название города \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)
