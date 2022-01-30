from guess import Guess
from guess_history import GuessHistory
from solver import all_indices_of
from word_list import WordList
from word_utils import choose_random, letter_frequencies


class Game:
    MAX_GUESSES = 6

    def __init__(self, correct_word=None, verbose=False):
        self.verbose = verbose
        self.word_list = WordList()
        self.correct_word = correct_word or self.word_list.choose_word()
        self.guess_history = GuessHistory()
        self.candidates = self.word_list.list

    def play(self):
        self.log(f"Correct word: {self.correct_word}")

        while self.guesses_left() > 0:
            self.log(f"{len(self.candidates)} possible words")
            word_to_guess = self.best_guess()
            self.guess_word(word_to_guess)
            self.calculate_candidates()
            if word_to_guess == self.correct_word:
                self.success = True
                self.log(f"Success in {self.guess_count()} guesses")
                return

        self.log("Failure")
        self.log(f"Correct: {self.correct_word}")
        self.log(f"Last Guess: {word_to_guess}")
        self.log(self.guess_history.history)
        self.success = False

    def guess_word(self, word):
        self.log(f"Guess: {word}")
        results = Guess(word).evaluate(self.correct_word)
        self.log(f"Results: {results}")
        self.guess_history.append(word, results)

    def calculate_candidates(self):
        self.candidates = list(
            filter(lambda x: self.guess_history.is_word_possible(x), self.candidates)
        )
        return self.candidates

    def best_guess(self):
        if self.guesses_left() == 1 or len(self.candidates) <= self.guesses_left():
            return choose_random(self.candidates)
        else:
            candidate_letter_frequencies = letter_frequencies(self.candidates)
            vowel_penalty = 1 + (self.guesses_left() * self.guesses_left() / 18)
            vowels = ["a", "e", "i", "o", "u"]
            for vowel in vowels:
                candidate_letter_frequencies[vowel] = (
                    candidate_letter_frequencies[vowel] / vowel_penalty
                )
            return sorted(
                self.word_list.list,
                key=lambda x: self.letter_frequency_score(
                    word=x, letter_frequencies=candidate_letter_frequencies
                ),
                reverse=True,
            )[0]

    def letter_frequency_score(self, word, letter_frequencies):
        WEIGHTS = {
            "missing": 0,
            "all_known": 0,
            "known_position": 1,
            "unknown_position": 10,
            "unknown": 100,
        }
        score = 0
        for letter in set(list(word)):
            frequency = letter_frequencies[letter]
            letter_status = self.guess_history.letter_status(letter)
            # no credit for known position guesses of previously known positions
            if letter_status == "known_position" and all(
                idx in self.guess_history.history[letter]["correct"]
                for idx in all_indices_of(word, letter)
            ):
                letter_status = "all_known"
            # no credit for unknown position guesses of previous misses
            elif letter_status == "unknown_position" and all(
                idx in self.guess_history.history[letter]["incorrect"]
                for idx in all_indices_of(word, letter)
            ):
                letter_status = "all_known"

            score += WEIGHTS[letter_status] * frequency

        return score

    def log(self, content):
        if self.verbose:
            print(content)

    def guess_count(self):
        return self.guess_history.guess_count()

    def guesses_left(self):
        return self.MAX_GUESSES - self.guess_count()
