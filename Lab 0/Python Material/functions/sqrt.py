def sqrt(n):
	x, xn = 0, n/2
	while x != xn:
		x, xn = xn, (xn + n/xn)/2
	return xn
		