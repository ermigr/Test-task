import numpy as np

def df(x):
	return 20*x**19 + 2*x - 20
def f(x):
	return x**20 + x**2 - 20*x

def min(low=-10, high=10, callback=None):
	e = 1e-3
	s = 1e-5
	x_min = None
	for i in range(low,high + 1,1):
		flag = True
		while flag:
			x = i - s * (df(i))
			if np.abs(df(x)) >= np.abs(df(i)):
				flag = False
			i = x
		if np.abs(df(x)) <= e:
			if x_min:
				if f(x_min) > f(x):
					x_min = x	
			else:
				x_min = x
	print (x_min)


min()