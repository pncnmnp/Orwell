import json
from os.path import isfile
import pickle
import pprint

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
		self.board = [	['z', 't', 'ar', 'c'], 
						['z', '0', 'e', '0'], 
						['z', '0', 'h', 'lg'], 
						['0', '0', 't', '0']]
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

	def key(self, event):
		if event == "Right":
			self.board = [self.perform_move(board) for board in self.board]

		if event == "Left":
			self.board = list(
				map(lambda x: self.perform_move(x[::-1])[::-1], self.board))

		if event == "Up":
			transpose = lambda l_of_l:[list(l) for l in zip(*l_of_l)]
			self.board = list(map(lambda x: self.perform_move(x[::-1])[::-1],transpose(self.board)))
			self.board = transpose(self.board)

		if event == "Down":
			transpose = lambda l_of_l:[list(l) for l in zip(*l_of_l)]
			self.board = list(map(self.perform_move,transpose(self.board)))
			self.board = transpose(self.board)

if __name__ == "__main__":
	obj = Game()
	pprint.pprint(obj.board)
	for move in ["Up", "Down", "Left", "Right"]:
		obj.key(move)
		print()
		pprint.pprint(obj.board)
