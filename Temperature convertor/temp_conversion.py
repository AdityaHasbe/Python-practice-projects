print("Welcome to the temperature converter!")
conv = int(input("Which conversion do you want:\n 1. °F to °C,\n 2. °C to °F:\n (Enter 1 or 2): "))
if conv ==1:
    f =  float(input("Enter the temperature in °F: "))
    print(f"The temperature is {round((5/9)*(f-32),2)} °C")
elif conv ==2:
    c= float(input("Enter the temp in °C: "))
    print(f"The temperature is {round(((9/5)*c)+32,2)} °F")
else:
    print("Enter a valid input!")

    