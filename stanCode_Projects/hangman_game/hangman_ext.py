"""
File: hangman.py
Name: Harry Kuo
-----------------------------
This program plays hangman game.
Users sees a dashed word, trying to
correctly figure the un-dashed word out
by inputting one character each round.
If the user input is correct, show the
updated word on console. Players have N_TURNS
chances to try and win this game.
"""


import random


# This constant controls the number of guess the player has.
N_TURNS = 7


def main():
    """
    This program demonstrates the hangman game.
    Users have 'N-TURNS' to figure out the un-dashed word.
    """
    ans = random_word()     # create a random word
    hidden_word(ans)        # call the function to replace the word with dash
    count = N_TURNS
    print('You have '+str(count) + ' wrong guesses left.')
    match_ans = ""
    while True:
        guess = input("Your guess: ")
        guess = guess.upper()           # turn the input into capital ones
        match_ans = match_word(ans, match_ans, guess)   # call function to match the un-dashed word and user input
        count = count_memory(ans, guess, count)     # call function to count the chances left
        if count == 0:
            print('You are completely hung : (')
            print_hangman(count)
            break
        elif match_ans.find(ans) != -1:
            print('You win!'+'\n'+'The word was '+ans)
            break
        else:
            print('The word looks like ' + match_ans)
            print('You have ' + str(count) + ' wrong guesses left.')
            print_hangman(count)


def hidden_word(s):
    """
    :param s: str, the un-dashed word
    :return: str, print the word replaced by dash
    """
    ans = ""
    for i in range(len(s)):
        ans += '_'
    print('The word looks like '+ans)


def match_word(s, new_s, guess):
    """
    :param s: str, the un-dashed word
    :param new_s: str, last updated word figured out by user
    :param guess: str, alphabet key-in by user
    :return: str, the latest result of matching
    """
    if s.find(guess) == -1:
        print('There is no '+guess+'\'s in the word.')
    else:
        print('You are correct.')
    if new_s == "":
        ans = ""
        for i in range(len(s)):
            if guess == s[i]:
                ans += s[i]
            else:
                ans += '_'
        return ans
    else:
        ans = ""
        for i in range(len(s)):
            if guess == s[i]:
                ans += s[i]
            else:
                ans += new_s[i]
        return ans


def count_memory(s, guess, n):
    """
    :param s: str, the un-dashed word
    :param guess: str, alphabet key-in by user
    :param n: int, the chances left last time
    :return: int, the chances left by latest guess
    """
    count = n
    if s.find(guess) == -1:
        count += -1
    else:
        pass
    return count


def print_hangman(count):
    """
    :param count: int, the chances left by latest guess
    :return: print hangman
    """
    if count <= 6:
        print('===========')
        print('|'+'\t'+" "+'|')
    if count <= 5:
        print('|'+'\t'+" "+'O')
    if count <= 2:
        print('|'+'\t'+'/'+'|'+'\\')
    elif count <= 3:
        print('|'+'\t'+'/'+'|')
    elif count <= 4:
        print('|'+'\t'+" "+'|')
    if count == 0:
        print('|'+'\t'+'/'+" "+'\\')
    elif count <= 1:
        print('|'+'\t'+'/')


def random_word():
    num = random.choice(range(9))
    if num == 0:
        return "NOTORIOUS"
    elif num == 1:
        return "GLAMOROUS"
    elif num == 2:
        return "CAUTIOUS"
    elif num == 3:
        return "DEMOCRACY"
    elif num == 4:
        return "BOYCOTT"
    elif num == 5:
        return "ENTHUSIASTIC"
    elif num == 6:
        return "HOSPITALITY"
    elif num == 7:
        return "BUNDLE"
    elif num == 8:
        return "REFUND"


#####  DO NOT EDIT THE CODE BELOW THIS LINE  #####
if __name__ == '__main__':
    main()
