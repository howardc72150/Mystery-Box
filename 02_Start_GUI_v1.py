from tkinter import *
from functools import partial
import random

class Start:
    def __init__(self, partner):
        # GUI to get starting balance and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Set initial balance to zero
        self.starting_funds = IntVar()
        self.starting_funds.set(0)

        # Mystery heading (row=0)
        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game",
                                       font=("Verdana", "19", "bold"))
        self.mystery_box_label.grid(row=0)

        # Initial instructions (row=1)
        self.mystery_instructions = Label(self.start_frame, font=("Verdana", "10", "italic"),
                                          text="Please enter a dollar amount (between $5 and $50)"
                                          " in the box below. Then choose the stakes. The higher"
                                          " the stakes, the more you can win!", wrap=300, justify=LEFT, padx=10, pady=10)
        self.mystery_instructions.grid(row=1)

        # Entry box (row=2)
        self.entry_error_frame = Frame(self.start_frame, width=200)
        self.entry_error_frame.grid(row=2)
        
        self.start_amount_entry = Entry(self.entry_error_frame, font=("Verdana", "19", "bold"), width=10)
        self.start_amount_entry.grid(row=0, column=0)

        self.add_funds_button = Button(self.entry_error_frame, font=("Verdana", "19", "bold"),
                                       text="Add Funds", command=self.check_funds)
        self.add_funds_button.grid(row=0,column=1)

        self.amount_error_label = Label(self.entry_error_frame, fg="maroon",
                                        text="", font="Verdana 10 bold", wrap=275, justify=LEFT)
        self.amount_error_label.grid(row=1, columnspan=2, pady=5)

        # Button frame (row=3)
        self.stakes_frame = Frame(self.start_frame)
        self.stakes_frame.grid(row=3)

        # Buttons go here.
        button_font = "Verdana 12 bold"
        self.low_stakes_button = Button(self.stakes_frame, text="Low ($5)",
                                       command=lambda: self.to_game(1),
                                       font=button_font, bg="#FF9933")
        self.low_stakes_button.grid(row=0, column=0, pady=10)

        self.medium_stakes_button = Button(self.stakes_frame, text="Medium ($10)",
                                       command=lambda: self.to_game(2),
                                       font=button_font, bg="#FFFF33")
        self.medium_stakes_button.grid(row=0, column=1, padx=5, pady=10)

        self.high_stakes_button = Button(self.stakes_frame, text="High ($15)",
                                       command=lambda: self.to_game(3),
                                       font=button_font, bg="#99FF33")
        self.high_stakes_button.grid(row=0, column=2, pady=10)

        # Disable all stakes buttons at start.
        self.low_stakes_button.config(state=DISABLED)
        self.medium_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

        # Help button
        self.help_button = Button(self.start_frame, text="How to Play",
                                  bg="#808080", fg="white", font=button_font)
        self.help_button.grid(row=5, pady=10)

    def check_funds(self):
        starting_balance = self.start_amount_entry.get()

        # Set error background colojurs (and assume that there are no errors
        # at the start)
        error_bg = "#ffafaf"
        has_errors = False
        
        # Change background to white (for testing)
        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        # Disable all stakes buttons in case user changes mind and decreases
        # amount entered.
        self.low_stakes_button.config(state=DISABLED)
        self.medium_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

        try:
            starting_balance = int(starting_balance)
            if starting_balance < 5:
                has_errors = True
                error_feedback = "Sorry, the last you can play with is $5"
            elif starting_balance > 50:
                has_errors = True
                error_feedback = "Too high! The most you can risk in this" \
                                  "game is $50"

            elif starting_balance >= 15:
                self.low_stakes_button.config(state=NORMAL)
                self.medium_stakes_button.config(state=NORMAL)
                self.high_stakes_button.config(state=NORMAL)
            elif starting_balance >= 10:
                self.low_stakes_button.config(state=NORMAL)
                self.medium_stakes_button.config(state=NORMAL)
            else:
                self.low_stakes_button.config(state=NORMAL)
        
        except ValueError:
            has_errors = True
            error_feedback = "Please enter a dollar amount (no text / decimals.)"

        if has_errors == True:
            self.start_amount_entry.config(bg=error_bg)
            self.amount_error_label.config(text=error_feedback)
        else:
            self.starting_funds.set(starting_balance)



    def to_game(self, stakes):
        starting_balance = self.starting_funds.get()
        Game(self, stakes, starting_balance)
        root.withdraw()

class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)

# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box")
    var = Start(root)
    root.mainloop()  