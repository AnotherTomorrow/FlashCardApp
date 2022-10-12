from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# Tries to open CSV "to_learn.csv", if it's not there it creates a CSV file.
try:
    data = pandas.read_csv("to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ----------------------------------------FUNCTIONALITY----------------------------------------------#


def flip_card():
    flash_card.itemconfig(background, image=back_card)
    flash_card.itemconfig(title_text, text="English", fill="white")
    flash_card.itemconfig(word_text, text=current_card["English"], fill="white")


def next_card():
    global current_card, time_flip
    window.after_cancel(time_flip)
    current_card = random.choice(to_learn)
    flash_card.itemconfig(background, image=front_card)
    flash_card.itemconfig(title_text, text="French", fill="black")
    flash_card.itemconfig(word_text, text=current_card["French"], fill="black")

    time_flip = window.after(3000, func=flip_card)


def remove_card():
    to_learn.remove(current_card)
    cards_to_learn = pandas.DataFrame(to_learn)
    cards_to_learn.to_csv("To_Learn.csv", index=False)
    next_card()

# ---------------------------------------USER INTERFACE----------------------------------------------#


window = Tk()
window.title("French To English")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

time_flip = window.after(3000, func=flip_card)

front_card = PhotoImage(file="card_front.png")
back_card = PhotoImage(file="card_back.png")


flash_card = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
background = flash_card.create_image(400, 270, image=front_card)
title_text = flash_card.create_text(400, 175, text="", fill="black", font=("Arial", 60, "italic"))
word_text = flash_card.create_text(400, 325, text="", fill="black", font=("Arial", 60, "bold"))
flash_card.grid(column=0, row=0, columnspan=2)


green_button = PhotoImage(file="right.png")
right = Button(window, image=green_button, bg=BACKGROUND_COLOR)
right.grid(column=1, row=1)

red_button = PhotoImage(file="wrong.png")
wrong = Button(window, image=red_button, bg=BACKGROUND_COLOR, command=next_card)
wrong.grid(column=0, row=1)

next_card()

window.mainloop()
