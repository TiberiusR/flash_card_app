from tkinter import *
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
TIMER = None
CURRENT_CARD = {}

# Data
try:
    DATA = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    DATA = pd.read_csv("data/french_words.csv")

WORDS_DICT = DATA.to_dict(orient="records")

# Functions


def next_card():
    global CURRENT_CARD, flip_timer

    window.after_cancel(flip_timer)
    CURRENT_CARD = choice(WORDS_DICT)
    canvas.itemconfig(card, image=CARD_FRONT_IMG)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=CURRENT_CARD["French"], fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card, image=CARD_BACK_IMG)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=CURRENT_CARD["English"], fill="white")


def is_known():
    WORDS_DICT.remove(CURRENT_CARD)
    data = pd.DataFrame(WORDS_DICT)
    data.to_csv("data/words_to_learn.csv", index=False)

    next_card()


# UI
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

# Images
RIGHT_IMG = PhotoImage(file="images/right.png")
WRONG_IMG = PhotoImage(file="images/wrong.png")
CARD_FRONT_IMG = PhotoImage(file="images/card_front.png")
CARD_BACK_IMG = PhotoImage(file="images/card_back.png")

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(400, 263, image=CARD_FRONT_IMG)
canvas.grid(column=0, row=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))

# Buttons
right_button = Button(image=RIGHT_IMG, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

wrong_button = Button(image=WRONG_IMG, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)


next_card()

window.mainloop()
