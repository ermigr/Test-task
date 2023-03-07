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