from tkinter import *
from functools import partial
import random

class Start:
    def __init__(self, partner):
        # GUI to get starting balance and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Mystery heading (row=1)
        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game",
                                       font=("Verdana", "19", "bold"))
        self.mystery_box_label.grid(row=1)

        # Entry box (row=2)
        self.start_amount_entry = Entry(self.start_frame, font=("Verdana", "19", "bold"))
        self.start_amount_entry.grid(row=2)

        # Play button (row=3)
        self.lowstakes_button = Button(text="Low ($5)", command=lambda: self.to_game(1))
        self.lowstakes_button.grid(row=2, pady=10)

    def to_game(self, stakes):
        starting_balance = self.start_amount_entry.get()
        Game(self, stakes, starting_balance)

class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)
        
        # Disable low stakes button
        partner.lowstakes_button.config(state=DISABLED)

        # Initalise variables
        self.balance = IntVar()

        # Set starting balance to amount entered by user at start of the game
        self.balance.set(starting_balance)

        # GUI setup
        self.game_box = Toplevel()
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # Heading row
        self.heading_label = Label(self.game_frame, text="Heading",
                                  font=("Verdana", "19", "bold"), padx=10,
                                  pady=10)
        self.heading_label.grid(row=0)

        # Balance label
        self.balance_frame = Frame(self.game_frame)
        self.balance_frame.grid(row=1)

        self.balance_label = Label(self.game_frame, text="Balance...")
        self.balance_label.grid(row=2)

        self.play_button = Button(self.game_frame, text="Gain",
                                  padx=10, pady=10, command=self.reveal_boxes)
        self.play_button.grid(row=3)

    def reveal_boxes(self):
        # Retrieve the balance from the initial function.
        current_balance = self.balance.get()

        # Adjust hte balance (subtract game cost and add pay out)
        # For testing purposes, just add 2
        current_balance += 2
        
        # Set balance to adjusted balance
        self.balance.set(current_balance)

        # Edit label so user can see their balance
        self.balance_label.configure(text="Balance: {}".format(current_balance))


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box")
    var = Start(root)
    root.mainloop()  