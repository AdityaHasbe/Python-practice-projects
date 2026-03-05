# project 2. The slot machine

import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

balance = 0
while True:
    
    print("\n\nWelcome to the slot machine")
    print("*****************************")
    print("1. Play")
    print("2. Check Balance")
    print("3. Add balance")
    print("4. Exit")
    try: 
        choice = int(input("Enter (1-3): "))
    except ValueError:
        print("Invalid input")
        continue
    if choice == 4:
        print("Thanks for using our slot machine, see you again.")
        break
    elif choice == 1:
        try:
            bet = int(input("Enter your bet: "))
        except ValueError:
            print("Invalid input")
        if bet > balance:
            print("Insufficient balance")
        else:
            balance -= bet
            for i in range(15):
                out1= random.choice(["@","#","*"])
                out2= random.choice(["@","#","*"])
                out3= random.choice(["@","#","*"])
                clear_screen()

                print("Spinning the reels...")
                print("*****************************")
                print(out1, end="|")
                print(out2, end="|")
                print(out3)
                print("*****************************")
                time.sleep(0.05 +i/100)


            if out1==out2==out3:
                print(f"Jackpot! You won ${bet*2}")
                balance+=bet*2
            else:
                print(f"You lost")
            
    elif choice ==3:
        amt_to_be_added = float(input("Enter amount to be added: "))
        balance+=amt_to_be_added
        print(f"Your current balance is ${balance}")
    else:
        print(f"Your current balance is ${balance}")
       
