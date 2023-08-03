import time
import random
from valid_word_list import get_valid_word_list
from AnagramExplorer import AnagramExplorer


def generate_letters(
    fun_factor: int, distribution: str, explorer: AnagramExplorer
) -> list:
    """Generates a list of 7 randomly-chosen lowercase letters which can form at least
    fun_factor unique anagramable words

       Args:
        fun_factor (int): minimum number of unique anagram words offered by the chosen letters
        distribution (str): The type of distribution to use in order to choose letters
                          "uniform" - chooses letters based on a uniform distribution, with replacement
                          "scrabble" - chooses letters based on a scrabble distribution, without replacement
        explorer (AnagramExplorer): helper object used to compute anagrams of letters.

       Returns:
           A set of lowercase letters with length 7

       Example
       -------
       >>>explorer = AnagramExplorer(get_valid_word_list())
       >>>generate_letters(75, "scrabble", explorer)
       ["p", "o", "t", "s", "r", "i", "a"]
    """
    finished = False
    letters = []
    while (
        not finished
    ):  # while loop -> we don't know how many times we'll have to pick to get a fun distribution
        letters = []

        # 1 choose some random letters based on the preferred distribution
        if distribution == "uniform":
            for i in range(7):
                letters.append(chr(random.randint(97, 122)))
        elif distribution == "scrabble":
            options = [x for x in range(97, 123)]
            for i in range(7):
                letter = chr(random.choice(options))
                letters.append(letter)
                options.remove(ord(letter))

        # 2 check how many unique anagram words can be formed from those letters
        possible_words = explorer.get_all_anagrams(letters)

        # 3 decide if there are enough possible words
        if len(possible_words) >= fun_factor:
            finished = True

    # Tip: Start with a predefined list of letters for testing
    # letters = ["p", "o", "t", "s", "r", "i", "a"]

    return letters


def parse_guess(guess: str) -> tuple:
    """Splits an entered guess into a two word tuple with all white space removed

    Args:
     guess: A single string reprsenting the player guess

    Returns:
     A tuple of two words. ("", "") in case of invalid input.

    Examples
    --------
    >>>parse_guess("eat, tea")
    ("eat", "tea")

    >>>parse_guess("eat , tea")
    ("eat", "tea")

    >>>parse_guess("eat,tea")
    ("eat", "tea")

    >>>parse_guess("eat tea")
    ("", "")
    """
    words = guess.strip().split(",")

    if len(words) != 2 or "(" in guess or ")" in guess or '"' in guess:
        return ("", "")

    word1 = words[0].strip()
    word2 = words[1].strip()

    return (word1, word2)


def play_game(time_limit: int, letters: list, explorer: AnagramExplorer) -> list:
    """Plays a single game of AnaGame

    Args:
      time_limit: Time limit in seconds
      letters: A list of valid letters from which the player can create an anagram
      explorer (AnagramExplorer): helper object used to compute anagrams of letters.

    Returns:
       A list of tuples reprsenting all player guesses
    """
    guesses = []
    quit = False

    start = time.perf_counter()  # start the stopwatch (sec)
    stop = start + time_limit

    while time.perf_counter() < stop and not quit:
        guess = input("")
        if guess.strip() == "quit":
            quit = True
        elif guess.strip() == "hint":
            print(f"Try working with: {explorer.get_most_anagrams(letters)}")
        else:
            tuple_guess = parse_guess(guess)
            if len(tuple_guess[0]) > 1:
                guesses.append(tuple_guess)
            else:
                print("Invalid input")

        print(f"{letters} {round(stop - time.perf_counter(), 2)} seconds left")

    print("Thanks for playing Anagame!")

    return guesses


