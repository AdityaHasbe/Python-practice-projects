# project 4. hangman game

import random
import time
print("Welcome to the Hangman Game!")

print("****************************")

time.sleep(2)

print("Rule: You will have 5 lifes at starting and you have to guess a word letter by letter.")

input(">>> Press Enter to start <<<")

words = ["table", "floor", "apple", "heart", "sun", "blueberry", "dog", "mango", "wood", "system"]
correct_word = random.choice(words) 
length = len(correct_word)

guesses = ['_'] * length
lives = 5

# The loop runs as long as there are blanks AND lives left
while '_' in guesses and lives > 0:
    print("\nWord:", " ".join(guesses))
    print(f"Lives remaining: {lives}")
    
    guess = input("Enter a letter: ").lower()

    if guess in correct_word:
        # Update the list with the correct letter
        for i in range(length):
            if guess == correct_word[i]:
                guesses[i] = guess
        print("Good job!")
    else:
        lives -= 1
        print(f"Wrong! '{guess}' is not in the word.")

# End of game checks
if '_' not in guesses:
    print(f"\nCongratulations! You found the word: {correct_word}")
else:
    print(f"\nGame Over! The word was: {correct_word}")