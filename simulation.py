import statistics
from game import Game
from word_list import WordList

class Simulation:
    GAME_COUNT = 1000

    def __init__(self):
        self.successes = 0
        self.failures = 0
        self.guess_counts = []
        self.failing_words = []
    
    def run(self):
        words = self.select_words()
        for word in words:
            game = Game(correct_word=word)
            game.play()
            if game.success:
                self.successes += 1 
                self.guess_counts.append(game.guess_count())
            else:
                self.failures += 1
                self.failing_words.append(word)
    
    def select_words(self):
        return WordList().choose_words(self.GAME_COUNT)

    def success_rate(self):
        return self.successes / (self.successes + self.failures)

    def average_guess_count(self):
        return statistics.mean(self.guess_counts)

    def stdev_guess_count(self):
        return statistics.stdev(self.guess_counts)

if __name__ == '__main__':
    simulation = Simulation()
    simulation.run()

    print(f"Success Rate: {simulation.success_rate()}")
    print(f"Average Guesses: {simulation.average_guess_count()}")
    print(f"Stdev Guesses: {simulation.stdev_guess_count()}")
    print(f"Failing Words: {simulation.failing_words}")
