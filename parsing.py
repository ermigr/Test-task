import csv
import copy
import re

with open('male_names.csv', encoding="utf-8") as f:
	male = []
	reader = csv.reader(f)
	for row in reader:
		male.append(row[0])

with open('female_names.csv', encoding="utf-8") as f:
	female = []
	reader = csv.reader(f)
	for row in reader:
		female.append(row[0])

with open('test_data.csv', encoding="utf-8") as f:
	data = [r for r in csv.reader(f)]

data_update = copy.deepcopy(data)
data_update[0] = 'id line_n role text greeting farewell'.split()
for i, row in enumerate(data_update):
	if i > 0:
		row.append('')
		row.append('')

self_introduction = 'зовут это'.split()
greeting = 'здравствуйте добрый'.split()
company_introduction = 'компания'.split()
farewell = 'свидания хорошего'.split()

for i, row in enumerate(data):
	male_name = ''.join(set(row[3].title().split()) & set(male))
	female_name = ''.join(set(row[3].title().split()) & set(female))
	key_word_self = ''.join(set(row[3].lower().split()) & set(self_introduction))
	key_word_greeting = ''.join(set(row[3].lower().split()) & set(greeting))
	key_word_farewell = ''.join(set(row[3].lower().split()) & set(farewell))
	key_word_company = ''.join(set(row[3].lower().split()) & set(company_introduction))

	male_combination_1 = re.findall(male_name + r'\s(\S+\s)?' + key_word_self, row[3], flags=re.IGNORECASE)
	male_combination_2 = re.findall(key_word_self + r'\s(\S+\s)?' + male_name, row[3], flags=re.IGNORECASE)
	female_combination_1 = re.findall(female_name + r'\s(\S+\s)?' + key_word_self, row[3], flags=re.IGNORECASE)
	female_combination_2 = re.findall(key_word_self + r'\s(\S+\s)?' + female_name, row[3], flags=re.IGNORECASE)

	if i > 0:
		if key_word_greeting:
			print ('Реплика, где менеджер поздоровался.')
			print ('-' + data[i][3] + '\n')
			data_update[i][4] = 1
		else:
			data_update[i][4] = 0
		if male_name and key_word_self and (male_combination_1 or male_combination_2):
			print ('Реплика, где менеджер представил себя.') 
			print ('-' + data[i][3] + '\n')
			print ('Имя менеджера.') 
			print ('-' + male_name + '\n')
			if key_word_company:
				print ('Название компании (только первое слово, остальное пока вручную)')
				print ('-' + ''.join(re.findall(key_word_company + r'\s\S+', data[i][3]))[len(key_word_company) + 1:])
				print ('Реплика с названием компании.')
				print ('-' + data[i][3] + '\n')
		else:
			if female_name and key_word_self and (female_combination_1 or female_combination_2):
				print ('Реплика, где менеджер представил себя.') 
				print ('-' + data[i][3] + '\n')
				print ('Имя менеджера.') 
				print ('-' + female_name + '\n')
				if key_word_company:
					print ('Название компании (только первое слово, остальное пока вручную)')
					print ('-' + ''.join(re.findall(key_word_company + r'\s\S+', data[i][3]))[len(key_word_company) + 1:])
					print ('Реплика с названием компании.')
					print ('-' + data[i][3] + '\n')
		if key_word_farewell:
			print ('Реплика, где менеджер попрощался.')
			print ('-' + data[i][3] + '\n')
			data_update[i][5] = 1
		else:
			data_update[i][5] = 0

greeting = []
farewell = []
for i in range(6):
	greeting.append(0)
	farewell.append(0)
for row in data_update[1:]:
	if row[2] == 'manager':
		greeting[int(row[0])] += row[4]
		farewell[int(row[0])] += row[5]
for i in range(6):
	if not greeting[i] or not farewell[i]:
		print ('В диалоге номер ' + str(i))
	if not greeting[i]:
		print ('-менеджер не поздоровался')
	if not farewell[i]:
		print ('-менеджер не попрощался')
print ('\n')

with open('test_data_copy.csv', 'w', newline='', encoding="utf-8") as f:
	csv.writer(f).writerows(data_update)

with open('test_data_copy.csv', encoding="utf-8") as f:
	reader = csv.reader(f)
	for row in reader:
		print (row)