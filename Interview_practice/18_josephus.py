"""
Josephus problem
circular round killing the nth person
"""

def josephus(n, k):
	if n == 1:
		return 1
	return (josephus(n - 1, k) + k-1) % n + 1;

print josephus(14, 2)