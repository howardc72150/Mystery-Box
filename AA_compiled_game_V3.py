from tkinter import *
from functools import partial
import random
import re

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

            # List for holding statistics.
        self.round_stats_list = []
        self.game_stats_list = [starting_balance, starting_balance]

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
        photo = PhotoImage(file="Mystery-Box\question.gif")

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
                                  font=("Verdana 15 bold"), bg="#808080", fg="white",
                                  command=self.to_help)
        self.help_button.grid(row=0, column=0, padx=2)

        self.stats_button = Button(self.help_export_frame, text="Game Stats",
                                   font=("Verdana 15 bold"), bg="#003366", fg="white", command= lambda:self.to_stats(self.round_stats_list, self.game_stats_list))
        self.stats_button.grid(row=0, column=1, padx=2)

            # Quit button
        self.quit_button = Button(self.game_frame, text="Quit", fg="white", bg="#660000",
                                  font=("Verdana 15 bold"), width=20, command=self.to_quit,
                                  padx=10, pady=10)
        self.quit_button.grid(row=6, pady=10)

    def to_help(self):
        get_help = Help(self)
    
    def to_stats(self, game_history, game_stats):
        GameStats(self, game_history, game_stats)

    def reveal_boxes(self):
            # Retrieve the balance from initial function
        current_balance = self.balance.get()
        stakes_multiplier = self.multiplier.get()
        
        round_winnings = 0
        prizes = []
        stats_prizes = []
        for item in range(0,3):
            prize_num = random.randint(1,100)
            if 0 < prize_num <= 5:
                prize_list = "gold (${})\n".format(5*stakes_multiplier)
                prize = PhotoImage(file="Mystery-Box\gold_low.gif")
                round_winnings += 5*stakes_multiplier
            elif 5 < prize_num <= 25:
                prize_list = "silver (${})\n".format(2*stakes_multiplier)
                prize = PhotoImage(file="Mystery-Box\silver_low.gif")
                round_winnings += 2*stakes_multiplier
            elif 25 < prize_num <= 65:
                prize_list = "copper (${})\n".format(1*stakes_multiplier)
                prize = PhotoImage(file="Mystery-Box\copper_low.gif")
                round_winnings += stakes_multiplier
            else:
                prize_list = "lead\n($0)"
                prize = PhotoImage(file="Mystery-Box\lead.gif")
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
        self.game_stats_list[1] = current_balance
        balance_statement = "Game Cost: ${}\nPayback: ${} \n" \
                            "Current Balance: ${}".format(5*stakes_multiplier, round_winnings, current_balance)
        
            # Add round results to statistics list.
        round_summary = "{} | {} | {} - Cost: ${} | " \
                        "Payback: ${} | Current Balance: " \
                        "${}".format(stats_prizes[0], stats_prizes[1], stats_prizes[2],
                                     5*stakes_multiplier, round_winnings, current_balance)
        self.round_stats_list.append(round_summary)
        print(self.round_stats_list)

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
    
class Help:
    def __init__(self, partner):

        # Disable help button.
        partner.help_button.config(state=DISABLED)

        # Sets up child window
        self.help_box = Toplevel()

        # If users press cross at top, closes help and releases help button.
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # Setup GUI frame
        self.help_frame = Frame(self.help_box, width=300)
        self.help_frame.grid()

        # Set up help heading
        self.how_heading = Label(self.help_frame, text="Help / Instructions",
                                font="Verdana 14 bold")
        self.how_heading.grid(row=0)

        help_text = "Choose an amount to play with and then choose the stakes. " \
                    "Higher stakes cost more per round but you can win more as " \
                    "well.\n\n" \
                    "When you enter the play area, you will see three mystery " \
                    "boxes. To reveal the contents of the boxes, click the " \
                    "'Open Boxes' button. If you don't have enough money to play, " \
                    "the button will turn red and you will need to quit the " \
                    "game.\n\n" \
                    "The contents of the boxes will be added to your balance. " \
                    "The boxes could contain..\n\n" \
                    "Low: Lead ($0) | Copper ($1) | Silver ($2) | Gold ($10)\n" \
                    "Medium: Lead ($0) | Copper ($2) | Silver ($4) | Gold ($25)\n" \
                    "High: Lead ($0) | Copper ($5) | Silver ($10) | Gold ($50)\n\n" \
                    "If each box contains gold, you earn $30 (low stakes). If " \
                    "they contained copper, silver and gold you would receive " \
                    "$13 ($1 + $2 + $10) and so on."
        
        self.help_text = Label(self.help_frame, text=help_text,
                               justify=LEFT, wrap=250, padx=10, pady=10)
        self.help_text.grid(row=1)

        # Dismiss button
        self.dismiss_btn = Button(self.help_frame, text="Dismiss",
                                  width=10, bg="#660000", fg="white",
                                  font="Verdana 15 bold", command=partial(self.close_help, partner))
        self.dismiss_btn.grid(row=2)

    def close_help(self, partner):
        # Put help button back to normal
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()

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


        # Export and dismiss button frame (row 3)
        self.export_dismiss_frame = Frame(self.details_frame)
        self.export_dismiss_frame.grid(row=5, pady=10)

        # Export button
        self.export_button = Button(self.export_dismiss_frame, text="Export",
                                    font=("Verdana", "15", "bold"), command=lambda: self.export(game_history, game_stats))
        self.export_button.grid(row=0, column=0)


            # dismiss button
        self.dismiss_button = Button(self.export_dismiss_frame, text="Dismiss",
                                  width=10, bg="#660000", fg="white",
                                  font="Verdana 15 bold", command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=0, column=1)

    def export(self, game_history, game_stats):
        get_export = Export(self, game_history, game_stats)

    def close_stats(self, partner):
            # Put help button back to normal
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()

