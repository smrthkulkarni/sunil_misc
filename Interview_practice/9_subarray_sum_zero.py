"""
9_subarray_with_sum_zero.py
Subarray with the sum having zero

Input: {4, 2, -3, 1, 6}
Output: true 
There is a subarray with zero sum from index 1 to 3.

Input: {4, 2, 0, 1, 6}
Output: true 
There is a subarray with zero sum from index 2 to 2.

Input: {-3, 2, 3, 1, 6}
Output: false
There is no subarray with zero sum.
"""

def subarray_sum(arr, sum):
	lptr = 0
	rptr = 0
	total = 0
	for index,val in enumerate(arr):
		total = total + val
		if(total == sum):
			print "The sum is between "+str(lptr) + " : "+ str(rptr)
			return
		if val == 0:
			print "Zero found at "+ str(index)
			return
		elif val > 0:			
			rptr = rptr + 1
		else:
			rptr = rptr + 1
			if total > sum:
				while(total > sum and lptr<rptr):
					total = total - arr[lptr]
					lptr = lptr + 1
				
	print "No match found"

def main():
	arr = [4, 2, -3, 1, 6]
	sum = 0
	subarray_sum(arr, sum)

	arr = [4, 2, 0, 1, 6]
	subarray_sum(arr, sum)

	arr = [-3, 2, 3, 1, 6]
	subarray_sum(arr, sum)

if __name__ == "__main__":
	main()