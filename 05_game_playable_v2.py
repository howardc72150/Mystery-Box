from tkinter import *
from functools import partial
import random

class Start:
    def __init__(self, partner):
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid(row=2, pady=10)
        
        self.push_me_button = Button(self.start_frame,text="Push Me", command=self.to_game)
        self.push_me_button.grid(row=0, pady=10)

    def to_game(self):
        starting_balance = 50
        stakes = 2

        Game(self, stakes, starting_balance)
        self.start_frame.destroy()

class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)

            # Initialise balance and multiplier variables.        
        self.balance = IntVar()
        self.balance.set(starting_balance)
        self.multiplier = IntVar()
        self.multiplier.set(stakes)

            # GUI setup.
        self.game_box = Toplevel()
        self.game_box.protocol('WM_DELETE_WINDOW', self.to_quit)
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

            # Heading row.
        self.heading_label = Label(self.game_frame, text="Play..",
                                   font=("Verdana 24 bold"), padx=10, pady=10)
        self.heading_label.grid(row=0)

            # Instructions label.
        self.instructions_label = Label(self.game_frame, wrap=300, justify=LEFT,
                                        text="Press <enter> or click the 'Open Boxes'"
                                        " button to reveal the contents of the mystery boxes.",
                                        font=("Verdana 10"), padx=10, pady=10)
        self.instructions_label.grid(row=1)

            # Boxes go here (row=2)
        box_text = "Verdana 16 bold"
        box_background = "#b9ea96"
        box_width = 5
        self.box_frame = Frame(self.game_frame)
        self.box_frame.grid(row=2, pady=10)
        photo = PhotoImage(file="question.gif")

        self.prize1_label = Label(self.box_frame, image=photo, padx=10, pady=10)
        self.prize2_label = Label(self.box_frame, image=photo, padx=10, pady=10)
        self.prize3_label = Label(self.box_frame, image=photo, padx=10, pady=10)

        self.prize1_label.photo = photo
        self.prize2_label.photo = photo
        self.prize3_label.photo = photo
        self.prize1_label.grid(row=0, column=0)
        self.prize2_label.grid(row=0, column=1, padx=10)
        self.prize3_label.grid(row=0, column=2)

            # Play button.
        self.play_button = Button(self.game_frame, text="Open boxes", bg="#FFFF33",
                                  font=("Verdana 15 bold"), width=20, padx=10, pady=10,
                                  command=self.reveal_boxes)
        self.play_button.grid(row=3)

            # Bind button to enter.
        self.play_button.focus()
        self.play_button.bind('<Return>', lambda e: self.reveal_boxes())
        self.play_button.grid(row=3)

            # Balance label.
        start_text = "Game cost: ${} \n "" \nHow much " \
                     "will you win?".format(stakes * 5)
        self.balance_label = Label(self.game_frame, font=("Verdana 12 bold"), fg="green",
                                   text=start_text, wrap=300, justify=LEFT)
        self.balance_label.grid(row=4, pady=10)

            # Help and game stats.
        self.help_export_frame = Frame(self.game_frame)
        self.help_export_frame.grid(row=5, pady=10)

        self.help_button = Button(self.help_export_frame, text="Help / Rules",
                                  font=("Verdana 15 bold"), bg="#808080", fg="white")
        self.help_button.grid(row=0, column=0, padx=2)

        self.stats_button = Button(self.help_export_frame, text="Game Stats",
                                   font=("Verdana 15 bold"), bg="#003366", fg="white")
        self.stats_button.grid(row=0, column=1, padx=2)

            # Quit button
        self.quit_button = Button(self.game_frame, text="Quit", fg="white", bg="#660000",
                                  font=("Verdana 15 bold"), width=20, command=self.to_quit,
                                  padx=10, pady=10)
        self.quit_button.grid(row=6, pady=10)

    def reveal_boxes(self):
            # Retrieve the balance from initial function.
        current_balance = self.balance.get()
        stakes_multiplier = self.multiplier.get()
        
        round_winnings = 0
        prizes = []
        stats_prizes = []
        for item in range(0,3):
            prize_num = random.randint(1,100)
            if 0 < prize_num <= 5:
                prize_list = "gold\n(${})".format(5*stakes_multiplier)
                prize = PhotoImage(file="gold_low.gif")
                round_winnings += 5*stakes_multiplier
            elif 5 < prize_num <= 25:
                prize_list = "silver\n(${})".format(2*stakes_multiplier)
                prize = PhotoImage(file="silver_low.gif")
                round_winnings += 2*stakes_multiplier
            elif 25 < prize_num <= 65:
                prize_list = "copper\n(${})".format(1*stakes_multiplier)
                prize = PhotoImage(file="copper_low.gif")
                round_winnings += stakes_multiplier
            else:
                prize_list = "lead\n($0)"
                prize = PhotoImage(file="lead.gif")
            prizes.append(prize)
            stats_prizes.append(prize_list)
        
        photo1 = prizes[0]
        photo2 = prizes[1]
        photo3 = prizes[2]

            # Display prizes.
        self.prize1_label.config(image=photo1)
        self.prize2_label.config(image=photo2)
        self.prize3_label.config(image=photo3)
        self.prize1_label.photo = photo1
        self.prize2_label.photo = photo2
        self.prize3_label.photo = photo3

            # Deduct cost of game.
        current_balance -= 5*stakes_multiplier
            # Add winnings
        current_balance += round_winnings
            # Set balance to new balance
        self.balance.set(current_balance)
        balance_statement = "Game Cost: ${}\nPayback: ${} \n" \
                            "Current Balance: ${}".format(5*stakes_multiplier, round_winnings, current_balance)
        
            # Edit label so user can see their balance.
        self.balance_label.config(text=balance_statement)

        if current_balance < 5*stakes_multiplier:
            self.play_button.config(state=DISABLED)
            self.game_box.focus()
            self.play_button.config(text="Game Over")
            
            balance_statement = "Current Balcen: ${}\n" \
                                "Your balance is too low. You can only quit " \
                                "or view your stats. Sorry about that.".format(current_balance)
            self.balance_label.config(fg="#660000", font="Verdana 10 bold")

    def to_quit(self):
        root.destroy()
    
    # Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box")
    var = Start(root)
    root.mainloop()  