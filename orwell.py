from numpy.random import choice
from os.path import isfile
from functools import partial
from sys import exit
from itertools import chain
from csv import reader
from nltk.stem import WordNetLemmatizer
import tkinter as tk
import datetime
import json
import pickle
import pprint
import random
import re

class Words:
	def __init__(self):
		self.WORDS_PATH = "./words/dictionary.json"
		self.WORDS_COMPRESS = "./words/dictionary.pkl"

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

class TempEvent:
	def __init__(self, value):
		self.keysym = value

class Game:
	def __init__(self):
		self.board = [	['-', '-', '-', '-'], 
						['-', '-', '-', '-'], 
						['-', '-', '-', '-'], 
						['-', '-', '-', '-']]
		self.score = 0
		self.root = tk.Tk()		
		self.root.title("Orwell")
		self.root.bind("<KeyPress>", self.key)

		self.ALPHABET_FREQ = "./words/freq.json"
		self.freq = json.load(open(self.ALPHABET_FREQ))

		self.word_list = Words().pickle_word_list()

		self.highscorefile = "./highscore.csv"
		self.highscore = self.get_high_score()

		self.MEANINGS_PATH = "./words/meanings.json"
		self.meanings = json.load(open(self.MEANINGS_PATH))

		self.meaning_label = tk.Label(
			self.root,
			text="",
			font='Times 9',
			justify="left",
			wraplength=300
		)
		self.meaning_label.grid(row=10, column=0, sticky="s", columnspan=4)


	def get_high_score(self):
		with open(self.highscorefile, 'r') as w:
			read = reader(w)
			return max(int(col[1].replace(',', '')) for col in read)

	def adjust_frequency(self, word):
		alphas = [1 if chr(w+97) in word else 0 for w in range(26)]
		reduce_indexes = [index for index in range(26) if alphas[index]==1]
		increase_indexes = [index for index in range(26) if alphas[index]==0]

		for ri in reduce_indexes:
			CONSTANT = (self.freq[chr(ri+97)]/100)*10
			self.freq[chr(ri+97)] -= CONSTANT
			total_incr = sum([self.freq[chr(ii+97)] for ii in increase_indexes])

			for ii in increase_indexes:
				self.freq[chr(ii+97)] += CONSTANT*(self.freq[chr(ii+97)]/total_incr)

	def click(self, x, y, text):
		if self.board[x][y] in self.word_list:
			self.score += len(self.board[x][y])*100
			self.adjust_frequency(self.board[x][y])
			# print(self.freq)
			old_word = self.board[x][y]
			self.board[x][y] = '-'
			self.display(after_click=True, old_word=old_word)

	def perform_move(self, l):
		# Throws '-' values on the left
		# eg - ['ar', '-', '-', 'c'] -> ['-', '-', 'ar', 'c']
		for i in range(len(l)):
			if l[i] == '-':
				del l[i]
				l.insert(0, '-')

		# If all zeros (i.e. ['-', '-', '-', '-']), then return the list
		if l.count(0) >= 3:
			return l

		# If a combination in dictionary, merge the words
		# ['-', '-', 'ar', 'c'] -> ['-', '-', '-', 'arc']
		n = l[1:]
		for i in range(len(l) - 1):
			if l[i]+n[i] in self.word_list:
				l[i] += n[i]
				l[i + 1] = '-'

		# Again throws '-' values on the left
		for i in range(len(l)):
			if l[i] == '-':
				del l[i]
				l.insert(0, '-')
		return l

	def key(self, event, to_display=True):
		if to_display == False:
			old_board = self.board

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

		if to_display:
			self.display()
		else:
			new_board = self.board
			self.board = old_board
			return new_board

	def spawn(self):
		# Probability distribution
		p = [x/sum(list(self.freq.values())) for x in list(self.freq.values())]
		num = choice([ord(x) for x in self.freq.keys()], p = p)

		index = [(i, j) for i in range(len(self.board))
				 for j in range(len(self.board))
				 ]  # Generate all possible rows and columns
		index = list(filter(lambda x: self.board[x[0]][x[1]] == '-',
							index))  # Filter out non zero rows

		if len(index) > 0:
			index = random.choice(index)
			self.board[index[0]][index[1]] = chr(num)
			# print(chr(num), index)

		elif self.game_over_check() == True:
			self.game_over()

			# Append the current score in the highscore file
			date = datetime.datetime.now().strftime("%d/%m/%y")
			with open(self.highscorefile, 'a') as w:
				w.write(date+','+str(self.score)+'\n')

			exit(0)

		else:
			pass

	def display(self, after_click=False, old_word=None):
		if after_click == False:
			self.spawn()

		for i in range(len(self.board)):
			for j in range(len(self.board)):
				colors = {0:"white", 1:"coral", 2:"tomato", 3:"orange red", 4:"red", 5:"red3", 
				6:"red4", 7:"light goldenrod", 8:"goldenrod", 9:"dark goldenrod", 10:"indian red", 11:"gold"}

				if self.board[i][j] == '-':
					color = colors[0]
				else:
					color = colors[len(self.board[i][j])]

				tk.Button(
					self.root,
					text=self.board[i][j],
					height=2,
					width=6,
					borderwidth=3,
					activebackground="#D3D3D3",
					font = 'Helvetica 14 bold',
					fg = "black",
					bg = color,
					relief="ridge",
					command=partial(self.click, i, j, self.board[i][j])).grid(
						row=i, column=j)

				self.root.update()

		tk.Label(
			self.root,
			text="Score: "+str(self.score)+"\nHighest: "+str(self.highscore),
			font='Helvetica 10 bold',
			justify="left"
		).grid(row=5, column=0, sticky="nsew", rowspan=4)

		tk.Label(
			self.root,
			text="Remember - \nMoving tile goes ahead of the still tile",
			font='Helvetica 10 bold',
			justify="center"
		).grid(row=5, column=1, sticky="nsew", columnspan=4)		
		
		if after_click:
			try:
				meaning = self.find_meaning(old_word)
				self.meaning_label.config(text=str(old_word).upper() + ": " + meaning)
			except:
				self.meaning_label.config(text=str(old_word).upper() + ": No Meaning Found")

		self.root.update()

	def find_meaning(self, old_word):
		if old_word not in self.meanings:
			full_text = self.meanings[WordNetLemmatizer().lemmatize(old_word)]
		else:
			full_text = self.meanings[old_word]

		if len(full_text) <= 10:
			return None
		meanings = [meaning.replace("\n", "").strip() for meaning in re.split('[0-9][.]', full_text) if meaning != "" and len(meaning) >= 5]

		# Adding '1.', '2.' ahead of the meanings
		meanings = [str(index + 1) + ". " + meanings[index] for index in range(len(meanings))]

		return "\n".join(meanings[:2])

	def game_over_check(self):
		if (self.key(TempEvent("Left"), to_display=False) 
			== self.key(TempEvent("Left"), to_display=False) 
			== self.key(TempEvent("Left"), to_display=False) 
			== self.key(TempEvent("Left"), to_display=False)):
			if len([1 for word in list(chain.from_iterable(self.board)) if len(word) > 1]) == 0:
				return True
		else:
			return False

	def game_over(self):
		text = "Game Over! Your score is: " + str(self.score)
		popup = tk.Tk()
		popup.wm_title("Game Over!")
		label = tk.Label(popup, text = text)
		label.pack()
		exitButton = tk.Button(popup, text = "Exit", command = self.root.destroy)
		exitButton.pack()
		self.root.wait_window(popup)

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
