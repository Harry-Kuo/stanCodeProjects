"""
File: boggle.py
Name: Harry Kuo
----------------------------------------

"""

import time

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'


def main():
	"""
	This program will demonstrate how boggle game works.
	"""
	# read the dictionary file into list(word_dictionary)
	word_dictionary = []
	read_dictionary(word_dictionary)

	# to let user input the letters in boggle game and store in the list(word_input)
	word_input = []
	for i in range(4):
		row_input = input(str(i+1)+' row of letters: ')
		if len(row_input) != 7:
			print('Illegal input')
			break
		else:
			lower_row_input = row_input.lower()
			row = lower_row_input.split()
			word_input.append(row)
	start = time.time()
	# to loop over every alphabet in boggle game
	ans_lst = []
	for i in range(4):
		for j in range(4):
			word = word_input[i][j]			# to get the start alphabet
			co_word = [(i, j)]				# to get the coordinate of the beginning alphabet
			boggle(word_dictionary, word_input, word, co_word, i, j, ans_lst)
	print(f'There are {len(ans_lst)} words in total.')
	end = time.time()
	print('----------------------------------')
	print(f'The speed of your boggle algorithm: {end - start} seconds.')


def boggle(word_dictionary, word_input, word, co_word, x, y, ans_lst):
	"""
	:param word_dictionary: list, to store all the vocabulary in an English dictionary
	:param word_input: list, to store the alphabets inputted by the user
	:param word: str, a current status of word being explored
	:param co_word: list, to store the coordinates of all the alphabets inputted by the user
	:param x: int, the coordinate-x of the alphabet
	:param y: int, the coordinate-y of the alphabet
	:param ans_lst: list, to store the words found in boggle game
	:return: print what the recursive function found
	"""
	if len(word) >= 4 and word in word_dictionary and word not in ans_lst:
		ans_lst.append(word)
		print(f'Found \"{word}\"')

	if has_prefix(word_dictionary, word):
		# to find the neighbors of each alphabet
		for i in range(-1, 2):
			for j in range(-1, 2):
				co_x = x + i
				co_y = y + j
				# to examine the boundary of boggle game
				if 0 <= co_x <= 3 and 0 <= co_y <= 3 and (co_x, co_y) not in co_word:
					# choose
					word += word_input[co_x][co_y]
					co_word.append((co_x, co_y))
					# explore
					boggle(word_dictionary, word_input, word, co_word, co_x, co_y, ans_lst)
					# un-choose
					word = word[:len(word)-1]
					co_word.pop()


def read_dictionary(lst):
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
	with open(FILE, 'r') as f:
		for line in f:
			word = line.strip()  		# to clean up the information which is not necessary
			lst.append(word)


def has_prefix(word_dictionary, sub_s):
	"""
	:param word_dictionary: list, to store all the vocabulary in an English dictionary
	:param sub_s: str, the prefix of the word
	:return: bool, to show if there is any words with prefix stored in sub_s
	"""
	for word in word_dictionary:
		if word.startswith(sub_s):
			return True
	return False


if __name__ == '__main__':
	main()
