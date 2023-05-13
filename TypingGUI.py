
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

    def end(self):
        """TODO display the scoreboard GUI above the game UI"""
        pass

    def reset(self):
        """TODO Remove scoreboard fields from view and clear text inputs"""
        pass
