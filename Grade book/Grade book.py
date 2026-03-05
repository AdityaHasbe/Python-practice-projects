# project 6: The Grade Book
import sys
import time

database = [{'name': "Aditya", 'standard': 12, 'marks': [90, 100, 80]}]

def main():
    while True:
        print("1.View the result of exisiting student\n2.Add a new student\n3.Exit")
        choice = input("Enter your choice: ")

        if choice not in ["1", "2", "3"]:
            print("Invalid choice. Try again.")
            continue
        else:
            choice = int(choice)

        if choice == 1:
            view()
        elif choice == 2:
            add()
        elif choice == 3:
            sys.exit()


def view():
    namestudent = input("Enter students name: ")
    time.sleep(1)

    for x in database:
        if namestudent.lower() == x["name"].lower():
            time.sleep(1)

            print("Student found, printing details")
            for key, value in x.items():
                print(key.capitalize() + ":", value)

            percent = sum(x['marks']) / len(x['marks'])

            if percent >= 33:
                print(f"Percentage: {percent:.2f}% ; Result status: Pass")
            else:
                print(f"Percentage: {percent:.2f}% ; Result status: Fail")
            return

    print("Student not found.")


def add():
    name = ""
    while name == "":
        name = input("Enter student name: ")
        if name == "":
            print("Please enter a name.")

    for x in database:
        if name.lower() == x["name"].lower():
            print("Student already exists.")
            return

    while True:
        try:
            standard = int(input("Enter student standard: "))
            if standard <= 0:
                print("Standard must be greater than 0.")
                continue
            break
        except ValueError:
            print("Enter a valid number.")

    while True:
        try:
            no_of_subjects = int(input("Enter number of subjects: "))
            if no_of_subjects <= 0:
                print("Number of subjects must be greater than 0.")
                continue
            break
        except ValueError:
            print("Enter a valid number.")

    marks_list = []

    for x in range(1, no_of_subjects + 1):
        while True:
            try:
                marks = float(input(f"Enter marks for subject {x}: "))
                marks_list.append(marks)
                break
            except ValueError:
                print("Enter a valid number.")

    database.append({
        "name": name,
        "standard": standard,
        "marks": marks_list
    })
    print("Student added successfully.")

main()
