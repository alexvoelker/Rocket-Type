from tkinter import Tk, Entry, Label


class TypingGUI:
    def __init__(self):
        # TODO tkinter GUI environment
        self.window = Tk()
        self.window.title("RocketType Typing Test")
        self.window.config(height=400, width=800)

        self.label_player_wpm = Label(text='Words Per Minute: 0')
        self.entry_player_name = Entry()

        self.text_entry = Entry(width=75)

        self.new_word_typed = False
        self.click_stopped = False

        # TODO typing input and text checker

        # TODO Display typing speed
        self.displayed_wpm = 0

        self.words_correct = []
        self.words_incorrect = []
        self._to_continue = True

        self.window.mainloop()

    def reset_new_word_typed(self):
        self.new_word_typed = False

    def add_words(self, words: list[str]):
        pass

    def display_wpm(self, wpm):
        """Set the value of a label field to be the wpm value"""
        self.displayed_wpm = wpm
        self.label_player_wpm.config(text=f"Words Per Minute: {self.displayed_wpm}")

    def gui_loop(self):
        while self._to_continue:
            # While the game is running, collect user input

            # Whenever a full new word is entered, check if it was entered in correctly
            # and append the input to either self.words_correct or self.words_incorrect

            pass

    def end(self):
        """TODO display the scoreboard GUI above the game UI"""
        # TODO Make the text entry unalterable
        self._to_continue = False

        # TODO Place the scoreboard top 10 scores above the UI
        pass

    def reset(self):
        """TODO Remove scoreboard fields from view and clear text inputs"""
        pass