class Export:
    def __init__(self, partner, game_history, all_game_stats):
        print(game_history)

            # Disable history button
        partner.export_button.config(state=DISABLED)

            # Creates child window
        self.export_box = Toplevel()
        
            # If users press cross at top, closes history and 'releases' export button
        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))

            # Set up GUI frame
        self.export_frame = Frame(self.export_box, width=300)
        self.export_frame.grid()

            # Set up history heading (row 0)
        self.how_heading = Label(self.export_frame, text="Export / Instructions",
                                font=("Verdana", "16", "bold"))
        self.how_heading.grid(row=0)

            # Export instructions
        self.export_text = Label(self.export_frame, text="If the filename you enter below"
                                " already exists, its contents will be replaced with your"
                                " calculation history", justify=LEFT, wrap=250, width=40)
        self.export_text.grid(row=1)

            # Warning text (label, row 2)
        self.export_text = Label(self.export_frame, text="If the filename you enter below"
                                " already exists, its contents will be replaced with your"
                                " calculation history", justify=LEFT, bg="#ffafaf", fg="maroon",
                                font=("Verdana", "10", "italic"), wrap=225, padx=10, pady=10)
        self.export_text.grid(row=2, pady=10)

        # Filename entry box (row 3)
        self.filename_entry = Entry(self.export_frame, width=20,font=("Verdana", "10", "italic"),
                                    justify=CENTER)
        self.filename_entry.grid(row=3, pady=10)
        
        # Error message labels (initially blank, row 4)
        self.save_error_label = Label(self.export_frame, text="", fg="maroon")
        self.save_error_label.grid(row=4)

        # Save and cancel frame (row 4)
        self.save_cancel_frame = Frame(self.export_frame)
        self.save_cancel_frame.grid(row=5, pady=10)

        # Save and cancel buttons (row 0 of save_Cancel frame)
        self.save_button = Button(self.save_cancel_frame, text="Save", font=("Verdana", "10", "bold"),
                                  command=partial(lambda: self.save_history(partner, game_history, all_game_stats)))
        self.save_button.grid(row=0, column=0)

        self.cancel_button = Button(self.save_cancel_frame, text="Cancel", font=("Verdana", "10", "bold"),
                                    command=partial(self.close_export, partner))
        self.cancel_button.grid(row=0, column=1)

    def save_history(self, partner, game_history, all_game_stats):
        # Regular expression to check filename is valid
        regex = "[A-Za-z0-9]"
        has_errors = "no"

        filename = self.filename_entry.get()
        print(filename)

        for letter in filename:
            if re.match(regex, letter):
                continue
        
            elif letter == " ":
                problem = "(no spaces allowed)"
            
            else:
                problem = (" (no {}'s allowed)".format(letter))
            has_errors = "yes"
            break

        if filename == "":
            problem = "can't be blank"
            has_errors = "yes"
        
        if has_errors == "yes":
            # Display error message
            self.save_error_label.config(text="Invalid filename - {}".format(problem))
            # Change entry box background to pink
            self.filename_entry.config(bg="#ffafaf")
            print()
        
        else:
            filename = filename + ".txt"
            f = open(filename, "w+")

            f.write("**** Game Statistics****\n\n")
            start_balance = all_game_stats[0]
            final_balance = all_game_stats[1]

            initial_statement = "Starting Balance ${:.2f}\n".format(start_balance)
            final_statement = "Closing Balance ${:.2f}\n".format(final_balance)

            if start_balance > final_balance:
                won_loss = "You lost ${:.2f}".format(start_balance-final_balance)
            elif start_balance < final_balance:
                won_loss = "You won ${:.2f}".format(final_balance-start_balance)
            else:
                won_loss = "You broke even"

            f.write(initial_statement)
            f.write(final_statement)
            f.write("\n")
            f.write(won_loss)

            f.write("\nMystery Box History\n\n")

            for item in game_history:
                f.write(item + "\n")
            
            f.close()
            self.close_export(partner)

    def close_export(self, partner):
        partner.export_button.config(state=NORMAL)
        self.export_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box")
    var = Start(root)
    root.mainloop()  