import tkinter as tk
import subprocess
from PIL import Image, ImageTk

def start_game():
    root.destroy() #close start screen
    subprocess.run(["python", "E:\Downloads\Blackjack-coursework\mains\main_game.py"])#run main game script

#initialize Tkinter
root = tk.Tk()
root.geometry('1080x720')
root.configure(background='#458B00')
root.title('BlackJack - Start Screen')

#title Label
title_label = tk.Label(root, text="Welcome to BlackJack!", font=("Arial", 30, "bold"), bg='#458B00', fg='white')
title_label.pack(pady=1)

#background Image
try:
    bg_img = Image.open("e:\Downloads\main.png") 
    bg_img = bg_img.resize((1080, 720))  
    bg_img = ImageTk.PhotoImage(bg_img)
    bg_label = tk.Label(root, image=bg_img, bg='#458B00')
    bg_label.image = bg_img
    bg_label.pack(pady=1)
except FileNotFoundError:
    print("Start screen image not found.")

#start Button
start_btn = tk.Button(root, text="play for free", font=("Arial", 20, "bold"), bg="green", fg="white", command=start_game)
start_btn.place(x=370, y=490,width=330, height=70)

start_btn.lower()
bg_label.bind("<Button-1>", lambda e: start_btn.invoke())


#tk loop
root.mainloop()
