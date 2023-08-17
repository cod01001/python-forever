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



class meinfo(StatesGroup):
    Q1 = State()


@dp.message_handler(Command('start'), state=None)
async def welcome(message):
    joinedFile = open('user.txt', 'r')
    joinedUsers = set()
    for line in joinedFile:
        joinedUsers.add(line.strip())
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open('user.txt', 'a')
        joinedFile.write(str(message.chat.id) + '\n')
        joinedUsers.add(message.chat.id)

    await bot.send_message(message.chat.id, f"ПРИВЕffТ,*{message.from_user.first_name},* БОТ РАБОТАЕТ",
                           reply_markup=keyboard.start, parse_mode="Markdown")


@dp.message_handler(commands=['rassilka'])
async def rassilka(message):
    if message.chat.id == config.admin:
        await bot.send_message(message.chat.id, f'''*Рассылка началась
        Бот оповетсит когад рассылку закончит*''', parse_mode='Markdown')

        receive_user, block_users = 0, 0
        joinedFile = open('user.txt', 'r')
        jionedUsers = set()
        for line in joinedFile:
            jionedUsers.add(line.strip())
        joinedFile.close()
        print(jionedUsers)

        for user in jionedUsers:
            try:
                print('111')
                await bot.send_photo(user, open('d.png', 'rb'), message.text[message.text.find(' '):])
                receive_user += 1


            except:
                block_users += 1

            await asyncio.sleep(0.4)
        await bot.send_message(message.chat.id, f'''*Рассылка была завершена *
получили сообщение: *{receive_user}*
заблокировали бота: *{block_users}*''', parse_mode='Markdown')


@dp.message_handler(content_types=['text'])
async def get_message(message):

    if message.text == 'Погода':

        await message.answer("Введи название города для получения погоды:")
        await meinfo.Q1.set()
    
        @dp.message_handler(state=meinfo.Q1)
        async def get_weather(message: types.Message, state: FSMContext):
            await state.finish()  # Завершаем текущее состояние

            try:
                r = requests.get(
                    f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={config.open_weather_map}&units=metric'
                )
                data = r.json()
                city_name = data['name']
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                pressure = data['main']['pressure']
                wind = data['wind']['speed']
                sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
                sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
                response = (f"Погода в городе: {city_name}\n"
                            f"Температура: {temp}°C\n"
                            f"Влажность: {humidity}%\n"
                            f"Давление: {pressure} мм.рт.ст.\n"
                            f"Скорость ветра: {wind} м/с\n"
                            f"Восход солнца: {sunrise_timestamp}\n"
                            f"Закат солнца: {sunset_timestamp}")
                await message.answer(response)
            except:
                await message.answer("Ошибка. Проверьте название города.")






    if message.text == 'Информация':
        await bot.send_message(message.chat.id,
                               text='Информация\nБот создан специально для обучения',
                               parse_mode='Markdown')

    if message.text == 'Статистика':
        await bot.send_message(message.chat.id,
                               text="хочешь посмотреть статистику бота?",
                               reply_markup=keyboard.stats, parse_mode='Markdown')


    if message.text == 'Разработчик':
        link1 = open('link.txt', encoding='utf-8')
        link = link1.read()

        text1 = open('text.txt',encoding='utf-8')
        text = text1.read()
        await bot.send_message(message.chat.id,text=f'Создатуль: {link}\n{text}',parse_mode='HTML')




@dp.callback_query_handler(text_contains='join')
async def join(call: types.CallbackQuery):
    if call.message.chat.id == config.admin:
        d = sum(1 for line in open("user.txt"))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Вот статистика бота: *{d}* человек', parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'У тебя нет админки\n Куда ты полез', parse_mode='Markdown')


@dp.callback_query_handler(text_contains='cancle')
async def cancle(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Ты вернулся В главное меню. Жми опять кнопки', parse_mode='Markdown')


@dp.callback_query_handler(text_contains='pour')
async def cancle(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Нет, мы все спортсмены', parse_mode='Markdown')


#---------------------------------------------







if __name__ == '__main__':
    print("Бот запущен!")
    executor.start_polling(dp)