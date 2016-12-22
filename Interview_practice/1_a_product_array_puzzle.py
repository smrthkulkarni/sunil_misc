"""
A Product Array Puzzle
arr[] = {10, 3, 5, 6, 2}
prod[] = {180, 600, 360, 300, 900}

O(n2) => For each index find the appropriate value
O(n) =>
left -> [1, 10, 30, 150, 900]
right -> [900, 60, 12, 2, 1]
"""
def get_array():
	return [10, 3, 5, 6, 2]

def get_left_product(arr):
	result = []
	tmp_prod = 1
	for id, val in enumerate(arr):
		if id == 0: 
			result.append(tmp_prod)
			tmp_prod = val
		else:
			result.append(tmp_prod)
			tmp_prod = tmp_prod * val
	return result

def get_right_product(arr):
	arr.reverse()
	right_product = get_left_product(arr)
	right_product.reverse()
	return right_product

def get_final_result():
	left = get_left_product(get_array())
	right = get_right_product(get_array())
	print get_array()
	print left 
	print right
	final = []
	for id, val in enumerate(left):
		final.append(val * right[id])
	return final

def main():
	print get_final_result()

if __name__ == "__main__":
	main()
