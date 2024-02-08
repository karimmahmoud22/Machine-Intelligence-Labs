def log(n):
	x, xn = 0, 1
	while x - xn > 10e-10 or x - xn < -10e-10 :
		x, xn = xn, xn - (1 - n/(2**xn))/0.693147181
	return xn