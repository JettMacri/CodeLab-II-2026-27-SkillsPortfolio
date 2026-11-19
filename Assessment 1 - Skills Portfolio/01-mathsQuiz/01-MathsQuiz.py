from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pygame

# initialize mixer settings and channels for sfx and music
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()
pygame.mixer.set_num_channels(8)

# main window setup for the quiz app
root = Tk()
root.title("Quiz Time")
root.geometry("1024x576")
root.resizable(False, False)

# resolve base directory so resource paths work regardless of run location
script_dir = os.path.dirname(os.path.abspath(__file__))

# sets quizicon.png from Resources as the window icon using iconphoto
icon_path = os.path.join(script_dir, "Resources", "quizicon.png")
if os.path.exists(icon_path):
    app_icon = ImageTk.PhotoImage(Image.open(icon_path))
    root.iconphoto(False, app_icon)

# loading background images and resizing them to fit the window
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

# audio file paths inside the resources folder
correct_sound_path = os.path.join(script_dir, "Resources", "correct.mp3")
wrong_sound_path = os.path.join(script_dir, "Resources", "wrong.mp3")
bg_music_path = os.path.join(script_dir, "Resources", "BGMuisc.wav")

# default volume levels
sfx_volume = 0.7
bgm_volume = 0.4

# audio objects and playback tracking
correct_sfx = None
wrong_sfx = None
bgm_sound = None
bgm_channel = pygame.mixer.Channel(0)
using_music_stream = False


# load sound effects safely so missing files dont crash the app
def load_sound_file(path):
    # skip loading if the file does not exist
    if not os.path.exists(path):
        return None
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None


# start background music, with a channel fallback if music stream has trouble
def start_bgm():
    global bgm_sound, using_music_stream

    if not os.path.exists(bg_music_path):
        return

    # try streaming music first
    try:
        pygame.mixer.music.load(bg_music_path)
        pygame.mixer.music.set_volume(bgm_volume)
        pygame.mixer.music.play(-1)
        using_music_stream = True
        return
    except pygame.error:
        using_music_stream = False

    # fallback to Sound object on channel 0 if streaming fails
    try:
        bgm_sound = pygame.mixer.Sound(bg_music_path)
        bgm_channel.set_volume(bgm_volume)
        bgm_channel.play(bgm_sound, loops=-1)
    except pygame.error:
        bgm_sound = None


# keeps bgm looping across screens if it stops
def check_bgm():
    # restart streamed music if it stopped
    if using_music_stream:
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.set_volume(bgm_volume)
                pygame.mixer.music.play(-1)
        except pygame.error:
            pass
    # restart channel fallback music if it stopped
    elif bgm_sound is not None:
        if not bgm_channel.get_busy():
            bgm_channel.set_volume(bgm_volume)
            bgm_channel.play(bgm_sound, loops=-1)


# play sfx when user answers a question
def play_sfx(sound_obj):
    if sound_obj is None:
        return
    # stop any overlapping playback so the feedback sound plays cleanly
    sound_obj.set_volume(sfx_volume)
    sound_obj.stop()
    sound_obj.play()


# update sfx volume from the slider
def set_sfx_volume(val):
    global sfx_volume
    # slider gives 0-100, pygame expects 0.0-1.0
    sfx_volume = float(val) / 100.0
    if correct_sfx is not None:
        correct_sfx.set_volume(sfx_volume)
    if wrong_sfx is not None:
        wrong_sfx.set_volume(sfx_volume)


# update bgm volume from the slider
def set_bgm_volume(val):
    global bgm_volume
    # slider gives 0-100, pygame expects 0.0-1.0
    bgm_volume = float(val) / 100.0
    if using_music_stream:
        try:
            pygame.mixer.music.set_volume(bgm_volume)
        except pygame.error:
            pass
    else:
        bgm_channel.set_volume(bgm_volume)


# clean up audio when window closes
def on_close():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except pygame.error:
        pass
    root.destroy()


# run cleanup when user clicks the window close button
root.protocol("WM_DELETE_WINDOW", on_close)

# main canvas holding backgrounds, text, and embedded widgets
canvas = Canvas(
    root,
    width=1024,
    height=576,
    highlightthickness=0
)
canvas.pack()

