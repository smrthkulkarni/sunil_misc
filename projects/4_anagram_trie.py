"""
Print all the anagrams together
For example, if the given array is 
	Input -> ["cat", "dog", "tac", "god", "act"]
	Output -> ["cat tac act dog god"]
"""

def sort_within_words(word_lists):
	sorted_words = []
	for word in word_lists:
		w = word.upper()
		w = list(w)
		w.sort()
		sorted_words.append(w)
	return sorted_words

def create_trie(sorted_words):
	root = dict()
	for i, word in enumerate(sorted_words):
		current_dict = root
		for letter in word:
			current_dict = current_dict.setdefault(letter, {})
		current_dict["_end"] = i
	return root

def search_trie(trie, word):
	current_dict = trie
	for letter in word:
		if letter in current_dict:
			current_dict = current_dict.get(letter)
	else:
		if "_end" in current_dict:
			return current_dict["_end"]

def find_anagrams(sorted_words, actual_words):
	trie = create_trie(sorted_words)
	value_dict = dict()
	for i, word in enumerate(sorted_words):
		index = search_trie(trie, word)
		if index not in value_dict:
			value_dict[index] = list()
		value_dict[index].append(actual_words[i])
	for key, value in value_dict.iteritems():
		print value

def main():
	actual_words = ["cat", "dog", "tac", "god", "act"]
	sorted_words = sort_within_words(actual_words)
	find_anagrams(sorted_words, actual_words)

if __name__ == "__main__":
	main()