from aiogram import Bot, types
from aiogram.utils import executor
import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

import config
import keyboard
import logging

import requests
import pprint
import datetime

storage = MemoryStorage()
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO,
                    )



def get_meather(city,open_weather_map):
    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.open_weather_map}&units=metric'
        )
        data = r.json()
        #pprint.pprint(data)

        city_name = data['name']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        print(f'''погода в городе:{city_name}
температура:{temp}С°
влажность:{humidity}%
давление:{pressure} мм.рт.ст.
скорость ветра:{wind}м/с
восход солнца:{sunset_timestamp}
закат солнца:{sunrise_timestamp} ''')


    except Exception as ex:
        print(ex)
        print('проверьте название города')

def main():
	citi = 'moscow'
	get_meather(citi,config.open_weather_map)


if __name__ =='__main__':
	main()