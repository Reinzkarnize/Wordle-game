import random
import time
import sys

# each of our text files contains 1000 words
LISTSIZE = 1000

# values for colors and score (EXACT == right letter, right place; CLOSE == right letter, wrong place; WRONG == wrong letter)
EXACT = 2
CLOSE = 1
WRONG = 0

# ANSI color codes for boxed in letters
GREEN = "\033[38;2;255;255;255;1m\033[48;2;106;170;100;1m"
YELLOW = "\033[38;2;255;255;255;1m\033[48;2;201;180;88;1m"
RED = "\033[38;2;255;255;255;1m\033[48;2;220;20;60;1m"
RESET = "\033[0;39m"

def print_slow(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_guess(wordsize):
    # ensure users actually provide a guess that is the correct length
    while True:
        guess = input(f"Input a {wordsize}-letter word: ")

        # check if guess has the correct length
        if len(guess) == wordsize:
            # check if all characters are lowercase
            if all(c.islower() for c in guess):
                return guess

def check_word(guess, wordsize, status, choice):
    score = 0

    # compare guess to choice and score points as appropriate, storing points in status
    for i in range(wordsize):
        for j in range(wordsize):
            # if char in guess is in the correct spot, add EXACT to status[i]
            if guess[i] == choice[i]:
                status[i] = EXACT

            # if char in guess is in choice but in the wrong spot, add CLOSE to status[i]
            elif guess[i] == choice[j]:
                status[i] = CLOSE

    # sum the values in status to calculate the score
    score = sum(status)

    return score

def print_word(guess, wordsize, status):
    # print word character-for-character with correct color coding
    for i in range(wordsize):
        if status[i] == EXACT:
            print(GREEN + guess[i] + RESET, end='')
        elif status[i] == CLOSE:
            print(YELLOW + guess[i] + RESET, end='')
        else:
            print(RED + guess[i] + RESET, end='')

    print()

def main():
    print_slow(GREEN + 'This is WORDLE GAME' + RESET)
    print()
    wordsize = int(input('Choose a word size (5 - 8): '))
    print()

    # ensure wordsize is either 5, 6, 7, or 8
    if wordsize not in [5, 6, 7, 8]:
        print('Error: wordsize must be either 5, 6, 7, or 8')
        return

    # open correct file, each file has exactly LISTSIZE words
    wl_filename = f'{wordsize}.txt'
    try:
        with open(wl_filename, 'r') as wordlist:
            options = [word.strip() for word in wordlist]
    except FileNotFoundError:
        print(f'Error opening file {wl_filename}.')
        return

    # pseudorandomly select a word for this game
    choice = random.choice(options)

    # allow one more guess than the length of the word
    guesses = wordsize + 1
    won = False

    # print greeting, using ANSI color codes to demonstrate
    print(f'You have {guesses} tries to guess the {wordsize}-letter word I\'m thinking of')

    # main game loop, one iteration for each guess
    for i in range(guesses):
        # obtain user's guess
        guess = get_guess(wordsize)

        # array to hold guess status, initially set to zero
        status = [WRONG] * wordsize

        # calculate score for the guess
        score = check_word(guess, wordsize, status, choice)

        print(f'Guess {i + 1}: ', end='')

        # print the guess
        print_word(guess, wordsize, status)

        # if they guessed it exactly right, terminate the loop
        if score == EXACT * wordsize:
            won = True
            break

    # print the game's result
    if won:
        print('You won!')
    else:
        print(f'You lose :C the answer is {choice}')

if __name__ == '__main__':
    main()
