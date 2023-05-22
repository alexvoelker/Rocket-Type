from tkinter import Tk, Entry, Label, DISABLED, StringVar, Frame, Button, WRITABLE, END
from tkinter.font import Font
import json


def get_top_scoreboard(num_scores: int) -> str:
    """Gather the scoreboard scores, sort them by wpm, and get the top num_scores of them"""
    try:
        with open("scoreboard.json", 'r') as scoreboard:
            json_scoreboard = json.load(scoreboard)
            scores = json_scoreboard["scores"]
            scores = sorted(scores, key=lambda x: int(x["words_per_minute"]), reverse=True)
            scores_to_return = scores[:num_scores]
            out = ""
            for score in scores_to_return:
                out += "----------\n"
                out += f"User: {score['username']}\n"
                out += f"Words Per Minute: {score['words_per_minute']}\n"
                out += f"Time Played (Seconds): {score['seconds_played']}\n"
            out += "----------\n"
            return out
    except FileNotFoundError:
        # File doesn't exist, so there are no scores!
        return "No Scores on File"


class TypingGUI:
    def __init__(self):
        # tkinter GUI environment
        self.window = Tk()
        self.window.title("RocketType Typing Test")
        self.window.config(height=400, width=800, pady=50, padx=50)

        # The title
        title_font = Font(size=20, weight='bold')
        self.label_game = Label(text="RocketType", font=title_font, pady=30)
        self.label_game.grid(column=2, row=0)

        # Player name changer
        username_string = StringVar()
        self.label_player_name_entry = Label(text="Player Name: ")
        self.label_player_name_entry.grid(column=0, row=2)
        self.entry_player_name = Entry(self.window, textvariable=username_string)
        self.entry_player_name.grid(column=1, row=2)

        # Words per minute counter
        self.displayed_wpm = 0
        self.label_player_wpm = Label(self.window, text=f'Words Per Minute: {self.displayed_wpm}')
        self.label_player_wpm.grid(column=3, row=2)

        # Where the words are displayed
        self.label_entry_word_prompt = Label(text="Type these words...")
        self.label_entry_word_prompt.grid(column=1, row=3)

        self.word_container = Frame(self.window, pady=25, padx=25)
        self.word_container.grid(column=2, row=3, pady=30)
        self.word_list = []
        self.word_labels = []

        self.user_input_string = StringVar()
        self.text_entry = Entry(self.window, width=25, textvariable=self.user_input_string)
        self.text_entry.grid(row=4, column=2)

        self.new_word_typed = False

        # TODO typing input and text checker
        self.words_typed = 0
        self.words_correct = []
        self.words_incorrect = []
        self.to_continue = True

        self.scoreboard_display = None  # Will use this variable later once the game ends

        self.end_button = Button(text="End Game", command=self.end)
        self.end_button.grid(row=4, column=3)

        # Maybe add resetting functionality later.
        # self.end_button = Button(text="Reset Game", command=self.reset_screen)
        # self.end_button.grid(row=5, column=3)

        self.window.mainloop()
        # self.gui_loop()

    def reset_new_word_typed(self):
        self.new_word_typed = False

    def add_words(self, words: list[str]):
        """Add words to the GUI display. NOTE: Only accepts word lists of length 18 or 6"""
        if len(words) != 6 and len(words) != 18:
            return

        count = 0

        if len(self.word_labels) > 0:
            for label in self.word_labels[:6]:
                label.destroy()
            word_labels = self.word_labels[6:]

            # If there are words in the word list,
            # shift the first two rows down
            for row in range(2):
                for column in range(6):
                    word_labels[count].grid(row=row, column=column)
                    count += 1

            # Then add the final row of new words
            word_num = 0
            for column in range(6):
                word_label = Label(self.word_container, text=words[word_num], fg='blue')
                word_label.grid(row=3, column=column)
                word_labels.append(word_label)
                word_num += 1

        else:
            for row in range(3):
                for column in range(6):
                    word_label = Label(self.word_container, text=words[count], fg='blue')
                    word_label.grid(row=row, column=column)
                    self.word_labels.append(word_label)

    def display_wpm(self, wpm):
        """Set the value of a label field to be the wpm value"""
        self.displayed_wpm = wpm
        self.label_player_wpm.config(text=f"Words Per Minute: {self.displayed_wpm}")

    def check_text_input(self):
        if self.to_continue:
            # While the game is running, collect user input
            word = self.text_entry.get()
            if ' ' not in word:  # Check for spaces in the entry box
                return
            # Check the self.text_entry for a new word (non-space characters followed by a space)
            if len(word.strip()) > 0:
                self.words_typed += 1
                if word == self.word_list[self.words_typed]:
                    self.words_correct.append(word)
                    #     TODO modify the entry_word_prompt to reflect a new correct word

                else:
                    #     TODO modify the entry_word_prompt to reflect a new incorrect word
                    self.words_incorrect.append(word)

                # Clear the entry when the word is typed
                self.text_entry.setvar("")

                print(word)

                # update self.new_word_typed to send a message to the TypingText logic engine
                self.new_word_typed = True

            # Whenever a full new word is entered, check if it was entered in correctly
            # and append the input to either self.words_correct or self.words_incorrect

            pass

    def end(self):
        """Display the scoreboard GUI above the game UI"""
        # Send the signal to end the game
        self.to_continue = False

        # Make the text entry unalterable and cleared of text
        self.text_entry['state'] = DISABLED
        self.text_entry.delete('1.0', END)

        # Place the scoreboard top scores above the UI
        scores = StringVar(value=get_top_scoreboard(5))
        self.scoreboard_display = Label(self.window, textvariable=scores)
        self.scoreboard_display.grid(row=1, column=2)

    def reset_screen(self):
        """Remove scoreboard fields from view and clear text inputs"""
        [label.destroy() for label in self.word_labels]
        self.word_labels.clear()
        self.text_entry['state'] = WRITABLE
        if self.scoreboard_display is not None:
            # Destroy the scoreboard display if it exists
            self.scoreboard_display.destroy()
