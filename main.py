from tkinter import *
import pandas as pd
import random
# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = '#B1DDC6'
WORD_FONT_FRONT = ('Ariel', 60, 'bold')
WORD_FONT_BACK = ('Ariel', 40, 'italic')
DEFINITION_FONT = ('Ariel', 20)
current_card = {}
# ---------------------------- LOAD DATA ------------------------------- #
# Check if user has a personalized list of words, if not open default vocab list
try:
    data = pd.read_csv('data/words_to_learn.csv')
    to_learn = data.to_dict(orient='records')
    if len(to_learn) < 1:
        raise ValueError('The list is empty')
except (FileNotFoundError, ValueError):
    original_data = pd.read_csv('data/vocab_words.csv')
    to_learn = original_data.to_dict(orient='records')


# ---------------------------- NEXT CARD ------------------------------- #
def next_card():
    """
    Choose a random word from to_learn list.
    Show front of flashcard for 3 seconds, then flip to show definition
    """
    if len(to_learn) > 0:
        global current_card, flip_timer
        window.after_cancel(flip_timer)
        current_card = random.choice(to_learn)
        canvas.itemconfig(top_text, text='', fill='black')
        canvas.itemconfig(bottom_text, text=current_card['word'], fill='black', font=WORD_FONT_FRONT)
        canvas.itemconfig(card_background, image=card_front_img)
        flip_timer = window.after(3000, func=flip_card)


# ---------------------------- FLIP CARD ------------------------------- #
def flip_card():
    """
    Flip the card from front side (showing word) to back (showing word and definition)
    """
    canvas.itemconfig(top_text, text=current_card['word'], fill='white')
    canvas.itemconfig(bottom_text, text=current_card['definition'], fill='white', font=DEFINITION_FONT)
    canvas.itemconfig(card_background, image=card_back_img)


# --------------------------- REMOVE CARD ------------------------------ #
def remove_card():
    """
    Remove word from to_learn list
    Save modified list
    Switch to next card (if available)
    """
    if len(to_learn) > 0:
        to_learn.remove(current_card)
        df = pd.DataFrame(to_learn)
        df.to_csv('data/words_to_learn.csv', index=False)
        next_card()
    else:
        global flip_timer
        window.after_cancel(flip_timer)
        canvas.itemconfig(top_text, text='', fill='black')
        canvas.itemconfig(bottom_text, text='Done!', fill='black')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Flash Cards')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Flip from front to back of flashcard
flip_timer = window.after(3000, func=flip_card)

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file='images/card_front.png')
card_back_img = PhotoImage(file='images/card_back.png')
card_background = canvas.create_image(400, 263, image=card_front_img)
top_text = canvas.create_text(400, 150, text='', fill='black', font=WORD_FONT_BACK)
bottom_text = canvas.create_text(400, 265, text='', fill='black', font=WORD_FONT_FRONT)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_button_img = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

right_button_img = PhotoImage(file='images/right.png')
right_button = Button(image=right_button_img, highlightthickness=0, command=remove_card)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()

