import random
from tkinter import *
import pandas as pd


class FlashCardApp:
    def __init__(self, window):
        self.window = window
        self.window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
        self.window.title('French-English Flash Cards')

        self.flip_timer = self.window.after(3000, self.flip_card)

        self.canvas = Canvas(self.window, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.img = PhotoImage(file='images/card_front.png')
        self.img_back = PhotoImage(file='images/card_back.png')
        self.bg_front = self.canvas.create_image(400, 263, image=self.img)
        self.title_label = self.canvas.create_text(400, 150, text='', font=('Ariel', 40, 'italic'))
        self.word_label = self.canvas.create_text(400, 263, text='', font=('Ariel', 60, 'bold'))
        self.canvas.grid(column=0, row=0, columnspan=2)

        self.img_button_wrong = PhotoImage(file="images/wrong.png")
        self.button_wrong = Button(image=self.img_button_wrong, highlightthickness=0, command=self.next_card)
        self.button_wrong.grid(column=0, row=1)

        self.img_button_right = PhotoImage(file="images/right.png")
        self.button_right = Button(image=self.img_button_right, highlightthickness=0, command=self.is_known)
        self.button_right.grid(column=1, row=1)

        self.to_learn = {}
        try:
            self.df = pd.read_csv('data/words_to_learn.csv')
        except FileNotFoundError:
            self.original_data = pd.read_csv('data/french_words.csv')
            self.to_learn = self.original_data.to_dict(orient='records')
        else:
            self.to_learn = self.df.to_dict(orient='records')

        self.next_card()

    def next_card(self):
        self.window.after_cancel(self.flip_timer)
        self.current_card = random.choice(self.to_learn)
        self.canvas.itemconfig(self.title_label, text='French', fill='black')
        self.canvas.itemconfig(self.word_label, text=self.current_card['French'], fill='black')
        self.canvas.itemconfig(self.bg_front, image=self.img)
        self.window.after(3000, self.flip_card)

    def flip_card(self):
        self.canvas.itemconfig(self.bg_front, image=self.img_back)
        self.canvas.itemconfig(self.title_label, text='English', fill='white')
        self.canvas.itemconfig(self.word_label, text=self.current_card['English'], fill='white')

    def is_known(self):
        self.to_learn.remove(self.current_card)
        data = pd.DataFrame(self.to_learn)
        data.to_csv('data/words_to_learn.csv', index=False)

        self.next_card()


if __name__ == "__main__":
    BACKGROUND_COLOR = "#B1DDC6"
    window = Tk()
    app = FlashCardApp(window)
    window.mainloop()
