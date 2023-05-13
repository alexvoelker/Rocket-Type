import random
import time
from datetime import datetime
from TypingGUI import TypingGUI


class TypingTest:
    def __init__(self):
        # initialize the word list
        with open('word_list.txt', 'r') as word_file:
            self.word_list = word_file.read().splitlines()

        # Words Per Minute Counter
        self.wpm = 0
        self.words_typed = 0
        self.user_name = "John Smith"

        self.words_generated_per_batch = 30
        self.words_to_type = self.get_more_words()
        # When a user gets within a set number of words typed of the word_to_type list, more will be generated
        self.word_batch_threshold = 10

        # Initialize the GUI
        self.GUI = TypingGUI()
        self.time_start = -1
        self.time_lasted = -1

        self.timeout_nano_seconds = 5 * 1000000000  # (5 Seconds in Nanoseconds)
        self.timeout_counter = -1

    def get_more_words(self) -> list:
        more_words = []
        for i in range(self.words_generated_per_batch):
            more_words.append(random.choice(self.word_list))
        return more_words

    def calculate_wpm(self):
        minutes_played = (time.time_ns() - self.time_start) * 1000000000 / 60
        self.wpm = self.words_typed / minutes_played
        return self.wpm

    def start(self):
        self.GUI.add_words(self.words_to_type)
        self.time_start = time.time_ns()
        self.timeout_counter = 0

        # Main Game Loop
        while not self.GUI.click_stopped and self.timeout_counter < self.timeout_nano_seconds:
            self.timeout_counter += time.time_ns() - self.timeout_counter

            if self.GUI.new_word_typed:
                self.GUI.reset_new_word_typed()
                self.words_typed += 1
                self.wpm = self.calculate_wpm()
                self.GUI.display_wpm(self.wpm)
                # Reset countdown clock
                self.timeout_counter = 0

            # TODO add typing error functionality

            # Check if more words are needed
            if self.words_typed % self.words_generated_per_batch - self.word_batch_threshold == 0:
                self.GUI.add_words(self.get_more_words())

        self.time_lasted = time.time_ns() - self.time_start
        self.end()

    def end(self):
        self.GUI.end()
        self.GUI.append_scoreboard(self.user_name,
                                   self.wpm, datetime.now(),
                                   # Time in seconds
                                   float(self.time_lasted / 1000000000))
