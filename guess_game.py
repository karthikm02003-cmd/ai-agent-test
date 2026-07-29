# guess_game.py

import random

def guess_the_number():
    """
    Plays a guess the number game where the computer picks a number
    and the user has to guess it.
    """
    print("-----------------------------------------")
    print("  Welcome to the Guess the Number Game!  ")
    print("-----------------------------------------")
    print("I'm thinking of a number between 1 and 100.")
    print("Can you guess what it is?")

    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    guesses = 0
    guess = None # Initialize guess to a value that won't match secret_number

    while guess != secret_number:
        try:
            # Get user input
            user_input = input("Enter your guess: ")
            guess = int(user_input)
            guesses += 1

            # Provide feedback
            if guess < 1 or guess > 100:
                print("Your guess is out of the valid range (1-100). Try again.")
            elif guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number {secret_number} in {guesses} guesses!")
        except ValueError:
            print("Invalid input. Please enter a whole number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    print("\nThanks for playing!")

# This ensures that guess_the_number() is called only when the script is executed directly
if __name__ == "__main__":
    guess_the_number()