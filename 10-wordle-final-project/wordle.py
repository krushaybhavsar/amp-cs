"""
[CS2] Wordle- Guess a five-letter secret word in at most six attempts.
"""
import random
from colorama import Back, Style, init

init(autoreset=True)
from wordle_wordlist import get_word_list


def get_feedback(guess: str, secret_word: str) -> str:
    guess = guess.upper()
    guess_list = list(guess)
    secret_word = secret_word.upper()
    secret_word_list = list(secret_word)

    final = ["-"] * 5

    if guess not in get_word_list() or len(guess) != 5:
        return "not a valid guess"

    for i in range(0, len(guess_list)):
        if guess_list[i] == secret_word_list[i]:
            final[i] = guess_list[i]
            secret_word_list[i] = "0"
            guess_list[i] = "0"

    for i in range(0, len(guess_list)):
        if guess_list[i] in secret_word_list and guess_list[i] != "0":
            final[i] = guess_list[i].lower()
            secret_word_list[secret_word_list.index(guess_list[i])] = "0"
            guess_list[i] = "0"

    return "".join(final)


def get_colored_feedback(feedbacks: list[str], secret_word: str) -> str:
    colored_feedback = "\n" + Back.WHITE + "       " + Style.RESET_ALL + "\n"  # top row
    for feedback in feedbacks:
        colored_feedback += Back.WHITE + " "
        for letter in feedback:
            if letter.isupper():
                colored_feedback += Back.GREEN + letter
            elif letter.islower():
                colored_feedback += Back.YELLOW + letter.upper()
            else:
                colored_feedback += Back.BLACK + letter
        colored_feedback += Back.WHITE + " " + Style.RESET_ALL + "\n"
    colored_feedback += Back.WHITE + "       " + Style.RESET_ALL  # bottom row
    return colored_feedback


def get_AI_guess(word_list: list[str], guesses: list[str], feedback: list[str]) -> str:
    """Analyzes feedback from previous guesses (if any) to make a new guess
    Args:
        word_list (list): A list of potential Wordle words
        guesses (list): A list of string guesses, could be empty
        feedback (list): A list of feedback strings, could be empty
    Returns:
     str: a valid guess that is exactly 5 uppercase letters
    """
    if len(guesses) == 0:
        return "SLATE"  # first guess

    letter_freq = {
        "s": 4106,
        "e": 3993,
        "a": 3615,
        "r": 2751,
        "o": 2626,
        "i": 2509,
        "l": 2231,
        "t": 2137,
        "n": 1912,
        "u": 1655,
        "d": 1615,
        "c": 1403,
        "y": 1371,
        "p": 1301,
        "m": 1267,
        "h": 1185,
        "g": 1050,
        "b": 1023,
        "k": 913,
        "f": 707,
        "w": 686,
        "v": 465,
        "z": 227,
        "x": 212,
        "j": 184,
        "q": 79,
    }

    perfect_letters = {}  # letters in right place (letter: index)
    good_letters = {}  # letters in wrong place (letter: index)
    bad_letters = set()  # letters not in word
    all_words = word_list.copy()
    valid_words = []  # words that match feedback
    valid_words_score = {}  # words that match feedback (word: desirbility score)

    for findex, feed in enumerate(feedback):
        for i in range(0, len(feed)):  # perfect_letters
            if feed[i] != "-":
                letter = feed[i].upper()
                if feed[i].isupper():
                    if letter not in perfect_letters.keys():
                        perfect_letters[letter] = set()
                    perfect_letters[letter].add(i)

        for i in range(0, len(feed)):  # good_letters
            if feed[i] != "-":
                letter = feed[i].upper()
                if feed[i].islower():
                    if letter not in good_letters.keys():  # instatiate good_letters if not already
                        good_letters[letter] = set()
                    if letter not in perfect_letters.keys():  # add index to good_letters if not already in perfect
                        good_letters[letter].add(i)
                    for l in good_letters.keys():  # remove index from good_letters if in perfect_letters after new guess
                        if l in perfect_letters.keys() and len(good_letters[l]) > 0:
                            good_letters[l].pop()

        for i in range(0, len(feed)):  # bad_letters
            if feed[i] == "-" and guesses[findex][i] not in perfect_letters.keys() and guesses[findex][i] not in good_letters.keys():
                bad_letters.add(guesses[findex][i])

    for word in all_words:
        valid = True
        if word not in guesses:
            if valid:
                for letter in perfect_letters.keys():
                    for index in perfect_letters[letter]:
                        if word[index] != letter:
                            valid = False
                            break

            if valid:
                for letter in good_letters.keys():
                    if letter in word:
                        for index in good_letters[letter]:
                            if word[index] == letter:
                                valid = False
                                break
                    else:
                        valid = False
                        break

            if valid:
                for letter in bad_letters:
                    if letter in word:
                        valid = False
                        break

            if valid:
                valid_words.append(word)

    if len(valid_words) == 0:
        return random.choice(word_list).upper()
    elif len(valid_words) == 1:
        return valid_words[0]

    for word in valid_words:
        score = 0
        for i, letter in enumerate(word):
            score += letter_freq[letter.lower()]
            # penalize words with multiple letters (less variation in letters)
            if word.count(letter) > 1:
                score -= letter_freq[letter.lower()] * 0.5
        valid_words_score[word] = score

    return sorted(valid_words_score.items(), key=lambda x: x[1], reverse=True)[0][0]


def valid_guess(past_guesses, guess: str) -> str:
    if len(guess) != 5:
        return "Guess must be exactly 5 letters long!"
    if not guess.isalpha():
        return "Guess must contain only letters!"
    if guess.upper() not in get_word_list():
        return "Guess must be a valid word!"
    if guess.upper() in past_guesses:
        return "You already guessed that!"
    return "valid"


def run_game():
    print("\n============== Welcome to Wordle! ==============")
    print("Guess a five-letter word in at most six attempts.")

    secret_word = random.choice(get_word_list()).upper()

    # print(secret_word)  # for testing purposes

    completed = False
    guesses = []
    feedbacks = []

    while not completed and len(guesses) < 6:
        guess_str = f"\nYou have {6 - len(guesses)} guess left." if len(guesses) == 1 else f"\nYou have {6 - len(guesses)} guesses."
        print(guess_str)
        guess = input("Enter guess: ")
        is_valid = valid_guess(guesses, guess)
        if is_valid == "valid":
            feedback = get_feedback(guess, secret_word)
            feedbacks.append(feedback)
            guesses.append(guess.upper())
            print(get_colored_feedback(feedbacks, secret_word))
            # print(get_AI_guess(get_word_list(), guesses, feedbacks))  # for testing purposes
            if feedback.upper() == secret_word:
                completed = True
        else:
            print(is_valid)

    if completed:
        print("You win!")
    else:
        print("You lose!")


if __name__ == "__main__":
    run_game()
