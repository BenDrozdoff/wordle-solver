from word_utils import all_indices_of


class Guess:
    def __init__(self, word):
        self.word = word

    def evaluate(self, correct_word):
        guessed_letters = list(self.word)
        correct_letters = list(correct_word)
        results = ["missing"] * 5

        for idx, letter in enumerate(correct_letters):
            if guessed_letters[idx] == letter:
                results[idx] = "correct"
            elif letter in set(guessed_letters):
                all_indices = all_indices_of(self.word, letter)
                overlapping_indices = list(
                    set(all_indices_of(correct_word, letter)).intersection(
                        set(all_indices)
                    )
                )
                incorrect_indices = list(set(all_indices) - set(overlapping_indices))
                if incorrect_indices:
                    first_incorrect_index = min(incorrect_indices)
                    results[first_incorrect_index] = "incorrect"
        return results
