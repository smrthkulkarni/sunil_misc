"""
The volume of rain water trapped in 2d

[0,1,0,2,1,0,1,3,2,1,2,1]
[0,1,1,2,2,2,2,3,3,3,3,3]
[0,1,1,2,2,2,2,3,3,3,3,3]

         __          |
|  __   |  |__     __|
| |  |\ |     |   |  
"""
def find_rain_log(arr):
	prev_high = -100
	total_log = 0
	tmp_log = 0
	for i in arr:
		if not (prev_high - i > 0):
			prev_high = i
			total_log = total_log + tmp_log
			continue
		else:
			tmp_log = tmp_log + (prev_high - i)
	print total_log

def main():
	find_rain_log([0,1,0,2,1,0,1,3,2,1,2,1])

if __name__ == "__main__":
	main()


