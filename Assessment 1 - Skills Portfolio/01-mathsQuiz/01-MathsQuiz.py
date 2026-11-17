from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Quiz Time")
root.geometry("800x450")
root.resizable(False, False)

# Load background images
bg1_raw = Image.open("Resources/1.png").resize((800, 450), Image.Resampling.LANCZOS)
bg1_img = ImageTk.PhotoImage(bg1_raw)

bg2_raw = Image.open("Resources/2.png").resize((800, 450), Image.Resampling.LANCZOS)
bg2_img = ImageTk.PhotoImage(bg2_raw)

canvas = Canvas(root, width=800, height=450, highlightthickness=0)
canvas.pack(fill="both", expand=True)

def show_page_two():
    canvas.delete("all")
    canvas.create_image(0, 0, image=bg2_img, anchor="nw")
    canvas.create_text(400, 75, text="CHOOSE DIFFICULTY", font=("Courier", 26, "bold"), fill="#f4d03f")
    
    # Difficulty buttons inside the laptop screen area
    btn_easy = Button(root, text="1. Easy", bg="#d0d3d4", font=("Courier", 10, "bold"), width=15)
    btn_mod = Button(root, text="2. Moderate", bg="#d0d3d4", font=("Courier", 10, "bold"), width=15)
    btn_adv = Button(root, text="3. Advanced", bg="#d0d3d4", font=("Courier", 10, "bold"), width=15)
    
    canvas.create_window(400, 200, window=btn_easy)
    canvas.create_window(400, 250, window=btn_mod)
    canvas.create_window(400, 300, window=btn_adv)

# Page 1 Setup
canvas.create_image(0, 0, image=bg1_img, anchor="nw")
canvas.create_text(400, 160, text="QUIZ TIME", font=("Courier", 32, "bold"), fill="#f4d03f")

ready_btn = Button(root, text="", bg="#d0d3d4", activebackground="#a6acaf", relief="raised", bd=2, width=18, height=2, command=show_page_two)
ready_btn_window = canvas.create_window(400, 260, window=ready_btn)

root.mainloop()