from telebot import types

menu = types.InlineKeyboardMarkup()
btn_random = types.InlineKeyboardButton(text='Случайная статья', callback_data='random')
btn_search = types.InlineKeyboardButton(text='Поиск', callback_data='search')
menu.add(btn_random, btn_search)