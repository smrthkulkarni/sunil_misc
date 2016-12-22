"""
Sum of linked list without extra space & modification

Input:
  First List: 5->6->3  // represents number 563
  Second List: 8->4->2 //  represents number 842
Output
  Resultant list: 1->4->0->5  // represents number 1405
"""

class Node(object):
	def __init__(self, left, val, right):
		self.value = val
		self.right = right

	@property
	def val(self):
	    return self._val
	@val.setter
	def val(self, value):
	    self._val = value

	@property
	def right(self):
	    return self._right
	@right.setter
	def right(self, value):
	    self._right = value

def create_node(val):
	return Node(None, val, None)

def create_linked_list(list_val):
	linked_list = None
	head = None
	for id,val in enumerate(list_val):
		if id == 0:
			linked_list = create_node(val)
			head = linked_list
		else:
			linked_list.right = create_node(val)
			linked_list = linked_list.right
	return head

def front_insertion(val, linked_list):
	if not linked_list:
		return create_node(val)
	else:
		new_node = create_node(val)
		new_node.right = linked_list
		return new_node

def find_list_lenght(linked_list):
	if not linked_list:
		return 0
	else:
		return find_list_lenght(linked_list.right) + 1

def position_both_to_same_msb(list_a, list_b, len_a, len_b):
	if len_a > len_b:
		diff_len = len_a - len_b
		for i in xrange(0,diff_len):
			list_a = list_a.right
		return (list_a, list_b)
	else:
		diff_len = len_b - len_a
		for i in xrange(0,diff_len):
			list_b = list_b.right
		return (list_a, list_b)

def linked_list_sum(list_a, list_b, carry, list_sum):
	if list_a:
		carry, list_sum = linked_list_sum(list_a.right, list_b.right, carry, list_sum)
		sum = list_a.value + list_b.value + carry
		unit_digit = sum % 10
		carry = sum/10
		list_sum = front_insertion(unit_digit, list_sum)
	return (carry, list_sum)
	

def add_larger_list_extra_value(longest_list, diff_len, list_sum, carry, count):
	if count != diff_len:
		count = count + 1
		carry, list_sum = add_larger_list_extra_value(longest_list.right, diff_len, list_sum, carry, count)
		sum = longest_list.value + carry
		unit_digit = sum % 10
		carry = sum/10
		list_sum = front_insertion(unit_digit, list_sum)
	return (carry, list_sum)

def print_list(list_val):
	if list_val:
		print str(list_val.value),
		print_list(list_val.right)
	
def main():
	list_a = create_linked_list([5,6,3])
	list_b = create_linked_list([8,4,2, 9, 3])
	print "Linked list A & B"
	print print_list(list_a)
	print print_list(list_b)

	len_a = find_list_lenght(list_a)
	len_b = find_list_lenght(list_b)
	mod_list_a, mod_list_b = position_both_to_same_msb(list_a, list_b, len_a, len_b)
	carry, list_sum = linked_list_sum(mod_list_a, mod_list_b, 0, None)
	if len_a > len_b:
		carry, list_sum = add_larger_list_extra_value(list_a, len_a - len_b, list_sum, carry, 0)
	else:
		carry, list_sum = add_larger_list_extra_value(list_b, len_b - len_a, list_sum, carry, 0)
	if carry:
		list_sum = front_insertion(carry, list_sum)
	print "Sum of linked list"
	print_list(list_sum)

if __name__ == "__main__":
	main()