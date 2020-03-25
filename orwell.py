from numpy.random import choice
from os.path import isfile
import tkinter as tk
import json
import pickle
import pprint
import random

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
		self.board = [	['0', '0', '0', '0'], 
						['0', '0', '0', '0'], 
						['0', '0', '0', '0'], 
						['0', '0', '0', '0']]
		self.score = 0
		self.root = tk.Tk()		
		self.root.title("Orwell")
		self.root.bind("<KeyPress>", self.key)

		self.ALPHABET_FREQ = "./words/freq.json"

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
		if event.keysym == "Right":
			self.board = [self.perform_move(board) for board in self.board]

		if event.keysym == "Left":
			self.board = list(
				map(lambda x: self.perform_move(x[::-1])[::-1], self.board))

		if event.keysym == "Up":
			transpose = lambda l_of_l:[list(l) for l in zip(*l_of_l)]
			self.board = list(map(lambda x: self.perform_move(x[::-1])[::-1],transpose(self.board)))
			self.board = transpose(self.board)

		if event.keysym == "Down":
			transpose = lambda l_of_l:[list(l) for l in zip(*l_of_l)]
			self.board = list(map(self.perform_move,transpose(self.board)))
			self.board = transpose(self.board)

		self.display()

	def spawn(self):
		# Probability distribution
		freq = json.load(open(self.ALPHABET_FREQ))
		p = [x/sum(list(freq.values())) for x in list(freq.values())]
		num = choice([ord(x) for x in freq.keys()], p = p)

		index = [(i, j) for i in range(len(self.board))
				 for j in range(len(self.board))
				 ]  # Generate all possible rows and columns
		index = list(filter(lambda x: self.board[x[0]][x[1]] == '0',
							index))  # Filter out non zero rows

		if len(index) > 0:
			index = random.choice(index)
			self.board[index[0]][index[1]] = chr(num)
			print(chr(num), index)

	def display(self):
		self.spawn()
		for i in range(len(self.board)):
			for j in range(len(self.board)):
				colors = {0:"white", 1:"coral", 2:"tomato", 3:"orange red", 4:"red", 5:"red3", 
				6:"red4", 7:"light goldenrod", 8:"goldenrod", 9:"dark goldenrod", 10:"indian red", 11:"gold"}

				if self.board[i][j] == '0':
					color = colors[0]
				else:
					color = colors[len(self.board[i][j])]

				tk.Label(
					self.root,
					text=self.board[i][j],
					height=3,
					width=10,
					borderwidth=3,
					font = 'Helvetica 14 bold',
					fg = "black",
					bg = color,
					relief="ridge").grid(
						row=i, column=j)

				self.root.update()

		tk.Label(
			self.root,
			text="Score: "+str(self.score)+"\nHighest: "+str(0),
			justify="left"
		).grid(
			row=5,
			column=0,
			sticky="nsew",
			rowspan=4
		)
		
		self.root.update()

if __name__ == "__main__":
	obj = Game()
	# pprint.pprint(obj.board)
	# for move in ["Up", "Down", "Left", "Right"]:
	# 	obj.key(move)
	# 	obj.spawn()
	# 	print()
	# 	pprint.pprint(obj.board)
	obj.display()
	obj.root.mainloop()	
