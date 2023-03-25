import telebot, wikipedia, os
import random
import math
import pandas as pd
import numpy as np
import re, string
import spacy
import speech_recognition as sr
import librosa
import pickle
from funs import funs
from telebot.util import quick_markup
from pydub import AudioSegment
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm

wikipedia.set_lang('ru')
nlp = spacy.load('ru_core_news_sm')
svc = svm.SVC()
r = sr.Recognizer()

TOKEN = '5783944601:AAGi3Kvl9Yy_LE-O2QfMNT2wLS2mIzX_9hM'
bot = telebot.TeleBot(TOKEN)


def str_without_br(text):
	return text.replace('\n', ' ')


def lemmatization(text):
	text = re.sub(f'[{string.punctuation}]', ' ', text)
	return ' '.join(token.lemma_ for token in nlp(text))

vectorizer = TfidfVectorizer(preprocessor=lemmatization, min_df=0.1, max_df=0.9, max_features=1000)


def fit():
	with open('dialogues.txt', encoding='utf-8') as f:
		content = f.read()
	
	replicas = content.split('\n')
	X_text = []
	y = []
	
	for replica in replicas:
		question_answer = replica.split('\\')
		if question_answer[0]:
			X_text.append(question_answer[0])
			y.append(question_answer[1])

	X = vectorizer.fit_transform(X_text)
	svc.fit(X, y)

fit()


def get_generative_replicas(question):
	text_vector = vectorizer.transform([question])
	reply = svc.predict(text_vector)[0]
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
	a = f"{user['text'][message.chat.id]}\{str_without_br(message.text)} \n"
	with open('dialogues.txt', 'a', encoding='utf-8') as f:
		f.write(a)
	fit()
	bot.send_message(message.chat.id, 'Я обучился, попробуйте снова\U0001f60A')


def translator(downloaded_file):
	with open('audio.py', 'wb') as new_file:
		new_file.write(downloaded_file)
	track = AudioSegment.from_file('audio.py')
	track.export('audio.wav', format='wav')

	with sr.AudioFile('audio.wav') as source:
		audio = r.record(source)
		r.adjust_for_ambient_noise(source)

	os.remove('audio.py')
	os.remove('audio.wav')
	return audio


def cut_sample(sample):
	series = []
	for i in sample:
		i = i.tolist()
		series.append(i.index(max(i)))
	series = pd.Series(series)
	good_time = series.value_counts()[:5].index
	sample = pd.DataFrame(sample)
	cut_sample = sample.loc[:, good_time]
	return np.array(cut_sample)


def classificator(downloaded_file):
	with open('audio.py', 'wb') as new_file:
		new_file.write(downloaded_file)
	track = AudioSegment.from_file('audio.py')
	track.export('audio.wav', format='wav')

	y_, sr = librosa.load('audio.wav')
	a = librosa.feature.melspectrogram(y=y_, sr=sr)

	X_test = [cut_sample(a).ravel().tolist()]
	X_test = [[math.log(i, 10) for i in sample] for sample in X_test]

	with open('estimator.py', 'rb') as f:
		estimator = pickle.load(f)

	os.remove('audio.py')
	os.remove('audio.wav')
	return estimator.predict(X_test)



user = {}
user['text'] = {}
user['voice'] = {}

@bot.message_handler(commands=['start'])
def _(message):
	bot.send_message(message.chat.id,'Здравствуйте, я бот\U0001F916')
	bot.send_message(message.chat.id,'Можем просто пообщаться\U0001F648')
	bot.send_message(message.chat.id,'Либо помогу перевести в текст голосовое сообщение\U0001F5E3\U0001F4AC') 


@bot.message_handler(content_types=['text'])
def _(message):
	id = message.chat.id
	user['text'][id] = message.text
	markup = quick_markup({
		'Дообучить': {'callback_data': 'learn'},
		'Википедия': {'callback_data': 'wiki'}
	}, row_width=2)
	bot.send_message(message.chat.id, get_generative_replicas(message.text), reply_markup=markup)
	bot.send_message(message.chat.id, random.choice(funs))


@bot.message_handler(content_types=['audio', 'voice'])
def _(message):
	id = message.chat.id
	if message.audio:
		file_id = message.audio.file_id
	elif message.voice:
		file_id = message.voice.file_id
	file_info = bot.get_file(file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	user['voice'][id] = downloaded_file
	markup = quick_markup({
		'Русский': {'callback_data': 'ru'},
		'Английский': {'callback_data': 'en'}
	}, row_width=2)
	bot.send_message(message.chat.id, 'Выберите язык записи', reply_markup=markup)


classifications = {'0': 'мужской', '1': 'женский'}

@bot.callback_query_handler(func=lambda call: True)
def _(call):
	id = call.message.chat.id
	if call.data == 'learn':
		bot.send_message(id, f"Напишите, пожалуйста, как правильно ответить на {user['text'][id].upper()}?)\nЯ постараюсь обучиться\U0001F913")
		bot.register_next_step_handler(call.message, wrong)
	elif call.data == 'wiki':
		bot.send_message(id, getwiki(user['text'][id]))
	elif call.data == 'ru' or call.data == 'en':
		sex = classifications[classificator(user['voice'][id])[0]]
		bot.send_message(id, f'На записи слышен {sex} голос')
		audiofile = translator(user['voice'][id])
		bot.send_message(id, r.recognize_google(audiofile, language=call.data))

# bot.infinity_polling()