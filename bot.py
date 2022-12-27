import telebot, wikipedia
from telebot.util import quick_markup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

wikipedia.set_lang('ru')
bot = telebot.TeleBot('TOKEN')


def clean_str(r):
	r = r.lower()
	r = [c for c in r if c.isalpha() or c.isspace() or c == '-']
	return ''.join(r)


def fit():
	with open('dialogues.txt', encoding='utf-8') as f:
		content = f.read()
	
	blocks = content.split('\n')
	dataset = []
	
	for block in blocks:
		replicas = block.split('\\')
		if replicas[0]:
			pair = [clean_str(replicas[0]), replicas[1]]
			dataset.append(pair)
	
	X_text = []
	y = []

	for question, answer in dataset[:10000]:
		X_text += [question]
		y += [answer]

	global vectorizer
	vectorizer = CountVectorizer()
	X = vectorizer.fit_transform(X_text)
	
	global clf
	clf = LogisticRegression()
	clf.fit(X, y)

fit()


def get_generative_replicas(question):
	text_vector = vectorizer.transform([question])
	reply = clf.predict(text_vector)[0]
	return reply


def getwiki(text):
	try:
		ny = wikipedia.page(text)
		wikitext = ny.content[:4096]
		wikishort = ''
		for i in wikitext:
			if i != '=':
				wikishort += i
			else:
				break
		return wikishort
	except Exception:
		return f'В энциклопедии нет информации об {text.upper()}'


def wrong(message):
	a = f'{clean_str(user[message.chat.id])}\{clean_str(message.text)} \n'
	with open('dialogues.txt', 'a', encoding='utf-8') as f:
		f.write(a)
	fit()
	bot.send_message(message.chat.id, 'Я обучился, попробуйте снова\U0001f60A')



user = {}

@bot.message_handler(commands=['start'])
def _(message):
	bot.send_message(message.chat.id,'Я бот, готов вам помочь\U0001F916')
	bot.send_message(message.chat.id,'Можем просто пообщаться\U0001F648')            


@bot.message_handler(content_types=['text'])
def _(message):
	id = message.chat.id
	user[id] = message.text
	markup = quick_markup({
		'Дообучить': {'callback_data': 'learn'},
		'Википедия': {'callback_data': 'wiki'}
	}, row_width=2)
	bot.send_message(message.chat.id, get_generative_replicas(message.text).capitalize(), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def _(call):
	id = call.message.chat.id
	if call.data == 'learn':
		bot.send_message(id, f'Напишите, пожалуйста, как правильно ответить на {user[id].upper()}?)\nЯ постараюсь обучиться\U0001F913')
		bot.register_next_step_handler(call.message, wrong)
	elif call.data == 'wiki':
		bot.send_message(id, getwiki(user[id]))
		bot.send_message(id, len(getwiki(user[id])))

bot.infinity_polling()