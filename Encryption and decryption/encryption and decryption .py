# project 5: randomised encryption
import random
import sys
import time

correct = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz1234567890"
key = "".join(random.sample(correct, len(correct)))

def encrypt():
    encryptedmessage = ""
    message = input("Enter the message to be encrypted: ")

    for x in message:
        if x not in correct:
            encryptedmessage += x
            continue
        index = correct.find(x)
        encryptedmessage += key[index]
    print(f"Encrypted message is {encryptedmessage}")
    print("Decryption key is: ","'"+ key+"'", "according to correct sequence","'"+correct+"'")


def decrypt():
    decryptedmessage = ""
    message = input("Enter the message to be decrypted: ")

    for x in message:
        if x not in key:
            decryptedmessage += x
            continue
        index = key.find(x)
        decryptedmessage += correct[index]
    print(f"Decrypted message is {decryptedmessage}")
    pass

while True:
    print("1.Encrypt\n2.Decrypt\n3.Exit")
    choice = input("Enter your choice: ")
    if choice not in ["1", "2", "3"]:
        print("Invalid choice. Try again.")
        continue
    if choice == "3":
        sys.exit()
    elif choice == "2":
        decrypt()
        time.sleep(3)
    elif choice == "1":
        encrypt()
        time.sleep(3)
    else:
        print("Invalid choice. Try again.")

