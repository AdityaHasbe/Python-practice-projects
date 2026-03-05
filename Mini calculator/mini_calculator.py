# mini python calculator
a = float(input("Enter first number: "))
b = float(input("Enter second number: "))
op = input("Enter operation to perform (+, -, *, /, %, exp): ")

operations = {
    "-": lambda a,b: f"The difference of {a} and {b} is {a - b}",
    "*": lambda a,b: f"The product of {a} and {b} is {a * b}",
    "+": lambda a,b: f"The sum of {a} and {b} is {a + b}",
    "exp": lambda a,b: f"{a} raised to the power of {b} is {a**b}",
    "/": lambda a,b: f"The quotient of {a} and {b} is {a/b}",
    "%": lambda a,b: f"The remainder when {a} is divided by {b} is {a%b}"
    }
if op not in operations:
    print("Invalid operation!")
else:
    if (op == "/" and b==0) or (op=="%" and b==0):
        print("Cannot divide by zero!")
    else:
        print(operations[op])

    # here it is imp to use labda( way of def a func in one line) bcoz it just creates the operations not calcuates all values, when we call it then it calculates the value
    
