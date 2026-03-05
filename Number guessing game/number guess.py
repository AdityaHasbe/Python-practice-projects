# project 2. number guessing game

import random

perfect = random.randint(1,10)

while True:
    try:
        guess = int(input("Enter a guess from 1 to 10 (both inclusive): "))
        if guess == perfect:
            print("You got it!")
            break
        elif guess < perfect:
            print("Go higher")
        elif guess > perfect:
            print("Go lower")
    except ValueError:
        print("Invalid input")