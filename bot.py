import telebot, wikipedia
from telebot.util import quick_markup, smart_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

wikipedia.set_lang('ru')
bot = telebot.TeleBot('5783944601:AAGi3Kvl9Yy_LE-O2QfMNT2wLS2mIzX_9hM')


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
		wikitext = ny.content
		return wikitext
	except Exception as e:
		return 'В энциклопедии нет информации об этом'


@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id,'Я бот, готов вам помочь\U0001F916')
	bot.send_message(message.chat.id,'Можем просто пообщаться\U0001F648')            


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	global question
	question = message.text
	markup = quick_markup({
		'Дообучить': {'callback_data': 'learn'},
		'Википедия': {'callback_data': 'wiki'}
	}, row_width=2)
	bot.send_message(message.from_user.id, get_generative_replicas(question), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	global question
	if call.data == 'learn':
		bot.send_message(call.message.chat.id, 'Напишите, пожалуйста, как правильно?)\nЯ постараюсь обучиться\U0001F913')
		bot.register_next_step_handler(call.message, wrong)
	elif call.data == 'wiki':
		split_message = smart_split(getwiki(question))
		for text in split_message:
			bot.send_message(call.message.chat.id, text)


def wrong(message):
	a = f'{clean_str(question)}\{clean_str(message.text)} \n'
	with open('dialogues.txt', 'a', encoding='utf-8') as f:
		f.write(a)
	fit()
	bot.send_message(message.from_user.id, 'Я обучился, попробуйте снова\U0001f60A')

bot.infinity_polling()