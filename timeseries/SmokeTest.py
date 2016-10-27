from series import TimeSeries

# projecteuler.net/problem=1
# Note: this is decidely *not* the intended purpose of this class.

threes = TimeSeries(range(0,1000,3))
fives = TimeSeries(range(0,1000,5))

s = 0
for i in range(0,1000):
	if i in threes or i in fives:
		s += i

print("sum",s)