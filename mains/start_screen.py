import tkinter as tk
import subprocess
from PIL import Image, ImageTk

def start_game():
    root.destroy()  # Close start screen
    subprocess.run(["python3", "mains/main_game.py"])

#tk stuff
root = tk.Tk()
root.geometry('1080x720')
root.configure(background='#458B00')
root.title('BlackJack - Start Screen')

#name
title_label = tk.Label(root, text="Welcome to BlackJack!", font=("Arial", 30, "bold"), bg='#458B00', fg='white')
title_label.pack(pady=10)

#backgroud image etc
bg_label = None #initialize bg_label was buggin out before
try:
    bg_img = Image.open("main.png") 
    bg_img = bg_img.resize((1080, 720))  
    bg_img = ImageTk.PhotoImage(bg_img)
    bg_label = tk.Label(root, image=bg_img, bg='#458B00')
    bg_label.image = bg_img
    bg_label.pack(pady=1)
except FileNotFoundError:
    print("Start screen image not found.")

#start Button
start_btn = tk.Button(root, text="Play for Free", font=("Arial", 20, "bold"), bg="green", fg="white", command=start_game)
start_btn.place(x=370, y=490, width=330, height=70)

start_btn.lower() # puts tkinter button behind so can see button design 

#so when mouse clicks anywhere on screen, start button is called/pressed
if bg_label:  
    bg_label.bind("<Button-1>", lambda e: start_btn.invoke()) #invoke kinda like calls the button coz it aint a function

#roooot
root.mainloop()