def calc_stats(guesses: list, letters: list, explorer) -> dict:
    """Aggregates several statistics into a single dictionary with the following key-value pairs:
       "valid" - list of valid guesses
       "invalid" - list of invalid/duplicate guesses
       "score" - per the rules of the gameis_valid_anagram_pair
       "accuracy" -  int percentage representing valid player guesses out of all player guesses
       "guessed" - set of unique words guessed
       "not guessed" - set of unique words not guessed
       "skill" - int percentage representing the total number of unique anagram words guessed out of all possible unique anagram words

    Args:
     guesses (list): A list of tuples representing all word pairs guesses by the user
     letters (list): The list of valid letters from which user should create anagrams
     explorer (AnagramExplorer): helper object used to compute anagrams of letters.

    Returns:
     dict: Returns a dictionary with seven keys: "valid", "invalid", "score", "accuracy", "guessed", "not guessed", "skill"

    Example
    -------
    >>>letters = ["p", "o", "t", "s", "r", "i", "a"]
    >>>guesses = [("star","tarts"),("far","rat"),("rat","art"),("rat","art"),("art","rat")]
    >>>explorer = AnagramExplorer(get_valid_word_list())
    >>>calc_score(guesses, letters, explorer)
    {
       "valid":[("rat","art")],
       "invalid":[("star","tarts"),("far","rat"),("rat","art"),("art","rat")],
       "score": 1,
       "accuracy": 20,
       "guessed": { "rat", "art" },
       "not_guessed": { ...73 other unique },
       "skill": 2
    }
    """

    all_anagrams = explorer.get_all_anagrams(letters).copy()

    stats = {}
    stats["valid"] = []  # list of tuples
    stats["invalid"] = []  # list of tuples
    for guess in guesses:
        if (
            explorer.is_valid_anagram_pair(pair=guess, letters=letters)
            and guess not in stats["valid"]
            and (guess[1], guess[0]) not in stats["valid"]
            # and guess[0] not in [x[0] or x[1] for x in stats["valid"]]
            # and guess[1] not in [x[0] or x[1] for x in stats["valid"]]
        ):
            stats["valid"].append(guess)
        else:
            stats["invalid"].append(guess)

    stats["score"] = 0  # total score per the rules of the game
    for v_guess in stats["valid"]:
        stats["score"] += len(v_guess[0]) - 2

    if len(guesses) == 0:
        stats["accuracy"] = 0
    else:
        stats["accuracy"] = int(
            (len(stats["valid"]) / (len(guesses))) * 100
        )  # int percentage representing valid player guesses out of all player guesses

    if len(all_anagrams) == 0:
        stats["skill"] = 0
    else:
        unique_guesses = set()
        for v_guess in stats["valid"]:
            unique_guesses.add(v_guess[0])
            unique_guesses.add(v_guess[1])
        stats["skill"] = int((len(unique_guesses) / len(all_anagrams)) * 100)
    stats["guessed"] = set()  # unique valid guessed words
    for v_guess in stats["valid"]:
        stats["guessed"].add(v_guess[0])
        stats["guessed"].add(v_guess[1])

    stats[
        "not guessed"
    ] = set()  # unique words the player could have guessed, but didn’t

    for word in all_anagrams:
        if word not in stats["guessed"]:
            stats["not guessed"].add(word)

    return stats


def display_stats(stats, explorer: AnagramExplorer):
    """Prints a string representation of the game results"""

    print("------------")
    print(f"Final Score: {stats['score']}")
    print("------------")
    print(f"Accuracy: {round(stats['accuracy'], 2)}%")
    print(f" valid guesses ({len(stats['valid'])}):", end=" ")
    for guess in stats["valid"]:
        print(f"  {guess[0]},{guess[1]}", end=" ")
    print(f"\n invalid guesses ({len(stats['invalid'])}):", end=" ")
    for guess in stats["invalid"]:
        print(f"  {guess[0]},{guess[1]}", end=" ")
    print("\n------------")
    print(f"Skill: {round(stats['skill'], 2)}%")
    print(
        f" unique words you could have guessed ({len(explorer.get_all_anagrams(letters)) - len(stats['guessed'])}):"
    )
    for guess in stats["not guessed"]:
        print(f"  {guess}", end=" ")


if __name__ == "__main__":
    time_limit = 60

    explorer = AnagramExplorer(get_valid_word_list())  # helper object

    letters = generate_letters(100, "scrabble", explorer)

    print("\nWelcome to Anagame!\n")
    print("Please enter your anagrams separated by a comma: eat,tea")
    print("Enter 'quit' to end the game early, or 'hint' to get a useful word\n")
    print(f"You have {time_limit} seconds to guess as many anagrams as possible!")
    print(f"{letters}")

    guesses = play_game(time_limit, letters, explorer)
    stats_dict = calc_stats(guesses, letters, explorer)
    display_stats(stats_dict, explorer)
