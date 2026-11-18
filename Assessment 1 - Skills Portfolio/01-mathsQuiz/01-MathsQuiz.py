from tkinter import *
from PIL import Image, ImageTk
import os
import winsound

root = Tk()
root.title("Quiz Time")
root.geometry("1024x576")
root.resizable(False, False)

script_dir = os.path.dirname(os.path.abspath(__file__))

bg_path = os.path.join(script_dir, "Resources", "Quiz.png")
bg_image_raw = Image.open(bg_path).resize((1024, 576))
bg_img = ImageTk.PhotoImage(bg_image_raw)

bg2_path = os.path.join(script_dir, "Resources", "Diffuculty.png")
bg2_image_raw = Image.open(bg2_path).resize((1024, 576))
bg2_img = ImageTk.PhotoImage(bg2_image_raw)

bg3_path = os.path.join(script_dir, "Resources", "Question.png")
bg3_image_raw = Image.open(bg3_path).resize((1024, 576))
bg3_img = ImageTk.PhotoImage(bg3_image_raw)

ready_bg_path = os.path.join(script_dir, "Resources", "Ready.png")
ready_bg_raw = Image.open(ready_bg_path).resize((1024, 576))
ready_bg_img = ImageTk.PhotoImage(ready_bg_raw)

correct_sound_path = os.path.join(script_dir, "Resources", "correct.wav")
wrong_sound_path = os.path.join(script_dir, "Resources", "wrong.wav")

canvas = Canvas(root, width=1024, height=576, highlightthickness=0)
canvas.pack()

current_difficulty = ""
question_number = 0
score = 0

questions = {
    "Easy": [
        ("5 + 3 = ?", ["6", "7", "8", "9"], 2),
        ("10 - 4 = ?", ["4", "5", "6", "7"], 2),
        ("3 x 2 = ?", ["5", "6", "7", "8"], 1),
        ("12 / 3 = ?", ["2", "3", "4", "5"], 2),
        ("7 + 6 = ?", ["11", "12", "13", "14"], 2)
    ],
    "Medium": [
        ("12 x 4 = ?", ["36", "42", "48", "52"], 2),
        ("81 / 9 = ?", ["7", "8", "9", "11"], 2),
        ("25 + 37 = ?", ["52", "62", "72", "82"], 1),
        ("100 - 46 = ?", ["44", "54", "56", "64"], 1),
        ("8 x 7 = ?", ["48", "54", "56", "64"], 2)
    ],
    "Hard": [
        ("15 x 12 = ?", ["160", "170", "180", "190"], 2),
        ("144 / 12 = ?", ["10", "11", "12", "14"], 2),
        ("25 x 16 = ?", ["350", "375", "400", "450"], 2),
        ("225 / 15 = ?", ["12", "14", "15", "18"], 2),
        ("17 x 13 = ?", ["211", "221", "231", "241"], 1)
    ]
}

def clear_screen():
    canvas.delete("all")
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()

def show_main():
    clear_screen()
    canvas.create_image(0, 0, image=bg_img, anchor="nw")
    ready_btn = Button(root, text="READY", bg="#c3c5c6", bd=0, width=28, height=1, command=show_difficulty)
    canvas.create_window(511, 390, window=ready_btn)

def go_back_to_difficulty():
    clear_screen()
    canvas.create_image(0, 0, image=bg2_img, anchor="nw")
    
    back_btn = Button(root, text="BACK", font=("Courier", 11, "bold"), bg="#34495e", fg="#ffffff", bd=0, relief="flat", highlightthickness=0, width=8, height=1, command=show_main)
    canvas.create_window(70, 40, window=back_btn)

    btn_easy = Button(root, text="EASY", font=("Courier", 14, "bold"), bg="#ffffff", fg="#2ecc71", activebackground="#ffffff", activeforeground="#27ae60", bd=0, relief="flat", highlightthickness=0, width=8, height=1, command=lambda: start_countdown("Easy"))
    canvas.create_window(361, 345, window=btn_easy)

    btn_med = Button(root, text="MEDIUM", font=("Courier", 14, "bold"), bg="#ffffff", fg="#9b59b6", activebackground="#ffffff", activeforeground="#8e44ad", bd=0, relief="flat", highlightthickness=0, width=8, height=1, command=lambda: start_countdown("Medium"))
    canvas.create_window(523, 345, window=btn_med)

    btn_hard = Button(root, text="HARD", font=("Courier", 14, "bold"), bg="#ffffff", fg="#e74c3c", activebackground="#ffffff", activeforeground="#c0392b", bd=0, relief="flat", highlightthickness=0, width=8, height=1, command=lambda: start_countdown("Hard"))
    canvas.create_window(677, 345, window=btn_hard)

