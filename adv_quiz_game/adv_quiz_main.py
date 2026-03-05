from qstorage import question_storage
import time
import os
import random

# defining clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#defining main game

def main_game():
    score= 0
    streak = 0
    best_streak = 0
    lifelines_count = 2
    correct_count = 0
    wrong_count = 0


    

    print("Great, lets play the quiz game!")
    time.sleep(1.2)
    clear_screen()
    # choosing cateogry
    print("Choose a cateogry to play:\n1.Science\n2.Geography\n3.Maths\n4.General Knowledge\n5.Mixed")
    while True:
        try:
            cateogry_choice = int(input("Enter your choice (1-5): "))
            break
        except ValueError:
            print("Please enter a valid choice.")
            time.sleep(1.1)

    clear_screen()
    # choosing difficulty
    print("Choose a difficulty level:\n1.Easy\n2.Medium\n3.Hard")
    while True:
        try:
            difficulty_choice = int(input("Enter your choice (1-3): "))
            break
        except ValueError:
            print("Please enter a valid choice.")
            time.sleep(1.1)
    #defining base points 
    if difficulty_choice == 1:
        base_points = 10
    elif difficulty_choice == 2:
        base_points = 20
    else:
        base_points = 30


    question_mapping = {11:"easy_science", 12:"medium_science", 13:"hard_science", 21:"easy_geography", 22:"medium_geography", 23:"hard_geography", 31:"easy_maths", 32:"medium_maths", 33:"hard_maths", 41:"easy_gk", 42:"medium_gk", 43:"hard_gk", 51:"easy_mixed", 52:"medium_mixed", 53:"hard_mixed"}
    cateogry_and_dif_chosen = int(str(cateogry_choice)+str(difficulty_choice))
    current_collection = question_storage[question_mapping[cateogry_and_dif_chosen]]
    random.shuffle(current_collection) # shuffling the questions
    # now current_collection is a list containing shuffled questions and options and answers of user selected difficulty and catoegry

    correct_ans = []
    guesses = []
    for i in current_collection:
        correct_ans.append(i["answer"].lower())
    # ans of shuffled q are stored in correct_ans list
    clear_screen()
    print("Questions loading....")


    
            
        

    # core logic
    time.sleep(1.5)
    for i in current_collection:
        clear_screen()
        print(i["question"], end = "" )
        if lifelines_count >0:
            print("               Lifelines remaining:", lifelines_count, "(Enter lifeline to use)")
        else:
            print("               No lifelines remaianing.") 
        
        print(i["options"])
        while True:
            user_guess = input("Enter your guess (A-D): ").lower()
            if user_guess not in ["a","b","c","d", "lifeline"]:
                print("Please enter a valid option.")
                continue
                
            if user_guess == "lifeline" and lifelines_count!=0:
                wrong_ans = [x for x in ["a","b","c","d"] if x not in i["answer"]]
                random.shuffle(wrong_ans)
                deleted_options = wrong_ans[0:2]
                print(f"Deleted options: {deleted_options}")
                
                lifelines_count -= 1
            elif lifelines_count == 0 and user_guess == "lifeline":   
                print("You have used all lifelines.")
            elif user_guess == i["answer"].lower():
                print("Correct!")
                time.sleep(1.3)
                streak+=1
                correct_count +=1
                if streak > best_streak:
                    best_streak = streak
                guesses.append(user_guess)
                score+= base_points*streak

                break
            else:
                print("Incorrect!")
                time.sleep(1.3)
                wrong_count +=1
                streak = 0
                guesses.append(user_guess)
                break
    time.sleep(1)
    clear_screen()
    print("Quiz completed!")
    print("Your performance report loading...")
    time.sleep(1)
    clear_screen()
    print("Your performance report:")
    print(f"\nYou answered {correct_count} out of 5 questions correctly.")
    print(f"\nYou answered {wrong_count} out of 5 questions incorrectly.")
    accuracy = correct_count*20
    print(f"\nYour accuracy is {accuracy}%")
    print(f"\nYour total score is {score}")
    print(f"\nYour best streak is {best_streak}")
    if accuracy>=90:
        print("\nYou are a Quiz Expert🏆!")
    elif accuracy>=70:
        print("\nYou are a Pro Player 🔥!")
    elif accuracy >=50:
        print("\nYou are a Intermediate Player😎!")
    else:
        print("\nYou are yet a beginner😅!")

    print("Press enter to continue.")
    input()

    clear_screen()

    print("1.Play again\n2.Exit")
    while True:
        try:
            choice_to_playagain = int(input("Enter your choice (1 or 2): "))
            break
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")
            time.sleep(1.3)

    if choice_to_playagain == 2:
        print("See you again!!")
        quit()
    else:
        main_game()

# intro screen

print("Welcome to the Quiz Game!")
print("*************************")
time.sleep(1)

while True:
    print("1.Play\n2.Quit")
    try:
        choice_to_play_initial = int(input("Enter your choice (1 or 2): "))
        break
    except ValueError:
        print("Invalid input. Please enter 1 or 2.")
        time.sleep(1.3)

if choice_to_play_initial == 2:
    print("See you again!!")
    quit()
else:
    main_game()