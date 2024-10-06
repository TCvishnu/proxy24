def startMenu():
    while True:
        print("Enter your choice:")
        print("1: Create a Game Room")
        print("2: Join a Game Room")
        print("3: Exit the Game")
        try:
            choice = int(input(">>> "))

            if choice == 1:
                print("You chose to create a game room.")
                break  
            elif choice == 2:
                print("You chose to join a game room.")
                break 
            elif choice == 3:
                print("Exiting the game. Goodbye!")
                break
            else:
                print("Invalid choice, please choose 1, 2, or 3.\n")
        except ValueError:
            print("Invalid input, please enter a number.\n")


startMenu()