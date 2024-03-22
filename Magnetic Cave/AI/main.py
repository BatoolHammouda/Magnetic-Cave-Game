from tkinter import *
import random
def next_turn(row, col):
    global player
    if btns[row][col]['text'] == "" and not check_winner():
        if (
            (col == 0 or btns[row][col-1]['text'] != "") or
            (col == 7 or btns[row][col+1]['text'] != "")
        ):
            btns[row][col]['text'] = player
            if check_winner():
                label.config(text=(player + " wins!"))
            elif check_tie():
                label.config(text=("Tie, No Winner!"))
            else:
                player = players[1] if player == players[0] else players[0]
                label.config(text=(player + " turn"))
        else:
            label.config(text=("Invalid move. Try again."))

def check_winner():
    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]  # Down, Right, Diagonal, Reverse Diagonal

    for row in range(8):
        for col in range(8):
            if btns[row][col]['text'] != "":
                symbol = btns[row][col]['text']
                for direction in directions:
                    dx, dy = direction
                    count = 1
                    for i in range(1, 5):
                        new_row = row + i * dx
                        new_col = col + i * dy
                        if (
                            new_row < 0 or new_row >= 8 or
                            new_col < 0 or new_col >= 8 or
                            btns[new_row][new_col]['text'] != symbol
                        ):
                            break
                        count += 1
                    if count == 5:
                        return True

    return False

def check_tie():
    for row in range(8):
        for col in range(8):
            if btns[row][col]['text'] == "":
                return False
    return True


def start_new_game():
    global player
    player = random.choice(players)
    label.config(text=(player + " turn"))
    for row in range(8):
        for col in range(8):
            btns[row][col]['text'] = ""

window = Tk()
window.title("Magnetic Cave")
players = ["■", "□"]
player = random.choice(players)
btns = [[0] * 8 for _ in range(8)]
label = Label(text=(player + " turn"), font=('consolas', 15))
label.pack(side="top")
restart_btn = Button(text="Restart", font=('consolas', 10), command=start_new_game)
restart_btn.pack(side="top")
btns_frame = Frame(window)
btns_frame.pack()

# Define colors
color1 = "white"
color2 = "beige"

for row in range(8):
    for col in range(8):
        # Alternate between color1 and color2 for the background
        if (row + col) % 2 == 0:
            bg_color = color1
        else:
            bg_color = color2

        btns[row][col] = Button(btns_frame, text="", font=('consolas', 30), width=2, height=1,
                                command=lambda row=row, col=col: next_turn(row, col),
                                bg=bg_color)
        btns[row][col].grid(row=row, column=col)


window.mainloop()
