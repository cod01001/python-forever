from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


start = types.ReplyKeyboardMarkup(resize_keyboard=True)
info = types.KeyboardButton('Информация')
stats = types.KeyboardButton('Статистика')
razrab = types.KeyboardButton('Разработчик')
pogoda = types.KeyboardButton('Погода')


start.add(info,stats,razrab,pogoda)



stats = InlineKeyboardMarkup()
stats.add(InlineKeyboardButton(f'Да', callback_data='join'))
stats.add(InlineKeyboardButton(f'Нет', callback_data='cancel'))
stats.add(InlineKeyboardButton(f'У вас наливают?', callback_data='pour'))


