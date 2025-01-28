import tkinter as tk
from tkinter import Label, Button, Entry
from PIL import Image, ImageTk
import random
import os

# Constants
image_directory = "mains/PNG-cards-1.3/"
card_back = "mains/PNG-cards-1.3/card back red.png"
image_refs = []  # To prevent garbage collection
bkg = "r/mains/3217577-middle.png"
current_bet = 0
balance = 100
player_x = 220
dealer_x = 450
player_y = 200
dealer_y = 200

# Initialize Deck
deck = [f"{rank}_of_{suit}" for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        for suit in ['hearts', 'diamonds', 'clubs', 'spades']]

# Tkinter setup
root = tk.Tk()
root.geometry('1080x720')
root.configure(background='#458B00')
root.title('BlackJack')


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


# Buttons
hit_button = Button(root, text='Hit', bg='#FFFAFA', font=('arial', 12, 'normal'), command=hit)
hit_button.place(x=98, y=92)

stand_button = Button(root, text='Stand', bg='#FFFAFA', font=('arial', 12, 'normal'), command=lambda: print("Stand pressed"))
stand_button.place(x=632, y=89)

# Betting Buttons
betbox = Button(root, text='Submit Bet Amount', bg='#FFFAFA', font=('arial', 12, 'normal'), command=lambda: print("Bet submitted"))
betbox.place(x=355, y=650)
bet = Entry(root)
bet.place(x=360, y=625)

# Labels
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

# Mainloop
root.mainloop()
