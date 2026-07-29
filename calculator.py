import random

def play_game():
    secret_number = random.randint(1, 100)
    guesses = 0
    print("I'm thinking of a number between 1 and 100.")
    print("Try to guess it!")

    while True:
        try:
            user_guess = int(input("Enter your guess: "))
            guesses += 1

            if user_guess < 1 or user_guess > 100:
                print("Please guess a number between 1 and 100.")
                continue

            if user_guess < secret_number:
                print("Higher!")
            elif user_guess > secret_number:
                print("Lower!")
            else:
                print(f"Congratulations! You guessed the number {secret_number} in {guesses} guesses.")
                break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

if __name__ == "__main__":
    while True:
        play_game()
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing!")
            break