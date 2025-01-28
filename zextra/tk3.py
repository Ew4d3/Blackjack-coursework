import tkinter as tk
from tkinter import Label, Button, Entry
from PIL import Image, ImageTk
import random
import os

# Placeholder function
def siuuu():
    print("")

# Initialize variables
image_directory = "mains/PNG-cards-1.3/"
card_back = "mains/PNG-cards-1.3/card back red.png"
image_refs = []
current_bet = 0
balance = 100
player_x = 220
dealer_x = 450
player_y = 200
dealer_y = 200

# Create the main window
root = tk.Tk()
root.geometry('1080x720')
root.configure(background='#458B00')
root.title('BlackJack')

def update_bet(amount):
    """Updates the current bet and displays it."""
    global current_bet, balance
    if amount == "reset":
        current_bet = 0
        balance = 100  # Reset balance if needed
    else:
        if amount <= balance:  # Ensure the bet doesn't exceed the balance
            current_bet += amount
            balance -= amount
    bet_amount_label.config(text=f'You have placed a £{current_bet} bet')
    balance_label.config(text=f'Balance: £{balance}')

# Define functions for each bet amount
def one():
    update_bet(1)

def five():
    update_bet(5)

def ten():
    update_bet(10)

def twenty():
    update_bet(20)

def fifty():
    update_bet(50)

def hundred():
    update_bet(100)

def max_bet():
    update_bet(balance)

def reset_bet():
    update_bet("reset")

deck = [f"{rank}_of_{suit}" for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        for suit in ['hearts', 'diamonds', 'clubs', 'spades']]

def display_card(card, x, y):
    """Displays a card image at the given coordinates."""
    global image_refs

    # Get the card image path
    card_image_path = os.path.join(image_directory, f"{card}.png")
    try:
        # Load and resize the card image
        card_image = Image.open(card_image_path)
        resized_card_image = card_image.resize((100, 150))
        tk_card_image = ImageTk.PhotoImage(resized_card_image)

        # Store a reference to prevent garbage collection
        image_refs.append(tk_card_image)

        # Create a label to display the image
        card_label = Label(root, image=tk_card_image, bg='#458B00')
        card_label.place(x=x, y=y)
    except FileNotFoundError:
        print(f"Error: File not found for card {card}")

def hit():
    """Deals two random cards to the player and dealer."""
    global player_x, dealer_x

    # Select two random cards for the player
    player_cards = random.sample(deck, 2)
    for card in player_cards:
        display_card(card, player_x, player_y)
        player_x += 25  # Offset for the next card

    # Select two random cards for the dealer
    dealer_cards = random.sample(deck, 2)
    for card in dealer_cards:
        display_card(card, dealer_x, dealer_y)
        dealer_x += 25  # Offset for the next card

# UI buttons and labels
hit_button = Button(root, text='Hit', bg='#FFFAFA', font=('arial', 12, 'normal'), command=hit)
hit_button.place(x=98, y=92)
stand_button = Button(root, text='Stand', bg='#FFFAFA', font=('arial', 12, 'normal'), command=quit)
stand_button.place(x=632, y=89)

# Bet buttons
bets1 = Button(root, text='1', bg='#FFFAFA', font=('arial', 12, 'normal'), command=one)
bets1.place(x=270, y=530)
bets2 = Button(root, text='5', bg='#FFFAFA', font=('arial', 12, 'normal'), command=five)
bets2.place(x=335, y=530)
bets3 = Button(root, text='10', bg='#FFFAFA', font=('arial', 12, 'normal'), command=ten)
bets3.place(x=370, y=530)
bets4 = Button(root, text='20', bg='#FFFAFA', font=('arial', 12, 'normal'), command=twenty)
bets4.place(x=415, y=530)
bets5 = Button(root, text='50', bg='#FFFAFA', font=('arial', 12, 'normal'), command=fifty)
bets5.place(x=462, y=530)
bets6 = Button(root, text='100', bg='#FFFAFA', font=('arial', 12, 'normal'), command=hundred)
bets6.place(x=510, y=530)
bets7 = Button(root, text='max', bg='#FFFAFA', font=('arial', 12, 'normal'), command=max_bet)
bets7.place(x=560, y=530)
bets8 = Button(root, text='Reset\nbet to 0', bg='#FFFAFA', font=('arial', 12, 'normal'), command=reset_bet)
bets8.place(x=620, y=530)

play_again_button = Button(root, text='Play Again', bg='#FFFAFA', font=('arial', 12, 'normal'), command=reset_bet)
play_again_button.place(x=350, y=420)

quit_button = Button(root, text='Quit', bg='#FFFAFA', font=('arial', 12, 'normal'), command=quit)
quit_button.place(x=200, y=420)

bet_amount_label = Label(root, text=f'You have placed a £{current_bet} bet', bg='#458B00', font=('arial', 12, 'normal'))
bet_amount_label.place(x=360, y=680)

balance_label = Label(root, text=f'Balance: £{balance}', bg='#458B00', font=('arial', 12, 'normal'))
balance_label.place(x=620, y=500)

result_label = Label(root, text='BlackJack Pays 3:2', bg='#458B00', font=('arial', 32, 'bold'))
result_label.place(x=220, y=50)

playertotal = Label(root, text='Player Total: 0', bg='#458B00', font=('arial', 12, 'normal'))
playertotal.place(x=170, y=100)
dealertotal = Label(root, text='Dealer Total: 0', bg='#458B00', font=('arial', 12, 'normal'))
dealertotal.place(x=500, y=100)

root.mainloop()
