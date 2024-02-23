import tkinter
import pandas
import random
import os

BACKGROUND_COLOR = "#B1DDC6"
TOP_WORD_POSITION = (400, 150)
TOP_WORD_FONT = ("Ariel", 40, "italic")
BOTTOM_WORD_POSITION = (400, 263)
BOTTOM_WORD_FONT = ("Ariel", 40, "bold")


def generate_word():
    if len(words_learned) >= 101:
        response = input("You know all the words! Would you like to start over? Type \'YES\' to start over:")
        if response == "YES":
            os.remove("data/words_learned.csv")
            print("Setup complete. Please run the program once again.")
            exit()
        else:
            exit()
    update_words_learned_file()
    for word in words:
        if word in words_learned:
            words.remove(word)
    # print(f"List of words which random word can be generated from: {words})")

    global random_word
    try:
        random_word = random.choice(words)
    except IndexError:
        response = input("You know all the words! Would you like to start over? Type \'YES\' to start over:")
        if response == "YES":
            os.remove("data/words_learned.csv")
            print("Setup complete. Please run the program once again.")
            exit()
        else:
            exit()
    finally:
        pass
        # print(f"Len words: {len(words)}")
        # print(f"Len words learned: {len(words_learned)}")


def word_skip():
    global random_word
    random_word = random.choice(words)
    rewrite_canvas()
    print("Word skipped!")


def rewrite_canvas():
    if card_state == "Front":
        canvas.itemconfig(canvas_image, image=card_front)
        canvas.itemconfig(canvas_top_text, fill="black", text="French")
        canvas.itemconfig(canvas_bottom_text, fill="black", text=random_word["French"])
        # print(random_word["French"])
    elif card_state == "Back":
        canvas.itemconfig(canvas_image, image=card_back)
        canvas.itemconfig(canvas_top_text, fill="white", text="English")
        canvas.itemconfig(canvas_bottom_text, fill="white", text=random_word["English"])
        # print(random_word["English"])


def switch_state():
    global card_state
    if card_state == "Front":
        card_state = "Back"
    elif card_state == "Back":
        card_state = "Front"
    # print(card_state)


def flip_card():
    switch_state()
    rewrite_canvas()
    window.after(3000, flip_card)


def check_words_learned():
    try:
        with open("data/words_learned.csv", "r") as file:
            pass  # print("File exists!")

    except FileNotFoundError:
        with open("data/words_learned.csv", "w") as file:
            file.write("French,English\n")


def word_correct():
    with open("data/words_learned.csv", "a") as file:
        file.write(f"{random_word['French']},{random_word['English']}\n")
    print(f"{random_word} added to words_learned.csv")
    generate_word()
    rewrite_canvas()


def update_words_learned_file():
    with open("data/words_learned.csv", "r") as file:
        global df_words_learned, words_learned
        df_words_learned = pandas.read_csv("data/words_learned.csv")
        words_learned = df_words_learned.to_dict(orient="records")  # List of dictionaries for each learned word




# -------------------------------------MAIN---------------------------------------- #



check_words_learned()

df_french_words = pandas.read_csv("data/french_words.csv")
words = df_french_words.to_dict(orient="records")  # List of dictionaries for each word in French and English

df_words_learned = pandas.read_csv("data/words_learned.csv")
words_learned = df_words_learned.to_dict(orient="records")  # List of dictionaries for each learned word

random_word = {}

card_state = "Front"

generate_word()  # Want to make sure we generate a word after the two lists of dictionaries have been initialized
# Will only generate a word that needs to be studied
# AKA - A word that appears in french_words.csv, but does not appear in words_learned.csv

window = tkinter.Tk()
window.title("Lucas's Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = tkinter.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = tkinter.PhotoImage(file="images/card_front.png")
card_back = tkinter.PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(405, 263, image=card_front)
canvas_top_text = canvas.create_text(TOP_WORD_POSITION, fill="black", text="French", font=TOP_WORD_FONT)
canvas_bottom_text = canvas.create_text(BOTTOM_WORD_POSITION, fill="black", text=random_word["French"], font=BOTTOM_WORD_FONT)
canvas.grid(column=0, row=0, columnspan=2)

incorrect_button_img = tkinter.PhotoImage(file="images/wrong.png")
button1 = tkinter.Button(image=incorrect_button_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=word_skip)
button1.grid(column=0, row=1)

correct_button_img = tkinter.PhotoImage(file="images/right.png")
button2 = tkinter.Button(image=correct_button_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=word_correct)
button2.grid(column=1, row=1)


window.after(3000, flip_card)


window.mainloop()
