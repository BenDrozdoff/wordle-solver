import string
from collections import defaultdict
from word_utils import letter_counts, letter_indices

class GuessHistory:
    def __init__(self):
        self.history = defaultdict(lambda: defaultdict(list))
        self.history['guesses'] = []

    def append(self, word, results):
        self.history['guesses'].append(word)
        guessed_letters = letter_indices(word)
        for letter, indices in guessed_letters.items():
            guesses = [(idx, results[idx]) for idx in indices]
            correct_indices = [guess[0] for guess in guesses if guess[1] == 'correct']
            incorrect_indices = [guess[0] for guess in guesses if guess[1] == 'incorrect']
            missing_indices = [guess[0] for guess in guesses if guess[1] == 'missing']
            if len(correct_indices) > 0:
                self.set_correct(letter=letter, indices=correct_indices)
                self.set_letter_min_count(letter=letter, count=len(correct_indices))
                # if we have correct and incorrect, we know there are more instances
                # of the letter not guessed, so we know a minimum letter count > 1
                if len(incorrect_indices) > 0:
                    self.set_incorrect(letter=letter, indices=incorrect_indices)
                    calculated_min = len(correct_indices) + len(incorrect_indices)
                    self.set_letter_min_count(letter=letter, count=calculated_min)
                # if we have correct and missing, we know that there are no other
                # instances of the letter
                if len(missing_indices) > 0:
                    calculated_max = len(correct_indices) + len(incorrect_indices) 
                    self.set_letter_max_count(letter=letter, count=calculated_max)
            elif len(incorrect_indices) > 0:
                self.set_incorrect(letter=letter, indices=incorrect_indices)
                self.set_letter_min_count(letter=letter, count=len(incorrect_indices))
                if len(missing_indices) > 0:
                    calculated_max = len(incorrect_indices) 
                    if self.history[letter]['max_count']:
                        calculated_max = min(self.history[letter]['max_count'], calculated_max)
                    self.history[letter]['max_count'] == calculated_max
            elif len(missing_indices) > 0:
                self.set_letter_max_count(letter=letter, count=0)

    def is_word_possible(self, word):
        word_letter_counts = letter_counts(word)
        word_letter_indices = letter_indices(word)
        for letter in string.ascii_lowercase:
            if type(self.history[letter]['max_count']) == int and self.history[letter]['max_count'] < word_letter_counts[letter]:
                return False                
            elif type(self.history[letter]['min_count']) == int and self.history[letter]['min_count'] > word_letter_counts[letter]:
                return False
            elif any(correct_index not in word_letter_indices[letter] for correct_index in self.history[letter]['correct']):
                return False
            elif any(incorrect_index in word_letter_indices[letter] for incorrect_index in self.history[letter]['incorrect']):
                return False
        return True

    def set_letter_max_count(self, letter, count):
        if type(self.history[letter]['max_count']) == int and self.history[letter]['max_count'] <= count:
            return
        self.history[letter]['max_count'] = count
        return count

    def set_letter_min_count(self, letter, count):
        if type(self.history[letter]['min_count']) == int and self.history[letter]['min_count'] >= count:
            return
        self.history[letter]['min_count'] = count
        return count

    def set_correct(self, letter, indices):
        self.history[letter]['correct'].extend(indices) 
        self.history[letter]['correct'] = list(set(self.history[letter]['correct']))
        return self.history[letter]['correct']

    def set_incorrect(self, letter, indices):
        self.history[letter]['incorrect'].extend(indices) 
        self.history[letter]['incorrect'] = list(set(self.history[letter]['incorrect']))
        return self.history[letter]['incorrect'] 

        
    def letter_status(self, letter):
        if self.history[letter]['max_count'] == 0:
            return 'missing'
        elif self.history[letter]['max_count'] == len(self.history[letter]['correct']):
            return 'all_known'
        elif self.history[letter]['min_count'] and self.history[letter]['min_count'] == len(self.history[letter]['correct']):
            return 'known_position'
        elif self.history[letter]['min_count'] and self.history[letter]['min_count'] > len(self.history[letter]['correct']):
            return 'unknown_position'
        elif not (type(self.history[letter]['min_count']) == int or type(self.history[letter]['max_count']) == int):
            return 'unknown'


    def guess_count(self):
        return len(self.history['guesses'])
    
