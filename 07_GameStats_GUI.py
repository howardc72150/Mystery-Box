from tkinter import *
from functools import partial
import random

class Game:
    def __init__(self):
        self.game_stats_list = [50, 6]
        self.round_stats_list = ['lead\n($0) | copper\n($1) | lead\n($0) - Cost: $5 | Payback: $1 | Current Balance: $46', 
                                 'copper\n($1) | copper\n($1) | silver\n($2) - Cost: $5 | Payback: $4 | Current Balance: $45', 
                                 'silver\n($2) | copper\n($1) | copper\n($1) - Cost: $5 | Payback: $4 | Current Balance: $44', 
                                 'silver\n($2) | lead\n($0) | lead\n($0) - Cost: $5 | Payback: $2 | Current Balance: $41', 
                                 'copper\n($1) | copper\n($1) | silver\n($2) - Cost: $5 | Payback: $4 | Current Balance: $40']
        self.game_frame = Frame()
        self.game_frame.grid()

            # heading row
        self.heading_label = Label(self.game_frame, text="Play",
                                   font="Verdana 24 bold", padx=10,pady=10)
        self.heading_label.grid(row=0)

            # history button
        self.stats_button = Button(self.game_frame, text="Game Stats",
                                   font="Verdana 14", padx=10, pady=10,
                                   command=lambda: self.to_stats(self.round_stats_list))
        self.stats_button(row=1)

    def to_stats(self, game_history, game_stats):
        GameStats(self, game_history, game_stats)

class GameStats:
    def __init__(self, partner, game_history, game_stats):
        print(game_history)

            # disable help button
        partner.stats_button.config(state=DISABLED)

            # initalise vars
        heading = "Verdana 12 bold"
        content = "Verdana 12"
        
            # sets up child window
        self.stats_box = Toplevel()
            
            # if users press cross at top, closes help and releases button.
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

            # set up GUI frame.
        self.stats_frame = Frame(self.stats_box)
        self.stats_frame.grid()

            # set up help heading
        self.stats_heading_label = Label(self.stats_frame, text="Game Statistics", font="Verdana 19 bold")
        self.stats_heading_label.grid(row=0)

if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box")
    var = Game(root)
    root.mainloop()  