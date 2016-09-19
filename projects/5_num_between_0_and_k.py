"""
count the number of 2s between 0 and N?
 => From 2 to 99. There are 20 

 1 digit ==> 1 * 10^0 = 1
 2 digit ==> 1 * 10^1 + 10 * 10^0 = 20
 3 digit ==> 1 * 10^2 + 10 * 10^1 + 100 * 10^0= 20

Formula: f * 10^(l-1)*l
"""
def find_number_of_k_0_to_n(n, k):
	original_num = n
	power = 1
	counter = 0
	i = 0

	while(n > 0):
		d = n % 10
		n = n/10
		counter = counter + d * (power * i)/10
		if (d>k):
			counter = counter + power
		elif (d==k):
			counter = counter + original_num % power + 1
		power = power * 10
		i = i+1
	return counter

print find_number_of_k_0_to_n(999, 2)


