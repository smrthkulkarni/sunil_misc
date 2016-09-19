"""
Balance Paranthesis
"""

class Node(object):
	def __init__(self, left, val, right):
		self.left = left
		self.value = val
		self.right = right

	@property
	def left(self):
	    return self._left
	@left.setter
	def left(self, value):
	    self._left = value

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


class Stack(object):
	def __init__(self, max_size_of_stack):
		self.stack = None
		self.max_size = max_size_of_stack
		self.stack_size = 0

	@property
	def stack(self):
		return self._stack

	@stack.setter
	def stack(self, val):
		self._stack = val

	@property
	def max_size(self):
		return self._max_size

	@max_size.setter
	def max_size(self, val):
		self._max_size = val

	def push(self, val):
		if self.stack_size > self.max_size:
			print "Stack is full"
		else:
			self.stack = self.node_front_insertion(val)
			self.stack_size = self.stack_size + 1
		return self.stack

	def pop(self):
		val = None
		if self.stack_size == 0:
			print "Stack is empty"
		else:
			val = self.node_front_removal()
			self.stack_size = self.stack_size - 1
		return val

	def node_front_insertion(self, val):
		if not self.stack:
			return create_node(val)
		else:
			new_node = create_node(val)
			new_node.right = self.stack
			return new_node	

	def node_front_removal(self):
		val = None
		if self.stack_size == 1:
			val = self.stack.value
			self.stack = None
		else:
			val = self.stack.value
			self.stack = self.stack.right
		return val

	def find_stack_top(self):
		return self.stack.value

class BalancedParanthesis(object):
	def __init__(self):
		self.stack = Stack(15)

	def push_paranthesis(self, val):
		if val == '(' or val == '{' or val == '[':
			self.stack.push(val)
			return 1

		stack_top = self.stack.find_stack_top()
		if val == ')' and stack_top == "(":
			self.stack.pop()
			return 1
		elif val == '}' and stack_top == "{":
			self.stack.pop()
			return 1
		elif val == ']' and stack_top == "[":
			self.stack.pop()
			return 1
		else:
			return 0

	def exe_balanced_paranthesis(self, exp):
		for i in exp:
			if i in ['[', '{', '(', ')', '}', ']']:
				if not self.push_paranthesis(i):
					return 0
		if self.stack.stack:
			return 0
		return 1

def main():
	bp = BalancedParanthesis()
	exp = '([{x+2}/2]'
	print exp
	if bp.exe_balanced_paranthesis(exp):
		print "Balanced"
	else:
		print "Not Balanced"

if __name__ == "__main__":
	main()