# tracking game state
current_difficulty = ""
question_number = 0
score = 0
active_screen = "main"
current_correct_answer = None

# questions grouped by difficulty level (8 per level)
questions = {
    "Easy": [
        ("5 + 3 = ?", ["6", "7", "8", "9"], 2),
        ("10 - 4 = ?", ["4", "5", "6", "7"], 2),
        ("3 x 2 = ?", ["5", "6", "7", "8"], 1),
        ("12 / 3 = ?", ["2", "3", "4", "5"], 2),
        ("7 + 6 = ?", ["11", "12", "13", "14"], 2),
        ("9 - 5 = ?", ["3", "4", "5", "6"], 1),
        ("4 x 3 = ?", ["10", "11", "12", "13"], 2),
        ("15 / 3 = ?", ["4", "5", "6", "7"], 1)
    ],
    "Medium": [
        ("12 x 4 = ?", ["36", "42", "48", "52"], 2),
        ("81 / 9 = ?", ["7", "8", "9", "11"], 2),
        ("25 + 37 = ?", ["52", "62", "72", "82"], 1),
        ("100 - 46 = ?", ["44", "54", "56", "64"], 1),
        ("8 x 7 = ?", ["48", "54", "56", "64"], 2),
        ("96 / 8 = ?", ["10", "11", "12", "13"], 2),
        ("48 + 29 = ?", ["67", "77", "87", "97"], 1),
        ("73 - 28 = ?", ["35", "45", "55", "65"], 1)
    ],
    "Hard": [
        ("15 x 12 = ?", ["160", "170", "180", "190"], 2),
        ("144 / 12 = ?", ["10", "11", "12", "14"], 2),
        ("25 x 16 = ?", ["350", "375", "400", "450"], 2),
        ("225 / 15 = ?", ["12", "14", "15", "18"], 2),
        ("17 x 13 = ?", ["211", "221", "231", "241"], 1),
        ("19 x 14 = ?", ["256", "266", "276", "286"], 1),
        ("324 / 18 = ?", ["16", "17", "18", "19"], 2),
        ("145 + 268 = ?", ["403", "413", "423", "433"], 1)
    ]
}


# shows instructions using a messagebox popup
def show_instructions():
    messagebox.showinfo(
        "Instructions",
        "Click READY (or press Enter) to pick a difficulty.\n"
        "Select an answer by clicking or pressing keys 1-4.\n"
        "Use the SFX and BGM sliders in the top-right to adjust volume."
    )


# handles keyboard shortcuts with root.bind("<Key>", ...)
def handle_keypress(event):
    # Enter starts from main screen
    if active_screen == "main" and event.keysym == "Return":
        show_difficulty()
    # number keys 1-4 map to option indices 0-3 during quiz
    elif active_screen == "quiz" and event.char in ("1", "2", "3", "4") and current_correct_answer is not None:
        check_answer(int(event.char) - 1, current_correct_answer)
    # Enter replays from results screen
    elif active_screen == "results" and event.keysym == "Return":
        show_difficulty()


# listen for key presses across the window
root.bind("<Key>", handle_keypress)


# draws the sfx and bgm sliders on each screen
def add_audio_controls():
    check_bgm()

    # sfx label and horizontal slider
    sfx_label = Label(
        root,
        text="SFX",
        font=("Courier", 10, "bold"),
        bg="#34495e",
        fg="#ffffff"
    )
    canvas.create_window(840, 28, window=sfx_label)

    sfx_slider = Scale(
        root,
        from_=0,
        to=100,
        orient=HORIZONTAL,
        bg="#34495e",
        fg="#ffffff",
        highlightthickness=0,
        troughcolor="#ffffff",
        showvalue=0,
        command=set_sfx_volume
    )
    sfx_slider.set(int(sfx_volume * 100))
    canvas.create_window(
        935, 28,
        window=sfx_slider,
        width=120,
        height=18
    )

    # bgm label and horizontal slider
    bgm_label = Label(
        root,
        text="BGM",
        font=("Courier", 10, "bold"),
        bg="#34495e",
        fg="#ffffff"
    )
    canvas.create_window(840, 56, window=bgm_label)

    bgm_slider = Scale(
        root,
        from_=0,
        to=100,
        orient=HORIZONTAL,
        bg="#34495e",
        fg="#ffffff",
        highlightthickness=0,
        troughcolor="#ffffff",
        showvalue=0,
        command=set_bgm_volume
    )
    bgm_slider.set(int(bgm_volume * 100))
    canvas.create_window(
        935, 56,
        window=bgm_slider,
        width=120,
        height=18
    )


