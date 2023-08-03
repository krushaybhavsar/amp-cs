from itertools import combinations


def get_sorted_hash_dict(corpus: list) -> dict:
    """
    Creates a fast dictionary look-up of all anagrams in a word corpus.
      Keys: tuples of sorted letters
      Values: alphabetized list of words from the corpus which are all anagrams of each other

     Args:
      corpus (list): A list of words which should be considered

     Returns:
      dict: Returns a dictionary with sorted tuple keys that return sorted lists of all anagrams of the key (per the corpus)

     Examples
     ----------
     >>>get_prime_hash_dict(["abed", "abled", "bade", "baled", "bead", "blade"])
     {
         ("a", "b", "d", "e"): ["abed", "bade", "bead"],
         ("a", "b", "d", "e", "l"): ["abled", "baled", "blade"]
     }

    """
    lookup_dict = {}

    for word in corpus:
        sorted_letters = tuple(sorted(word))
        if sorted_letters not in lookup_dict:
            lookup_dict[sorted_letters] = [word]
        else:
            lookup_dict[sorted_letters].append(word)

    return lookup_dict


prime_map = {
    "a": 2,
    "b": 3,
    "c": 5,
    "d": 7,
    "e": 11,
    "f": 13,
    "g": 17,
    "h": 19,
    "i": 23,
    "j": 29,
    "k": 31,
    "l": 37,
    "m": 41,
    "n": 43,
    "o": 47,
    "p": 53,
    "q": 59,
    "r": 61,
    "s": 67,
    "t": 71,
    "u": 73,
    "v": 79,
    "w": 83,
    "x": 89,
    "y": 97,
    "z": 101,
}


def prime_hash(str):
    hash_value = 1
    for letter in str:
        hash_value *= prime_map[letter]
    return hash_value


def get_prime_hash_dict(corpus):
    """
    Creates a fast dictionary look-up of all anagrams in a word corpus.
      Keys: Prime hash values (ie. each letter mapped to a prime number, then multiplied together)
      Values: alphabetized list of words from the corpus which are all anagrams of each other

     Args:
      corpus (list): A list of words which should be considered

     Returns:
      dict: Returns a dictionary with prime hash keys that return sorted lists of all anagrams of the key (per the corpus)

     Examples
     ----------
     >>>get_prime_hash_dict(["abed", "abled", "bade", "baled", "bead", "blade"])
     {
         462: ["abed", "bade", "bead"],
         17094: ["abled", "baled", "blade"]
     }
    """
    lookup_dict = {}

    for word in corpus:
        prime_hash_value = prime_hash(word)
        if prime_hash_value not in lookup_dict:
            lookup_dict[prime_hash_value] = [word]
        else:
            lookup_dict[prime_hash_value].append(word)

    return lookup_dict


def get_most_anagrams(corpus: list) -> list:
    """
    Uses a fast dictionary look-up to explore all anagram combinations in a word corpus.
    This function should return an alphabetized lists of words:
    The returned list contains the alphabetized list of the first word in the alphabetized list of words
     for each anagram group that produces the maximum number of anagrams:

     Args:
      corpus (list): A list of words which should be considered

     Returns:
      most_anagrams (list): A list containing the alphabetized list of the first word in the alphabetized list of words
     for each anagram group that produces the maximum number of anagrams

     Examples
     ----------
     >>>get_most_anagrams(["rat", "mouse", "tar", "art", "chicken", "stop", "pots", "tops" ])
     ['art', 'pots']

    """
    most_anagrams = []

    anagram_dict = get_prime_hash_dict(corpus)

    max_anagrams = 0

    for key in anagram_dict:
        if len(anagram_dict[key]) > max_anagrams:
            max_anagrams = len(anagram_dict[key])

    for key in anagram_dict:
        if len(anagram_dict[key]) == max_anagrams:
            most_anagrams.append(sorted(anagram_dict[key])[0])

    if max_anagrams <= 1 or len(corpus) == 0:
        return []

    return sorted(most_anagrams)


def get_all_anagrams(corpus: list[str]) -> set:
    """Creates a set of all unique words that could have been used to form an anagram pair.
      Words which can't create any anagram pairs should not be included in the set.

      Args:
        corpus (list): A list of words which should be considered

      Returns:
        set: all unique words in wordlist which form at least 1 anagram pair

      Examples
    ----------
    >>>get_all_anagrams(["abed","mouse", "bead", "baled", "abled", "rat", "blade"])
    {"abed",  "abled", "baled", "bead", "blade"}
    """
    all_anagrams = set()

    anagram_dict = get_prime_hash_dict(corpus)

    for key in anagram_dict:
        if len(anagram_dict[key]) > 1:
            for word in anagram_dict[key]:
                all_anagrams.add(word)

    return all_anagrams


if __name__ == "__main__":
    words1 = [
        "abed",
        "abet",
        "abets",
        "abut",
        "acme",
        "acre",
        "acres",
        "actors",
        "actress",
        "airmen",
        "alert",
        "alerted",
        "ales",
        "aligned",
        "allergy",
        "alter",
        "altered",
        "amen",
        "anew",
        "angel",
        "angle",
        "antler",
        "apt",
        "bade",
        "baste",
        "bead",
        "beast",
        "beat",
        "beats",
        "beta",
        "betas",
        "came",
        "care",
        "cares",
        "casters",
        "castor",
        "costar",
        "dealing",
        "gallery",
        "glean",
        "largely",
        "later",
        "leading",
        "learnt",
        "leas",
        "mace",
        "mane",
        "marine",
        "mean",
        "name",
        "pat",
        "race",
        "races",
        "recasts",
        "regally",
        "related",
        "remain",
        "rental",
        "sale",
        "scare",
        "seal",
        "tabu",
        "tap",
        "treadle",
        "tuba",
        "wane",
        "wean",
    ]

    words2 = ["abed", "allergy", "amen", "anew", "angel", "tap", "treadle"]

    print(f"Sorting via the prime hashing function: {sorted(words1, key=prime_hash)}")
    print()
    print(f"Sorted tuple lookup dictionary: {get_sorted_hash_dict(words1)}")
    print(f"Prime hash lookup dictionary: {get_prime_hash_dict(words2)}")
    print()
    most_anagrams = get_most_anagrams(words1)
    print(f"Most anagrams in words1:{most_anagrams}")
    print()
    most_anagrams = get_most_anagrams(words2)
    print(f"Most anagrams in words2: {most_anagrams}")
    print()
    print(f"All anagrams in words1: {get_all_anagrams(words1)}")
    print(f"All anagrams in words2: {get_all_anagrams(words2)}")
    print()
