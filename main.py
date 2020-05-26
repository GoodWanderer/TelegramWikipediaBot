# Добавление модулей
import telebot
from telebot import types
import wikipedia
import sqlite3

# Токен Telegram бота
bot = telebot.TeleBot('')

# Создание БД
con = sqlite3.connect("users.db")
cur = con.cursor()

# Создание таблицы
cur.execute("""CREATE TABLE IF NOT EXISTS users(
				id int,
				flag int
)""")

# Закрытие соединения
con.close()

# Создание callback кнопок
markup = types.InlineKeyboardMarkup()
btn_random = types.InlineKeyboardButton(text='Случайная статья', callback_data='random')
btn_search = types.InlineKeyboardButton(text='Поиск', callback_data='search')
markup.add(btn_random, btn_search)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):

	# Подключение к БД
	con = sqlite3.connect("users.db")
	cur = con.cursor()

	# Поиск пользователя в БД
	cur.execute("SELECT * FROM users WHERE id=?", [(message.chat.id)])
	result = cur.fetchall()

	# Если пользоветль не найден, то создать пользователя с флагом 0
	if result == []:
		cur.execute("INSERT INTO users VALUES (?, ?) ", (message.chat.id, 0))

	# Если пользователь найден, то придать флагу значение 0	
	else:	
		sql = "UPDATE users SET flag = ? WHERE id = ?"
		cur.execute(sql, [0, message.chat.id])

	# Сохранение записи в БД и закрытие соединения
	con.commit()
	con.close()

	# Сообщение
	bot.send_message(message.chat.id, 'Приветсвую тебя в Telegram боте - Wikipedia.\n'+
		'Этот бот упростит твой поиск в Wikipedia\n'+
		'Нажми на одну из кнопок, что бы начать.', reply_markup = markup)

# Обработчик нажатия кнопок
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(call):

	# Подключение к БД
	con = sqlite3.connect("users.db")
	cur = con.cursor()

	# Если произошло нажатие на кнопку "Поиск"
	if call.data == 'search':

		# Установка флага равного 1
		sql = "UPDATE users SET flag = ? WHERE id = ?"
		cur.execute(sql, [1, call.message.chat.id])

		# Сообщение
		bot.send_message(call.message.chat.id, 'Введите запрос:')

	# Если произошло нажатие на кнопку "Случайная статья"
	elif call.data == 'random':

		# Установка флага равного 0
		sql = "UPDATE users SET flag = ? WHERE id = ?"
		cur.execute(sql, [0, call.message.chat.id])

		# Поиск случайного запроса в Wikipeadia на русском языке
		wikipedia.set_lang('ru')
		complete = wikipedia.page(wikipedia.random())

		bot.send_message(call.message.chat.id, text = complete.title+'\n\n'+
			complete.summary'\n\n'+
			complete.url, reply_markup = markup)

	# Сохранение записи в БД и закрытие соединения
	con.commit()
	con.close()

# Обработчик введённого текста
@bot.message_handler(content_types=['text'])
def send_message(message):

	# Подключение к БД
	con = sqlite3.connect("users.db")
	cur = con.cursor()

	# Поиск пользователя в БД
	cur.execute("SELECT * FROM users WHERE id=?", [(message.chat.id)])
	result = cur.fetchall()

	# Если флаг пользователя равен 1
	if result[0][1] == 1: 

		# Утановить флаг равный 0
		sql = "UPDATE users SET flag = ? WHERE id = ?"
		cur.execute(sql, [0, message.chat.id])		

		# Обработчик ошибок (Wikipedia может не найти запрос пользователя)
		try:

			# Поиск запроса пользователя в Wikipeadia на русском языке
			wikipedia.set_lang('ru')
			search = wikipedia.search(message.text)
			complete = wikipedia.page(search[0])

			# Сообщение 			
			bot.send_message(message.chat.id, text = complete.title+'\n\n'+
				complete.summary+'\n\n'+
				complete.url, reply_markup = markup)

		except Exception:

			# Сообщение
			bot.send_message(message.chat.id, '404 Страница не найдена :(', reply_markup=markup)

 	# Сохранение записи в БД и закрытие соединения
	con.commit()
	con.close()

# Работа бота в безостановочном режиме
bot.polling(none_stop=True, interval=0)