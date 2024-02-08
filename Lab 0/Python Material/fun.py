def fib(n):
	a,b=0,1
	if n < 2:
		return n
	else:
		for _ in range(n-1):
			a,b=b,a+b
		return b
	
def fac(n):
	p = 1
	for i in range(2,n):
		p *= i
	return p