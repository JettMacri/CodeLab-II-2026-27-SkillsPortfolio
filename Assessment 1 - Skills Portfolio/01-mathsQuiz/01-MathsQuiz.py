from tkinter import *
from PIL import Image, ImageTk
import os

root = Tk()
root.title("Quiz Time")
root.geometry("800x450")
root.resizable(False, False)

script_dir = os.path.dirname(os.path.abspath(__file__))

bg_path = os.path.join(script_dir, "Resources", "Quiz.png")
bg_image_raw = Image.open(bg_path)
bg_image_raw = bg_image_raw.resize((800, 450))
bg_img = ImageTk.PhotoImage(bg_image_raw)

bg2_path = os.path.join(script_dir, "Resources", "Diffuculty.png")
bg2_image_raw = Image.open(bg2_path)
bg2_image_raw = bg2_image_raw.resize((800, 450))
bg2_img = ImageTk.PhotoImage(bg2_image_raw)

bg3_path = os.path.join(script_dir, "Resources", "Question.png")
bg3_image_raw = Image.open(bg3_path)
bg3_image_raw = bg3_image_raw.resize((800, 450))
bg3_img = ImageTk.PhotoImage(bg3_image_raw)

canvas = Canvas(root, width=800, height=450)
canvas.pack()

canvas.create_image(0, 0, image=bg_img, anchor="nw")

def go_back_to_main():
    canvas.delete("all")
    canvas.create_image(0, 0, image=bg_img, anchor="nw")
    ready_btn = Button(root, text="READY", bg="#c3c5c6", bd=0, width=22, height=1, command=show_difficulty)
    canvas.create_window(415, 315, window=ready_btn)

def go_back_to_difficulty():
    canvas.delete("all")
    canvas.create_image(0, 0, image=bg2_img, anchor="nw")
    
    back_btn = Button(root, text="BACK", font=("Courier", 9, "bold"), bg="#34495e", fg="#ffffff", bd=0, relief="flat", highlightthickness=0, width=6, height=1, command=go_back_to_main)
    canvas.create_window(415, 315, window=back_btn)

    btn_easy = Button(root, text="EASY", font=("Courier", 11, "bold"), bg="#ffffff", fg="#2ecc71", activebackground="#ffffff", activeforeground="#27ae60", bd=0, relief="flat", highlightthickness=0, width=7, height=1, command=lambda: start_countdown("Easy"))
    canvas.create_window(282, 270, window=btn_easy)

    btn_med = Button(root, text="MEDIUM", font=("Courier", 11, "bold"), bg="#ffffff", fg="#9b59b6", activebackground="#ffffff", activeforeground="#8e44ad", bd=0, relief="flat", highlightthickness=0, width=7, height=1, command=lambda: start_countdown("Medium"))
    canvas.create_window(409, 270, window=btn_med)

    btn_hard = Button(root, text="HARD", font=("Courier", 11, "bold"), bg="#ffffff", fg="#e74c3c", activebackground="#ffffff", activeforeground="#c0392b", bd=0, relief="flat", highlightthickness=0, width=7, height=1, command=lambda: start_countdown("Hard"))
    canvas.create_window(529, 270, window=btn_hard)

def start_quiz(difficulty_level):
    canvas.delete("all")
    canvas.create_image(0, 0, image=bg3_img, anchor="nw")
    
    back_btn = Button(root, text="BACK", font=("Courier", 9, "bold"), bg="#34495e", fg="#ffffff", bd=0, relief="flat", highlightthickness=0, width=6, height=1, command=go_back_to_difficulty)
    canvas.create_window(50, 30, window=back_btn)

    canvas.create_text(400, 215, text=f"Q1: What is 12 + 8 ({difficulty_level})?", font=("Courier", 10, "bold"), fill="#f4d03f")

    opt1 = Button(root, text="A) 15", font=("Courier", 9, "bold"), bg="#ffffff", fg="#333333", bd=0, width=12, height=1)
    canvas.create_window(320, 260, window=opt1)

    opt2 = Button(root, text="B) 20", font=("Courier", 9, "bold"), bg="#ffffff", fg="#333333", bd=0, width=12, height=1)
    canvas.create_window(480, 260, window=opt2)

    opt3 = Button(root, text="C) 25", font=("Courier", 9, "bold"), bg="#ffffff", fg="#333333", bd=0, width=12, height=1)
    canvas.create_window(320, 305, window=opt3)

    opt4 = Button(root, text="D) 30", font=("Courier", 9, "bold"), bg="#ffffff", fg="#333333", bd=0, width=12, height=1)
    canvas.create_window(480, 305, window=opt4)

def run_countdown(count):
    canvas.delete("countdown_text")
    if count > 0:
        canvas.create_text(400, 225, text=str(count), font=("Courier", 40, "bold"), fill="#f4d03f", tags="countdown_text")
        root.after(1000, run_countdown, count - 1)
    else:
        root.after(400, start_quiz, current_difficulty)

def start_countdown(level):
    global current_difficulty
    current_difficulty = level
    canvas.delete("all")
    canvas.create_rectangle(0, 0, 800, 450, fill="#0f0f1a", outline="")
    canvas.create_text(400, 140, text="GET READY!", font=("Courier", 24, "bold"), fill="#ffffff")
    run_countdown(3)

def show_difficulty():
    canvas.delete("all")
    canvas.create_image(0, 0, image=bg2_img, anchor="nw")
    
    back_btn = Button(root, text="BACK", font=("Courier", 9, "bold"), bg="#34495e", fg="#ffffff", bd=0, relief="flat", highlightthickness=0, width=6, height=1, command=go_back_to_main)
    canvas.create_window(50, 30, window=back_btn)

    btn_easy = Button(root, text="EASY", font=("Courier", 11, "bold"), bg="#ffffff", fg="#2ecc71", activebackground="#ffffff", activeforeground="#27ae60", bd=0, relief="flat", highlightthickness=0, width=7, height=1, command=lambda: start_countdown("Easy"))
    canvas.create_window(232, 290, window=btn_easy)

    btn_med = Button(root, text="MEDIUM", font=("Courier", 11, "bold"), bg="#ffffff", fg="#9b59b6", activebackground="#ffffff", activeforeground="#8e44ad", bd=0, relief="flat", highlightthickness=0, width=7, height=1, command=lambda: start_countdown("Medium"))
    canvas.create_window(400, 290, window=btn_med)

    btn_hard = Button(root, text="HARD", font=("Courier", 11, "bold"), bg="#ffffff", fg="#e74c3c", activebackground="#ffffff", activeforeground="#c0392b", bd=0, relief="flat", highlightthickness=0, width=7, height=1, command=lambda: start_countdown("Hard"))
    canvas.create_window(568, 290, window=btn_hard)

ready_btn = Button(root, text="READY", bg="#c3c5c6", bd=0, width=22, height=1, command=show_difficulty)
ready_btn_window = canvas.create_window(415, 315, window=ready_btn)

root.mainloop()