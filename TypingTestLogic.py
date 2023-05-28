import json
import random
import time
from datetime import datetime


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


class TypingTestLogic:
    def __init__(self):
        # initialize the word list
        with open('word_list.txt', 'r') as word_file:
            self.word_list = word_file.read().splitlines()

        # Words Per Minute Counter
        self.wpm = 0
        self.words_typed = 0
        self.user_name = "John Smith"  # Default User Name

        # Initial selection of words to type
        self.words_to_type = self.get_words_from_wordlist(18)
        # When a user gets within a set number of words typed of the word_to_type list, more will be generated
        self.words_generated_per_batch = 6
        self.word_batch_threshold = 6

        # Initialize the GUI
        self.time_start = -1
        self.time_lasted = -1
        self.timeout_seconds = 10
        self.started = True

    def get_words_from_wordlist(self, number_of_words) -> list:
        more_words = []
        for i in range(number_of_words):
            more_words.append(random.choice(self.word_list))
        return more_words

    def calculate_wpm(self):
        minutes_played = (time.time() - self.time_start) / 60
        self.wpm = self.words_typed / minutes_played
        return self.wpm

    def end(self):
        self.started = False

        append_scoreboard(user_name=self.user_name,
                          wpm=self.wpm,
                          date=datetime.now(),
                          # Time in seconds
                          time_spent=float(self.time_lasted))
