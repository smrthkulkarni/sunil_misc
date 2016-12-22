"""
Linked list to complete binary tree
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

def print_list(list_val):
	if list_val:
		print str(list_val.value),
		print_list(list_val.right)


class TreeNode(object):
	def __init__(self, val, left=None, right = None):
		self._left = left
		self._value = val
		self._right = right

	@property
	def left(self):
	    return self._left
	@left.setter
	def left(self, value):
	    self._left = value

	@property
	def value(self):
	    return self._value
	@value.setter
	def value(self, value):
	    self._value = value

	@property
	def right(self):
	    return self._right
	@right.setter
	def right(self, value):
	    self._right = value

def create_tree_node(val):
	return TreeNode(val)

class Queue(object):
	def __init__(self, max_size_of_queue):
		self.queue = None
		self.tail_queue= None
		self.max_size = max_size_of_queue
		self.queue_size = 0

	@property
	def queue(self):
		return self._queue

	@queue.setter
	def queue(self, val):
		self._queue = val

	@property
	def max_size(self):
		return self._max_size

	@max_size.setter
	def max_size(self, val):
		self._max_size = val

	def enqueue(self, val):
		if self.queue_size > self.max_size:
			print "Queue is full"
		else:
			self.node_end_insertion(val)
			self.queue_size = self.queue_size + 1
		return self.queue

	def dequeue(self):
		val = None
		if self.queue_size == 0:
			print "Queue is empty"
		else:
			val = self.node_front_removal()
			self.queue_size = self.queue_size - 1
		return val

	def node_end_insertion(self, val):
		if not self.queue:
			self.queue = create_node(val)
			self.tail_queue = self.queue
		else:
			new_node = create_node(val)
			self.tail_queue.right = new_node
			self.tail_queue = new_node

	def node_front_removal(self):
		val = None
		if self.queue:
			val = self.queue.value
			if self.queue_size == 1:
				self.queue = None
			else:
				self.queue = self.queue.right
		return val

	def print_queue_val(self):
		tmp = self.queue
		while(tmp):
			print tmp.value
			tmp = tmp.right


def traverse_linked_list(head, queue):
	while head:
		parent_node = queue.dequeue()

		left_child = None
		right_child = None
		
		left_child = create_tree_node(head.value)
		head = head.right
		queue.enqueue(left_child)

		if head:
			right_child = create_tree_node(head.value)
			head = head.right
			queue.enqueue(right_child)
		
		parent_node.left = left_child
		parent_node.right = right_child
	
def main():
	linked_list = create_linked_list([10, 12, 15, 25, 30, 36])
	print "Linked list"
	print print_list(linked_list)

	queue = Queue(10)
	root = create_tree_node(linked_list.value)
	queue.enqueue(root)
	

	queue.print_queue_val()
	
	traverse_linked_list(linked_list.right, queue)


	print "Traversal"
	print root.value
	print root.left.value
	print root.right.value
	print root.left.left.value
	print root.left.right.value
	print root.right.left.value	

if __name__ == "__main__":
	main()