def start_quiz():
    global question_number
    clear_screen()
    canvas.create_image(0, 0, image=bg3_img, anchor="nw")
    
    back_btn = Button(root, text="BACK", font=("Courier", 11, "bold"), bg="#34495e", fg="#ffffff", bd=0, relief="flat", highlightthickness=0, width=8, height=1, command=go_back_to_difficulty)
    canvas.create_window(70, 40, window=back_btn)

    current_questions = questions[current_difficulty]

    if question_number >= len(current_questions):
        show_results()
        return

    question, options, correct_answer = current_questions[question_number]

    canvas.create_text(512, 230, text=f"Q{question_number + 1}: {question}", font=("Courier", 14, "bold"), fill="#f4d03f")
    positions = [
        (410, 290),
        (614, 290),
        (410, 350),
        (614, 350)
    ]

    for i, option in enumerate(options):
        if i < len(positions):
            x_pos, y_pos = positions[i]
            opt_btn = Button(
                root, 
                text=option, 
                font=("Courier", 11, "bold"), 
                bg="#ffffff", 
                fg="#333333", 
                bd=0, 
                width=14, 
                height=1, 
                command=lambda ans=i: check_answer(ans, correct_answer)
            )
            canvas.create_window(x_pos, y_pos, window=opt_btn)

def check_answer(answer, correct_answer):
    global score, question_number
    clear_screen()
    canvas.create_image(0, 0, image=bg3_img, anchor="nw")

    if answer == correct_answer:
        score += 1
        msg = "CORRECT!"
        color = "#2ecc71"
        if os.path.exists(correct_sound_path):
            winsound.PlaySound(correct_sound_path, winsound.SND_ASYNC | winsound.SND_FILENAME)
    else:
        msg = "INCORRECT!"
        color = "#e74c3c"
        if os.path.exists(wrong_sound_path):
            winsound.PlaySound(wrong_sound_path, winsound.SND_ASYNC | winsound.SND_FILENAME)

    canvas.create_text(
        512, 335,
        text=msg,
        font=("Courier", 20, "bold"),
        fill=color
    )

    question_number += 1
    root.after(1000, start_quiz)

def show_results():
    clear_screen()
    canvas.create_image(0, 0, image=bg3_img, anchor="nw")

    canvas.create_text(
        512, 315,
        text=f"QUIZ DONE! SCORE: {score} / 5",
        font=("Courier", 14, "bold"),
        fill="#f4d03f"
    )

    restart_btn = Button(
        root,
        text="PLAY AGAIN",
        font=("Courier", 11, "bold"),
        bg="#ffffff",
        fg="#333333",
        bd=0,
        width=14,
        height=1,
        command=show_difficulty
    )
    canvas.create_window(512, 375, window=restart_btn)

def run_countdown(count):
    canvas.delete("countdown_text")
    if count > 0:
        canvas.create_text(500, 315, text=str(count), font=("Courier", 55, "bold"), fill="#f4d03f", tags="countdown_text")
        root.after(1000, run_countdown, count - 1)
    else:
        root.after(400, start_quiz)

def start_countdown(level):
    global current_difficulty, question_number, score
    current_difficulty = level
    question_number = 0
    score = 0
    clear_screen()
    canvas.create_image(0, 0, image=ready_bg_img, anchor="nw")
    run_countdown(3)

def show_difficulty():
    clear_screen()
    canvas.create_image(0, 0, image=bg2_img, anchor="nw")
    
    back_btn = Button(root, text="BACK", font=("Courier", 11, "bold"), bg="#34495e", fg="#ffffff", bd=0, relief="flat", highlightthickness=0, width=8, height=1, command=show_main)
    canvas.create_window(70, 40, window=back_btn)

    btn_easy = Button(root, text="EASY", font=("Courier", 14, "bold"), bg="#ffffff", fg="#2ecc71", activebackground="#ffffff", activeforeground="#27ae60", bd=0, relief="flat", highlightthickness=0, width=8, height=1, command=lambda: start_countdown("Easy"))
    canvas.create_window(361, 345, window=btn_easy)

    btn_med = Button(root, text="MEDIUM", font=("Courier", 14, "bold"), bg="#ffffff", fg="#9b59b6", activebackground="#ffffff", activeforeground="#8e44ad", bd=0, relief="flat", highlightthickness=0, width=8, height=1, command=lambda: start_countdown("Medium"))
    canvas.create_window(523, 345, window=btn_med)

    btn_hard = Button(root, text="HARD", font=("Courier", 14, "bold"), bg="#ffffff", fg="#e74c3c", activebackground="#ffffff", activeforeground="#c0392b", bd=0, relief="flat", highlightthickness=0, width=8, height=1, command=lambda: start_countdown("Hard"))
    canvas.create_window(677, 345, window=btn_hard)

show_main()

root.mainloop()