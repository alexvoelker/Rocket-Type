import json
import random
import time
from datetime import datetime
from TypingGUI import TypingGUI


def append_scoreboard(user_name: str, wpm: int, date: datetime, time_spent: float):
    """Add a score to the scoreboard"""

    new_score = {
        "date_ID": f"{date}",
        "username": user_name,
        "words_per_minute": wpm,
        "seconds_played": f"{time_spent:.2f}"
    }

    try:
        with open("scoreboard.json", 'r') as scoreboard:
            json_scoreboard = json.load(scoreboard)
            json_scoreboard["scores"].append(new_score)
        with open("scoreboard.json", "w") as scoreboard:
            json.dump(json_scoreboard, scoreboard, indent=4)
    except FileNotFoundError:
        # File doesn't exist, so create it!
        with open('scoreboard.json', 'w') as scoreboard:
            json.dump({"scores": [new_score]}, scoreboard, indent=4)

    print("Score added to scoreboard datafile")


class TypingTest:
    def __init__(self):
        # initialize the word list
        with open('word_list.txt', 'r') as word_file:
            self.word_list = word_file.read().splitlines()

        # Words Per Minute Counter
        self.wpm = 0
        self.words_typed = 0
        self.user_name = "John Smith"  # Default User Name

        self.words_generated_per_batch = 18
        self.words_to_type = self.get_more_words(18)
        # When a user gets within a set number of words typed of the word_to_type list, more will be generated
        self.word_batch_threshold = 6

        # Initialize the GUI
        self.GUI = TypingGUI()
        self.time_start = -1
        self.time_lasted = -1

        self.timeout_seconds = 10

    def get_more_words(self, number_of_words) -> list:
        more_words = []
        for i in range(number_of_words):
            more_words.append(random.choice(self.word_list))
        return more_words

    def calculate_wpm(self):
        minutes_played = (time.time() - self.time_start) / 60
        self.wpm = self.words_typed / minutes_played
        return self.wpm

    def start(self):
        self.GUI.add_words(self.words_to_type)
        self.time_start = time.time()
        timeout_counter = 0
        last_update_time = self.time_start

        # Main Game Loop
        current_time = time.time()  # add variable here to reduce latency caused in calling the time.time() function
        while not self.GUI.click_stopped:
            current_time = time.time()
            if timeout_counter >= self.timeout_seconds:
                # User timed out, so add timeout seconds to starting time to calculate a more accurate duration
                self.time_start += self.timeout_seconds
                break

            timeout_counter += current_time - last_update_time
            last_update_time = current_time

            if self.GUI.new_word_typed:
                self.GUI.reset_new_word_typed()
                self.words_typed += 1
                self.wpm = self.calculate_wpm()
                self.GUI.display_wpm(self.wpm)
                # Reset countdown clock
                timeout_counter = 0

            # Check if more words are needed after every word_batch_threshold words are typed
            if self.words_typed % self.word_batch_threshold == 0:
                self.GUI.add_words(self.get_more_words(self.words_generated_per_batch))

        self.time_lasted = current_time - self.time_start
        self.end()

    def end(self):
        self.user_name = self.GUI.entry_player_name.get().strip()
        append_scoreboard(self.user_name,
                          self.wpm, datetime.now(),
                          # Time in seconds
                          float(self.time_lasted))
        self.GUI.end()
