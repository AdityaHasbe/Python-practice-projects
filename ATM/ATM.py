# project 1: ATM
import time
def deposit(amt_to_be_deposited):
    print(f"You have deposited {amt_to_be_deposited:.2f}")
    time.sleep(1)
    print(f"Your current savings is {balance+amt_to_be_deposited:.2f}")
    
def withdraw(amt_to_be_withdrawn):
    print(f"You have withdrawn {amt_to_be_withdrawn:.2f}")
    time.sleep(1)
    print(f"Your current savings is {balance-amt_to_be_withdrawn:.2f}")
    
def check_balance():
    print(f"Your current balance is {balance:.2f}")
    

balance = 0
while True:
    
    print("\n\n\nWelcome to the ATM")
    print("******************")
    print("1. Withdraw")
    print("2. Deposit")
    print("3. Check Balance")
    print("4. Exit")
    try: 
        choice = int(input("Enter (1-4): "))
    except ValueError:
        print("Invalid input")
        continue
    
    if choice ==4:
        print("Thanks for using our ATM, see you again.")
        break

    elif choice ==1:
        try:
            amt_to_be_withdrawn = float(input("Enter amount to be withdrawn: "))
            if amt_to_be_withdrawn > balance:
                print("Insufficient balance")
            else:
                withdraw(amt_to_be_withdrawn)
                
                balance-=amt_to_be_withdrawn
        except ValueError:
            print("Invalid input")
    elif choice ==2:
        amt_to_be_deposited = float(input("Enter amount to be deposited: "))
        if amt_to_be_deposited>0:
            deposit(amt_to_be_deposited)
            balance+=amt_to_be_deposited
        else:
            print("Invalid amount")
    else:
        check_balance()
