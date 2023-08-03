from itertools import combinations


class AnagramExplorer:
    def __init__(self, all_words: list[str]):
        self.__corpus = all_words
        self.prime_map = {
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
        self.anagram_lookup = (
            self.get_lookup_dict()
        )  # Only calculated once, when the object is created
        self.anagram_dict = self.get_prime_hash_dict()

    @property
    def corpus(self):
        return self.__corpus

    def top_level_checks(
        self, letters: list[str], pair: tuple[str, str] = ("", ""), check_single_word=""
    ) -> bool:
        """
        This function implements top-level checks common to each is_anagram approach
        Highly-recommended to create this function.

        Could return bool, though a more streamlined process would also return lowercase versions of each word along with a boolean
        """
        if check_single_word != "":
            if check_single_word not in self.corpus:
                return False
            valid_letters = letters.copy()
            for letter in check_single_word:
                if letter not in valid_letters:
                    return False
                valid_letters.remove(letter)
            return True

        word1 = pair[0].lower()
        word2 = pair[1].lower()

        if (
            len(word1) != len(word2)
            or word1 == word2
            or word1 not in self.corpus
            or word2 not in self.corpus
        ):
            return False

        valid_letters = letters.copy()
        for letter in word1:
            if letter not in valid_letters:
                return False
            valid_letters.remove(letter)

        valid_letters = letters.copy()
        for letter in word2:
            if letter not in valid_letters:
                return False
            valid_letters.remove(letter)

        return True

    def is_valid_anagram_pair(self, pair: tuple[str, str], letters: list[str]) -> bool:
        """Checks whether a pair of words:
        -are both included in the allowable word list (self.corpus)
        -consist entirely of letters chosen at the beginning of the game
        -form a valid anagram pair

        Args:
            pair: A tuple of two strings
            letters: The letters from which the anagrams should be created

        Returns:
            bool: Returns True if the word pair fulfills all validation requirements, otherwise returns False
        """
        if not self.top_level_checks(pair=pair, letters=letters):
            return False
        return sorted(pair[0].lower()) == sorted(pair[1].lower())

    def get_lookup_dict(self) -> dict:
        """Creates a fast dictionary look-up (via prime hash or sorted tuple) of all anagrams in a word corpus.

        Args:
            corpus (list): A list of words which should be considered

        Returns:
            dict: Returns a dictionary with  keys that return sorted lists of all anagrams of the key (per the corpus)
        """
        lookup_dict = {}

        for word in self.corpus:
            prime_hash_value = self.prime_hash(word)
            if prime_hash_value not in lookup_dict:
                lookup_dict[prime_hash_value] = [word]
            else:
                lookup_dict[prime_hash_value].append(word)

        return lookup_dict

    def prime_hash(self, str):
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
        hash_value = 1
        for letter in str:
            hash_value *= prime_map[letter]
        return hash_value

    def get_prime_hash_dict(self):
        lookup_dict = {}

        for word in self.corpus:
            prime_hash_value = self.prime_hash(word)
            if prime_hash_value not in lookup_dict:
                lookup_dict[prime_hash_value] = [word]
            else:
                lookup_dict[prime_hash_value].append(word)

        return lookup_dict

    def get_all_anagrams(self, letters: list[str]) -> set:
        """Creates a set of all unique words that could have been used to form an anagram pair.
        Words which can't create any anagram pairs should not be included in the set.

        Ex)
         corpus: ["abed", "mouse", "bead", "baled", "abled", "rat", "blade"]
         all_anagrams: {"abed",  "abled", "baled", "bead", "blade"}

        Args:
           letters (list): A list of letters from which the anagrams should be created

        Returns:
           set: all unique words in corpus which form at least 1 anagram pair
        """

        all_anagrams = set()

        combos = []
        for i in range(3, len(letters) + 1):
            combos += list(combinations(letters, i))

        hash_keys = []
        for combo in combos:
            hash_keys.append(self.prime_hash("".join(combo)))

        for key in hash_keys:
            if key in self.anagram_dict.keys() and len(self.anagram_dict[key]) > 1:
                for word in self.anagram_dict[key]:
                    all_anagrams.add(word)
        return all_anagrams

    def get_most_anagrams(self, letters: list[str]) -> str:
        """Returns a word from one of the largest lists of anagrams that can be formed using the given letters."""

        anagram_dict = self.anagram_lookup
        max_anagrams = [-1, ""]

        for key in anagram_dict:
            word = sorted(anagram_dict[key])[0]
            if (
                len(anagram_dict[key]) > max_anagrams[0]
                and len(anagram_dict[key]) > 1
                and self.top_level_checks(letters=letters, check_single_word=word)
            ):
                max_anagrams[0] = len(anagram_dict[key])
                max_anagrams[1] = word

        if max_anagrams[0] <= 1 or len(self.corpus) == 0:
            return ""

        return max_anagrams[1]


if __name__ == "__main__":
    print("Running AnagramExplorer for testing")
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

    words2 = ["rat", "mouse", "tar", "art", "chicken", "stop", "pots", "tops"]

    letters = ["l", "o", "t", "s", "r", "i", "a"]

    my_explorer = AnagramExplorer(words2)

    print(my_explorer.is_valid_anagram_pair(("rat", "tar"), letters))
    print(my_explorer.is_valid_anagram_pair(("stop", "pots"), letters))
    print(my_explorer.get_most_anagrams(letters))
    print(my_explorer.get_all_anagrams(letters))
