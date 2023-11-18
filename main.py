import random
from tkinter import *
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}

try:
    df = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = df.to_dict(orient='records')


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_label, text='French', fill='black')
    canvas.itemconfig(word_label, text=current_card['French'], fill='black')
    canvas.itemconfig(bg_front, image=img)
    window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(bg_front, image=img_back)
    canvas.itemconfig(title_label, text='English', fill='white')
    canvas.itemconfig(word_label, text=current_card['English'], fill='white')


def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)

    next_card()


window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title('French-English Flash Cards')

flip_timer = window.after(3000, flip_card)

canvas = Canvas(window, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
img = PhotoImage(file='images/card_front.png')
img_back = PhotoImage(file='images/card_back.png')
bg_front = canvas.create_image(400, 263, image=img)
title_label = canvas.create_text(400, 150, text='', font=('Ariel', 40, 'italic'))
word_label = canvas.create_text(400, 263, text='', font=('Ariel', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

img_button_wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=img_button_wrong, highlightthickness=0, command=next_card)
button_wrong.grid(column=0, row=1)

img_button_right = PhotoImage(file="images/right.png")
button_right = Button(image=img_button_right, highlightthickness=0, command=is_known)
button_right.grid(column=1, row=1)

next_card()

window.mainloop()