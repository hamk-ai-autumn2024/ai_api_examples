import random

# Constants
MIN_NUMBER = 1
MAX_NUMBER = 100

def main():
    """
    Main function to run the number guessing game.
    """
    target_number = random.randint(MIN_NUMBER, MAX_NUMBER)
    attempts = 0

    print(f"Guess the number between {MIN_NUMBER} and {MAX_NUMBER}.")

    while True:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess < MIN_NUMBER or guess > MAX_NUMBER:
                print(f"Please enter a number between {MIN_NUMBER} and {MAX_NUMBER}.")
                continue

            if guess < target_number:
                print("Too low. Try again.")
            elif guess > target_number:
                print("Too high. Try again.")
            else:
                print(f"Congratulations! You've guessed the number in {attempts} attempts.")
                break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()