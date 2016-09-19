"""
Binary representation of a number
"""
class Binary(object):
	def __init__(self, val):
		self.n = val
		self.binary_array = []

	def binary(self):
		if self.n == 0:
			return True
		else:
			m = self.n % 2
			self.n = self.n/2
			self.binary_array.append(m)
			return self.binary()

	def print_binary(self):
		self.binary_array.reverse()
		for i in self.binary_array:
			print i, 

def main():
	binary = Binary(16)
	binary.binary()
	binary.print_binary()

if __name__ == "__main__":
	main()

			


