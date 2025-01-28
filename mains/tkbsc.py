import tkinter as tk
from tkinter import Label, Button, Entry 
from PIL import Image, ImageTk
import random
import os

def siuuu(): #placeholder for commands in buttons etc
    print("")

image_directory = "mains/PNG-cards-1.3/"
card_back = "mains/PNG-cards-1.3/card back red.png"
image_refs = []
bkg="r/mains/3217577-middle.png"
current_bet = 0
balance = 100
player_width = 220
dealer_width = 450
player_length = 200
dealer_length = 200
root = tk.Tk()
root.geometry('1080x720')
root.configure(background='#458B00')
root.title('BlackJack')



#lda card image
card_image_path = "mains/PNG-cards-1.3/2_of_clubs.png"  
card_image = Image.open(card_image_path)

#resize image coz far too big
card_image = card_image.resize((120, 180)) 
card_photo = ImageTk.PhotoImage(card_image)

#Label display card 
for i in range(2):
    card_label = Label(root, image=card_photo, bg='#458B00')
    card_label.place(x=player_width, y=player_length)  # Place the card at player position
    player_width += 25

#dealer cards
player_width+=200
for i in range(2):
    card_label = Label(root, image=card_photo, bg='#458B00')
    card_label.place(x=dealer_width, y=dealer_length)  # Place the card at dealer position
    dealer_width += 25
    



#ui stuff buttons labels etc
hit_button = Button(root, text='Hit', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
hit_button.place(x=98, y=92)
stand_button = Button(root, text='Stand', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
stand_button.place(x=632, y=89)

bets1=Button(root, text='1', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
bets1.place(x=270, y=530)
bets2=Button(root, text='5', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
bets2.place(x=335, y=530)
bets3=Button(root, text='10', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
bets3.place(x=370, y=530)
bets4=Button(root, text='20', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
bets4.place(x=415, y=530)
bets5=Button(root, text='50', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
bets5.place(x=462, y=530)
bets6=Button(root, text='100', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
bets6.place(x=510, y=530)
bets7=Button(root, text='max', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
bets7.place(x=560, y=530)
bets8=Button(root, text='min', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
bets8.place(x=610, y=530)
bets9=Button(root, text='Reset\nbet to 0', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
bets9.place(x=700, y=530)

play_again_button = Button(root, text='play again', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
play_again_button.place(x=350, y=420)

quit_button = Button(root, text='quit', bg='#FFFAFA', font=('arial', 12, 'normal'), command=quit)
quit_button.place(x=200, y=420)

betbox=Button(root, text='Submit Bet Amount', bg='#FFFAFA', font=('arial', 12, 'normal'), command=siuuu)
betbox.place(x=355, y=650)
bet = Entry(root)
bet.place(x=360, y=625)
Label(root, text='Bet Amount Input:', bg='#458B00', font=('arial', 12, 'normal')).place(x=360, y=600)
bet_amount_label = Label(root, text=f'You have placed a £{current_bet} bet', bg='#458B00', font=('arial', 12, 'normal'))
bet_amount_label.place(x=360, y=680)

result_label = Label(root, text='BlackJack Pays 3:2', bg='#458B00', font=('arial', 32, 'bold'))
result_label.place(x=220, y=50)
playertotal = Label(root, text='Player Total: 0', bg='#458B00', font=('arial', 12, 'normal'))
playertotal.place(x=170, y=100)
dealertotal = Label(root, text='Dealer Total: 0', bg='#458B00', font=('arial', 12, 'normal'))
dealertotal.place(x=500, y=100)

balance_label = Label(root, text=f'balance is :{balance}', bg='#458B00', font=('arial', 12, 'normal'))
balance_label.place(x=620, y=500)



root.mainloop()
