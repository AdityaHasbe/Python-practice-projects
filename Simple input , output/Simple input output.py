#project 1 

import sys

name = ""

while not name.isalpha():
    name = input("Enter your name: ")
    
    if name == "":
        print("Please enter a name.")
    elif not name.isalpha():
        print("Enter a valid name (letters only).")
    else:
        print("Valid name!")

while True:
    try:
        age = int(input("Enter your age: "))
        
        if age <= 0:
            print("You aren't born yet.")
            continue
        
        elif age > 100:
            print("You are too old to get a watch.")
            sys.exit()   # Terminates entire program
        
        else:
            break   
            
    except ValueError:
        print("Invalid age, enter a valid age.")


while True:
    try:
        price = float(input("Enter the price of your watch: "))
        
        if price < 0:
            print("Price cannot be negative.")
            continue
        
        else:
            break
            
    except ValueError:
        print("Enter a valid price.")


if price == 0:
    print(f"Hello {name.title()}, you are {age} years old and your watch is free!")
else:
    print(f"Hello {name.title()}, you are {age} years old and your watch costs ${price:.2f}")

