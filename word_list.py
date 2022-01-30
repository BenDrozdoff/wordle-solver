from word_utils import choose_random

class WordList:
    def __init__(self):
        with open('words.txt') as f:
            self.list = [word.strip() for word in f.readlines()]

    def choose_word(self):
        return choose_random(self.list)
    
    def choose_words(self, n):
        return choose_random(self.list, n)
