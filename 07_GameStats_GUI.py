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

            # to export instructions
        self.export_instructions = Label(self.stats_frame, text="Here are your Game Statistics. Please use the Export button to access the results"
                                         "of each round that you played.", wrap=250,font="Verdana 10 italic", justify=LEFT, fg="green", padx=10, pady=10)
        self.export_instructions.grid(row=1)

            # starting balance
        self.details_frame = Frame(self.stats_frame)
        self.details_frame.grid(row=2)

        self.start_balance_label = Label(self.details_frame, text="Starting Balance:", font=heading, anchor="e")
        self.start_balance_label.grid(row=0, column=0, padx=0)
        
        self.start_balance_value_label = Label(self.details_frame, font=content, text="${}".format(game_stats[0]), anchor="w")
        self.start_balance_value_label.grid(row=0, column=1, padx=0)

            # current balance
        self.current_balance_label = Label(self.details_frame, text="Current Balance:", font=heading, anchor="e")
        self.current_balance_label.grid(row=1,column=0,padx=10)

        self.current_balance_value_label = Label(self.details_frame, font=content, text="${}".format(game_stats[1]))
        self.current_balance_value_label.grid(row=1,column=1,padx=0)

        if game_stats[1] > game_stats[0]:
            win_loss = "Amount Won:"
            amount = game_stats[1] - game_stats[0]
            win_loss_fg = "green"
        else:
            win_loss = "Amount Lost:"
            amount = game_stats[0] - game_stats[1]
            win_loss_fg = "#660000"
        
            # amount won or lost
        self.wind_loss_label = Label(self.details_frame, text=win_loss, font=heading, anchor="e")
        self.wind_loss_label.grid(row=2,column=0,padx=0)

        self.wind_loss_value_label = Label(self.details_frame, font=content, text="${}".format(amount), fg=win_loss_fg, anchor="w")
        self.wind_loss_value_label.grid(row=2, column=1, padx=0)

            # rounds played
        self.games_played_label = Label(self.details_frame,text="Rounds Played:", font=heading, anchor="e")
        self.games_played_label.grid(row=4, column=0, padx=0)
        
        self.games_played_value_label = Label(self.details_frame, font=content, text=len(game_history), anchor="w")
        self.games_played_value_label.grid(row=4, column=1, padx=0)

            # dismiss button
            



if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Game(root)
    root.mainloop()  