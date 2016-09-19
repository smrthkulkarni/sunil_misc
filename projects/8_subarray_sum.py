"""
Subarray with the given sum

Input: arr[] = {1, 4, 20, 3, 10, 5}, sum = 33
Ouptut: Sum found between indexes 2 and 4

Input: arr[] = {1, 4, 0, 0, 3, 10, 5}, sum = 7
Ouptut: Sum found between indexes 1 and 4

Input: arr[] = {1, 4}, sum = 0
Output: No subarray found
"""
def subarray_sum(arr, sum):
	lptr = 0
	rptr = 0
	total = 0
	for index,val in enumerate(arr):
		total = total + val		
		if total < sum:			
			rptr = rptr + 1
		elif total > sum:
			while(total > sum and lptr<rptr):
				total = total - arr[lptr]
				lptr = lptr + 1
			if(total == sum):
				print "The sum is between "+str(lptr) + " : "+ str(rptr)
				return
		else:
			print "The sum is between "+str(lptr) + " : "+ str(rptr)
			return
	print "No match found"

def main():
	arr = [1, 4, 20, 3, 10, 5]
	sum = 33
	subarray_sum(arr, sum)

if __name__ == "__main__":
	main()
