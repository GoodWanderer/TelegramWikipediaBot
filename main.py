import telebot
import wikipedia
import db
import text
import button


bot = telebot.TeleBot(text.token)
db.CreateTable()

@bot.message_handler(commands=['start'])
def start_message(message):

	result = db.FindFlag(message.from_user.id)

	if not result:
		db.AddUser(message.from_user.id)
	else:	
		db.Flag0(message.from_user.id)

	bot.send_message(chat_id=message.from_user.id,
					 text=text.StartMessage,
					 reply_markup=button.menu)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(call):

	if call.data == 'search':
		db.Flag1(call.message.chat.id)

		bot.send_message(call.message.chat.id, 'Введите запрос:')

	elif call.data == 'random':
		db.Flag0(call.message.chat.id)

		wikipedia.set_lang('ru')
		complete = wikipedia.page(wikipedia.random())

		bot.send_message(chat_id=call.message.chat.id, text=complete.title+
													 '\n\n'+complete.summary+
													 '\n\n'+complete.url, reply_markup = button.menu)

@bot.message_handler(content_types=['text'])
def send_message(message):
	result = db.FindFlag(message.chat.id)
	if result == 1:
		db.Flag0(message.chat.id)

		try:
			wikipedia.set_lang('ru')
			search = wikipedia.search(message.text)
			complete = wikipedia.page(search[0])
			
			bot.send_message(message.chat.id, text=complete.title+
											'\n\n'+complete.summary+
											'\n\n'+complete.url, reply_markup=button.menu)
		except Exception:
			bot.send_message(message.chat.id, '404 Страница не найдена :(', reply_markup=button.menu)

bot.polling(none_stop=True, interval=0)