# removes old canvas items and widgets before switching pages
def clear_screen():
    canvas.delete("all")

    # keep the main canvas and remove other child widgets
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()


# start screen
def show_main():
    global active_screen
    active_screen = "main"
    clear_screen()

    canvas.create_image(
        0, 0,
        image=bg_img,
        anchor="nw"
    )

    # main start button
    ready_btn = Button(
        root,
        text="READY",
        font=("Courier", 11, "bold"),
        bg="#c3c5c6",
        bd=0,
        width=14,
        height=1,
        command=show_difficulty
    )
    canvas.create_window(
        511, 390,
        window=ready_btn
    )

    # button that opens the instructions popup
    info_btn = Button(
        root,
        text="HOW TO PLAY",
        font=("Courier", 10, "bold"),
        bg="#34495e",
        fg="#ffffff",
        bd=0,
        width=14,
        height=1,
        command=show_instructions
    )
    canvas.create_window(
        511, 430,
        window=info_btn
    )

    add_audio_controls()


# difficulty selection screen
def show_difficulty():
    global active_screen
    active_screen = "difficulty"
    clear_screen()

    canvas.create_image(
        0, 0,
        image=bg2_img,
        anchor="nw"
    )

    # return to start screen
    back_btn = Button(
        root,
        text="BACK",
        font=("Courier", 12, "bold"),
        bg="#34495e",
        fg="#ffffff",
        bd=0,
        relief="flat",
        highlightthickness=0,
        width=8,
        height=1,
        command=show_main
    )
    canvas.create_window(
        70, 40,
        window=back_btn
    )

    # difficulty buttons for Easy, Medium, and Hard
    btn_easy = Button(
        root,
        text="EASY",
        font=("Courier", 15, "bold"),
        bg="#ffffff",
        fg="#2ecc71",
        activebackground="#ffffff",
        activeforeground="#27ae60",
        bd=0,
        relief="flat",
        highlightthickness=0,
        width=8,
        height=1,
        command=lambda: start_countdown("Easy")
    )
    canvas.create_window(
        361, 345,
        window=btn_easy
    )

    btn_med = Button(
        root,
        text="MEDIUM",
        font=("Courier", 15, "bold"),
        bg="#ffffff",
        fg="#9b59b6",
        activebackground="#ffffff",
        activeforeground="#8e44ad",
        bd=0,
        relief="flat",
        highlightthickness=0,
        width=8,
        height=1,
        command=lambda: start_countdown("Medium")
    )
    canvas.create_window(
        523, 345,
        window=btn_med
    )

    btn_hard = Button(
        root,
        text="HARD",
        font=("Courier", 15, "bold"),
        bg="#ffffff",
        fg="#e74c3c",
        activebackground="#ffffff",
        activeforeground="#c0392b",
        bd=0,
        relief="flat",
        highlightthickness=0,
        width=8,
        height=1,
        command=lambda: start_countdown("Hard")
    )
    canvas.create_window(
        677, 345,
        window=btn_hard
    )

    add_audio_controls()


# resets score and question index before countdown
def start_countdown(level):
    global current_difficulty, question_number, score, active_screen

    # reset counters for a fresh round
    active_screen = "countdown"
    current_difficulty = level
    question_number = 0
    score = 0

    clear_screen()

    canvas.create_image(
        0, 0,
        image=ready_bg_img,
        anchor="nw"
    )

    add_audio_controls()
    run_countdown(3)


