import json
from datetime import datetime


class TypingGUI:
    def __init__(self):
        # TODO tkinter GUI environment

        self.new_word_typed = False
        self.click_stopped = False

        # TODO typing input and text checker

        # TODO Display typing speed

    def reset_new_word_typed(self):
        self.new_word_typed = False

    def add_words(self, words: list[str]):
        pass

    def display_wpm(self, wpm):
        """TODO Set the value of a label field to be the wpm value"""
        pass

    def append_scoreboard(self, user_name: str, wpm: int, date: datetime, time_spent: float):
        """Add a score to the scoreboard"""
        with json.load(open("scoreboard.json", 'r')) as scoreboard:
            json_scoreboard = json.load(scoreboard)
            json_scoreboard.update({f"{date}": {"username": user_name,
                                                "words_per_minute": wpm,
                                                "Seconds Played": f"{time_spent:.2f}"}})
        with open("scoreboard.json", "w") as scoreboard:
            json.dump(json_scoreboard, scoreboard, indent=4)
        print("Score added to scoreboard datafile")

    def end(self):
        """TODO display the scoreboard GUI above the game UI"""
        pass

    def reset(self):
        """TODO Remove scoreboard fields from view and clear text inputs"""
        pass
