
# project 4: smart shopping cart

import time

print("Welcome to the smart shopping cart!")
print("***********************************")
time.sleep(1)

print("Menu:")
menu = {"pizza": 100, "nachos": 40, "popcorn": 60, "soda": 25, "fries": 40}

# Keeping your original menu display style
for x in range(1, len(menu)+1):
    print(f"{x}. {list(menu.keys())[x-1]} - ${list(menu.values())[x-1]}")

cart = {}
total = 0

while True:
    item = input("Enter the item you want (press q to quit): ").lower()

    if item == "q":
        break

    if item not in menu:
        print("Item not in menu.")
        continue

    while True:
        try:
            quantity = int(input(f"How many {item} do you want? "))
            if quantity <= 0:
                print("Quantity must be greater than 0.")
                continue
            break
        except ValueError:
            print("Enter a valid quantity.")

    # Add or update item quantity
    cart[item] = cart.get(item, 0) + quantity


print("\nItem            Quantity        Price($)")
print("------------------------------------------")

for item, quantity in cart.items():
    price = menu[item] * quantity
    total += price
    print(f"{item:<15} {quantity:<10} {price:>10.2f}")

print("------------------------------------------")
print(f"Your total is ${total:.2f}")
