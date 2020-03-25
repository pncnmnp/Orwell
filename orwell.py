import json
from os.path import isfile
import pickle

class Words:
	def __init__(self):
		self.WORDS_PATH = "./words/words.json"
		self.WORDS_COMPRESS = "./words/words.pkl"

	def load_words(self):
		return json.load(open(self.WORDS_PATH))

	def pickle_word_list(self):
		if isfile(self.WORDS_COMPRESS):
			model = pickle.load(open(self.WORDS_COMPRESS, 'rb'))
		else:
			file = open(self.WORDS_COMPRESS, 'wb')
			pickle.dump(self.load_words(), file)
			file.close()
			model = pickle.load(open(self.WORDS_COMPRESS, 'rb'))

		return model

class Game:
	def __init__(self):
		self.board = [['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']]
		self.score = 0

	def perform_move(self, l):
		word_list = Words().pickle_word_list()

		# Throws '0' values on the left
		# eg - ['ar', '0', '0', 'c'] -> ['0', '0', 'ar', 'c']
		for i in range(len(l)):
			if l[i] == '0':
				del l[i]
				l.insert(0, '0')

		# If all zeros (i.e. ['0', '0', '0', '0']), then return the list
		if l.count(0) >= 3:
			return l

		# If a combination in dictionary, merge the words
		# ['0', '0', 'ar', 'c'] -> ['0', '0', '0', 'arc']
		n = l[1:]
		for i in range(len(l) - 1):
			if l[i]+n[i] in word_list:
				l[i] += n[i]
				l[i + 1] = '0'

		# Again throws '0' values on the left
		for i in range(len(l)):
			if l[i] == '0':
				del l[i]
				l.insert(0, '0')
		return l		



if __name__ == "__main__":
	obj = Words()
	l = obj.pickle_word_list()
	print("india" in l)