"""
Implementation of depth first search.
The bookmark has complicated logic to find the cycle. But dfs with back-tracking
is required

Hence here dfs is implemented

		 A
		/ \
	   C   B
	  /   / \
      \  D  E
        \ /
        F


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

def input_adj_list():
	return {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}

def dfs(forest, vertex_visit, stack):
	if stack == None:
		return
	else:
		node = stack.pop()
		if not node:
			return
		if not vertex_visit[node]:
			print node,
			vertex_visit[node] = True
			for adj_node in forest[node]:
				stack.push(adj_node)
		dfs(forest, vertex_visit, stack)


def main():
	start_node = "A"
	forest = input_adj_list()
	vertex_visit = {}
	for key in forest.iterkeys():
		vertex_visit[key] = None
	stack = Stack(100)
	stack.push(start_node)
	dfs(forest, vertex_visit, stack)

if __name__ == "__main__":
	main()
