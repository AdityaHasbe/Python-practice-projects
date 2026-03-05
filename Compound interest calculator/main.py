
# project 3 : compound interest


def checker(number):
    try:
        number = float(number)
        return True
    except ValueError:
        return False

while True:
    principle  = input("Enter the principle amount: ")
    if checker(principle):
        if float(principle) >0:
            break
        else:
            print("Enter a non negative principle amount.")
    else:
        print("Enter a valid principle amount.")
principle = float(principle)

while True:
    time  = input("Enter the time period (in years): ")
    if time.isdigit():
        break
    else:
        print("Enter a valid time period (in years).")

while True:
    rate = input("Enter the rate: ")
    if checker(rate):
        if float(rate) >0:
            break
        else:
            print("Enter a non negative rate.")
    else:
        print("Enter a valid rate.")
rate = float(rate)

current_balance = principle
for i in range(1, int(time)+1):
    current_balance = current_balance * (1 + rate/ 100)
    print(f"Year {i}: {current_balance:.2f}$")

