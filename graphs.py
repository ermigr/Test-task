ЗАДАНИЕ
Петя путешествует между городами на автомобиле и хочет рассчитать минимальный путь из пункта А в пункт Б, при этом он заправляется только на станциях
в городах, поэтому запас хода между ними ограничен.
Расстояние между двумя городами считается как сумма модулей разности по каждой из координат. Дороги есть между всеми парами городов. 

ФОРМАТ ВВОДА
В первой строке входных данных записано количество городов n.
В следующих n строках даны два целых числа: координаты каждого города. Все города пронумерованы числами от 1 до n в порядке записи во входных данных. 
В следующей строке записано целое положительное число k — максимальное расстояние между городами, которое Петя может преодолеть без дозаправки машины. 
В последней строке записаны два различных числа — номер города А и номер города Б.

ФОРМАТ ВЫВОДА
Если существуют пути, удовлетворяющие описанным выше условиям, то выведите
минимальное количество дорог, которое нужно проехать, чтобы попасть из начальной точки маршрута в конечную.
Если пути не существует, выведите -1.

Пример 1
Ввод                                Вывод

7                                   2
0 0
0 2
2 2
0 -2
2 -2
2 -1
2 1
2
1 3

Пример 2
Ввод                                Вывод

4                                   1
0 0
1 0
0 1
1 1
2
1 4

Пример 3
Ввод                                Вывод

4                                   -1
0 0
2 0
0 2
2 2
1
1 4


with open('input.txt') as f:
	quantity = f.readline().strip()
	cities = []
	for i in range(int(quantity)):
		cities.append([int(i) for i in f.readline().split()])
	distance_possible = int(f.readline())
	from_to = [int(i) for i in f.readline().split()]

cities_neighbors = sorted(cities, key=lambda x: abs(x[0] - cities[from_to[0]-1][0]) +
												abs(x[1] - cities[from_to[0]-1][1]))
weights = {} 

for i in range(len(cities_neighbors)):
	weights[i] = float('inf')
weights[0] = 0

def distance(a, b):
	return (abs(cities_neighbors[b][0] - cities_neighbors[a][0]) +
		    abs(cities_neighbors[b][1] - cities_neighbors[a][1]))

for i, _ in enumerate(cities_neighbors):
	for city in [city for city, _ in enumerate(cities_neighbors) if city > i]:
		if distance(i, city) <= distance_possible:
			weights[city] = min(weights[city], weights[i] + distance(i, city))

countdown = cities_neighbors.index(cities[from_to[1]-1])
ways = 0
if weights[countdown] == float('inf'):
	ways = -1
else:
	while countdown:
		for i in list(weights.keys())[:countdown]:
			if (distance(countdown, i) == weights[countdown] - weights[i] and
			   distance(countdown, i) <= distance_possible):
				countdown = i
				ways += 1
				break
print(ways)