# 3 second countdown before showing questions
def run_countdown(count):
    canvas.delete("countdown_text")

    if count > 0:
        canvas.create_text(
            500, 315,
            text=str(count),
            font=("Courier", 65, "bold"),
            fill="#f4d03f",
            tags="countdown_text"
        )
        # step down every second using root.after
        root.after(1000, run_countdown, count - 1)
    else:
        # short delay after countdown before first question
        root.after(400, start_quiz)


# displays the current question and answer buttons
def start_quiz():
    global question_number, active_screen, current_correct_answer

    active_screen = "quiz"
    clear_screen()

    canvas.create_image(
        0, 0,
        image=bg3_img,
        anchor="nw"
    )

    # go back to difficulty selection
    back_btn = Button(
        root,
        text="BACK",
        font=("Courier", 12, "bold"),
        bg="#34495e",
        fg="#ffffff",
        bd=0,
        relief="flat",
        highlightthickness=0,
        width=8,
        height=1,
        command=show_difficulty
    )
    canvas.create_window(
        70, 40,
        window=back_btn
    )

    add_audio_controls()

    current_questions = questions.get(current_difficulty, [])

    # move to results once all questions are finished
    if question_number >= len(current_questions):
        current_correct_answer = None
        show_results()
        return

    question, options, correct_answer = current_questions[question_number]
    current_correct_answer = correct_answer

    # show current question text
    canvas.create_text(
        512, 230,
        text=f"Q{question_number + 1}: {question}",
        font=("Courier", 20, "bold"),
        fill="#f4d03f"
    )

    # 2x2 grid positions for the four option buttons
    positions = [
        (410, 290),
        (614, 290),
        (410, 350),
        (614, 350)
    ]

    # build option buttons inside the canvas
    for i, option in enumerate(options):
        if i < len(positions):
            x_pos, y_pos = positions[i]

            opt_btn = Button(
                root,
                text=option,
                font=("Courier", 14, "bold"),
                bg="#ffffff",
                fg="#333333",
                bd=0,
                width=14,
                height=1,
                command=lambda ans=i: check_answer(ans, correct_answer)
            )
            canvas.create_window(
                x_pos,
                y_pos,
                window=opt_btn
            )


# checks selected answer, plays sfx, updates score, and moves to next question
def check_answer(answer, correct_answer):
    global score, question_number, current_correct_answer

    # block number-key answers while feedback is shown
    current_correct_answer = None
    clear_screen()

    canvas.create_image(
        0, 0,
        image=bg3_img,
        anchor="nw"
    )

    add_audio_controls()

    # score and play feedback sound
    if answer == correct_answer:
        score += 1
        msg = "CORRECT!"
        color = "#2ecc71"
        play_sfx(correct_sfx)
    else:
        msg = "INCORRECT!"
        color = "#e74c3c"
        play_sfx(wrong_sfx)

    canvas.create_text(
        512, 335,
        text=msg,
        font=("Courier", 23, "bold"),
        fill=color
    )

    # advance to next question after 1 second
    question_number += 1
    root.after(1000, start_quiz)


# final score screen with replay button
def show_results():
    global active_screen
    active_screen = "results"
    clear_screen()

    canvas.create_image(
        0, 0,
        image=bg3_img,
        anchor="nw"
    )

    add_audio_controls()

    total_q = len(questions.get(current_difficulty, []))

    canvas.create_text(
        512, 315,
        text=f"QUIZ DONE! SCORE: {score} / {total_q}",
        font=("Courier", 17, "bold"),
        fill="#f4d03f"
    )

    # replay button returns to difficulty screen
    restart_btn = Button(
        root,
        text="PLAY AGAIN",
        font=("Courier", 12, "bold"),
        bg="#ffffff",
        fg="#333333",
        bd=0,
        width=14,
        height=1,
        command=show_difficulty
    )
    canvas.create_window(
        512, 375,
        window=restart_btn
    )


# preload sound effects and start the app
correct_sfx = load_sound_file(correct_sound_path)
wrong_sfx = load_sound_file(wrong_sound_path)

# set initial sound effect volumes
if correct_sfx is not None:
    correct_sfx.set_volume(sfx_volume)
if wrong_sfx is not None:
    wrong_sfx.set_volume(sfx_volume)

# start music and open first screen
start_bgm()
show_main()

root.mainloop()