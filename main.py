import  random

option = ['scissor','paper','rock']

print("WELCOME TO THE GAME!!")
ready=input("ARE YOU READY?: Y/N \n")
while ready == 'Y' or ready == 'y':
    your_choice=input("Enter your choice rock, paper, scissor or EXIT?:\n ")
    if your_choice == "exit":
        break
    machine_choice = random.choice(option)
    print("MACHINE CHOSE:",machine_choice,"!!")
    if your_choice not in option:
        print("Wrong Input")
        break
    if your_choice == machine_choice:
        print("DRAW")
    elif (your_choice == "rock" and machine_choice == "scissor") or ( your_choice == "paper" and machine_choice == "rock" ) or (your_choice =="scissor" and machine_choice == "paper"):
        print("YOU WIN!!!")
    else:
        print("You Loose!!!")


