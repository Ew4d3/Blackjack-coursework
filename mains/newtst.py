##Hit and Stand Buttons: These buttons will only work and appear during the player's turn.
#Play Again Button: The button will say "Quit" until the round has ended and the result has been displayed, then it will change back to "Play Again."
#Blackjack on Initial Cards: If the player gets a Blackjack (21) on the initial cards, the game will immediately display the result as "Blackjack!"
#Update Player and Dealer Totals: The totals are updated only after the card has been flipped and revealed.


import tkinter as tk
from tkinter import Label, Button, Entry 
from PIL import Image, ImageTk
import random
import os

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
cards = [(value + " of " + suit) for suit in suits for value in values]
random.shuffle(cards)

image_directory = "/Users/ethan/Library/CloudStorage/GoogleDrive-ethanos999@gmail.com/Other computers/Main PC/() School Work  as at 30 04 21 E PC/A-Levels/Computer Science/()Campion School Work/CourseWork code/Blackjack py/PT1/()MainCode/()tkinter/mains/PNG-cards-1.3/"
card_back = "/Users/ethan/Library/CloudStorage/GoogleDrive-ethanos999@gmail.com/Other computers/Main PC/() School Work  as at 30 04 21 E PC/A-Levels/Computer Science/()Campion School Work/CourseWork code/Blackjack py/PT1/()MainCode/()tkinter/mains/PNG-cards-1.3/card back red.png"
image_refs = []
bkg="/Users/ethan/Library/CloudStorage/GoogleDrive-ethanos999@gmail.com/Other computers/Main PC/() School Work  as at 30 04 21 E PC/A-Levels/Computer Science/()Campion School Work/CourseWork code/Blackjack py/PT1/()MainCode/()tkinter/mains/3217577-middle.png"
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

# Function to get the user input from the text input box and display it
def getInputBoxValue():
    global current_bet
    userInput = bet.get()
    try:
        input_value = int(userInput)
        if current_bet + input_value > 100:
            bet_amount_label.config(text='You have exceeded the bet amount. Please try again.')
        else:
            current_bet += input_value
            bet_amount_label.config(text=f'You have placed a £{current_bet} bet')
    except ValueError:
        bet_amount_label.config(text='Invalid input. Please enter a number.')

# Function to update the bet amount label
def update_bet_amount(amount):
    global current_bet
    if current_bet + amount > 100:
        bet_amount_label.config(text='You have exceeded the bet amount. Please try again.')
    else:
        current_bet += amount
        bet_amount_label.config(text=f'You have placed a £{current_bet} bet')

# Functions called when buttons are clicked
def hit():
    print('Hit')
    player_hit()

def stand():
    print('Stand')
    flip_face_down_card()
    dealer_turn()

def bet_amount(amount):
    update_bet_amount(amount)

def one():
    bet_amount(1)

def five():
    bet_amount(5)

def ten():
    bet_amount(10)

def twenty():
    bet_amount(20)

def fifty():
    bet_amount(50)

def hundred():
    bet_amount(100)

def max_bet():
    bet_amount(100 - current_bet)

def min_bet():
    global current_bet
    current_bet = 1
    bet_amount_label.config(text=f'You have placed a £{current_bet} bet')

def reset():
    global current_bet
    current_bet = 0
    bet_amount_label.config(text=f'Bet amount reset to 0')

def card_value(card):#see if is a 10 value or 11 value , or regular card.
    value = card.split()[0]
    if value in ['Jack', 'Queen', 'King']:
        return 10
    elif value == 'Ace':
        return 11
    else:
        return int(value)

def deal_card():
    global cards
    if len(cards) == 0:
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        cards = [(value + " of " + suit) for suit in suits for value in values]
        random.shuffle(cards)
    card = cards.pop(0)
    return card

def slide_card(image_label, final_x, final_y, flip_function=lambda: None, step=10, delay=10): # animations 
    current_x, current_y = image_label.winfo_x(), image_label.winfo_y()
    moved = False

    # Move in the x direction
    if current_x < final_x:
        new_x = min(current_x + step, final_x)
        image_label.place(x=new_x, y=current_y)
        moved = True
    elif current_x > final_x:
        new_x = max(current_x - step, final_x)
        image_label.place(x=new_x, y=current_y)
        moved = True
    else:
        new_x = final_x

    # Move in the y direction
    if current_y < final_y:
        new_y = min(current_y + step, final_y)
        image_label.place(x=new_x, y=new_y)
        moved = True
    elif current_y > final_y:
        new_y = max(current_y - step, final_y)
        image_label.place(x=new_x, y=new_y)
        moved = True
    else:
        new_y = final_y

    if moved:
        root.after(delay, slide_card, image_label, final_x, final_y, flip_function, step, delay)
    else:
        flip_function()

def flip_card(image_label, card_image):
    image_label.config(image=card_image)
    image_label.image = card_image

    update_totals()

def carddisplay(card, x, y):
    global image_refs
    card_image_path = os.path.join(image_directory, card.replace(" ", "_") + ".png")
    try:
        card_back_image = Image.open(card_back)
        resized_card_back = card_back_image.resize((100, 150))
        tk_card_back = ImageTk.PhotoImage(resized_card_back)
        image_refs.append(tk_card_back)
        image_label = Label(root, image=tk_card_back)
        image_label.place(x=0, y=y)

        card_image = Image.open(card_image_path)
        resized_card_image = card_image.resize((100, 150))
        tk_card_image = ImageTk.PhotoImage(resized_card_image)
        image_refs.append(tk_card_image)

        slide_card(image_label, x, y, lambda: flip_card(image_label, tk_card_image))
    except FileNotFoundError:
        print(f"Error: File not found at {card_image_path}")


def display_initial_cards():
    global player_width, dealer_width, face_down_label, face_down_card

    # Deal and display two cards for the player
    for _ in range(2):
        card = deal_card()
        carddisplay(card, player_width, player_length)
        card_value_int = card_value(card)
        player_cards.append(card_value_int)
        player_total.set(player_total.get() + card_value_int)
        player_width += 25
        root.after(800, lambda: playertotal.config(text=f"Player Total: {player_total.get()}"))
        check_player_status()
        check_initial_blackjack()


    # Deal and display one face-up card for the dealer
    card = deal_card()
    carddisplay(card, dealer_width, dealer_length)
    card_value_int = card_value(card)
    dealer_cards.append(card_value_int)
    dealer_total.set(dealer_total.get() + card_value_int)
    dealer_width += 25
    root.after(800, lambda: dealertotal.config(text=f"Dealer Total: {dealer_total.get()}"))

    # Display one face-down card for the dealer
    face_down_card = deal_card()  # Save the face-down card for later flipping
    try:
        card_back_image = Image.open(card_back)
        resized_card_back = card_back_image.resize((100, 150))
        tk_card_back = ImageTk.PhotoImage(resized_card_back)
        image_refs.append(tk_card_back)
        face_down_label = Label(root, image=tk_card_back)
        face_down_label.place(x=0, y=dealer_length)  # Start from outside and slide in
        slide_card(face_down_label, dealer_width, dealer_length)
    except FileNotFoundError:
        print(f"Error: File not found at {card_back}")

    check_initial_blackjack()

def check_initial_blackjack():
    if player_total.get() == 21:
        end_game("Blackjack! Player wins.")

def flip_face_down_card(): #face down card would just sit therr at the start then would slide in but it was techincally already there
    global face_down_card , dealer_width , card_image_path , card_image_path
    card_image_path = os.path.join(image_directory, face_down_card.replace(" ", "_") + ".png")
    try:
        card_image = Image.open(card_image_path)
        resized_card_image = card_image.resize((100, 150))
        tk_card_image = ImageTk.PhotoImage(resized_card_image)
        image_refs.append(tk_card_image)
        flip_card(face_down_label, tk_card_image)
        card_value_int = card_value(face_down_card)
        dealer_cards.append(card_value_int)
        dealer_total.set(dealer_total.get() + card_value_int)
        dealer_width += 25

    except FileNotFoundError:
        print(f"Error: File not found at {card_image_path}")

def player_hit():
    global player_width
    card = deal_card()
    carddisplay(card, player_width, player_length)
    card_value_int = card_value(card)
    player_cards.append(card_value_int)
    player_total.set(player_total.get() + card_value_int)
    player_width += 25
    check_player_status()

def check_player_status():
    if player_total.get() > 21:
        if 11 in player_cards:
            player_total.set(player_total.get() - 10)
            player_cards[player_cards.index(11)] = 1
        else:
            end_game("Bust! Dealer wins.")
    elif player_total.get() == 21:
        end_game("Blackjack! Player wins.")

def dealer_turn():
    global dealer_width
    while dealer_total.get() < 17:
        card = deal_card()
        card_value_int = card_value(card)
        dealer_cards.append(card_value_int)
        dealer_total.set(dealer_total.get() + card_value_int)
        carddisplay(card, dealer_width, dealer_length)
        dealer_width += 25
    check_winner()

def check_winner():
    if dealer_total.get() > 21:
        end_game("Dealer busts! Player wins.")
    elif player_total.get() > dealer_total.get():
        end_game("Player wins!")
    elif dealer_total.get() == player_total.get():
        end_game("Push!")
    else:
        end_game("Dealer wins!")

def update_totals():
    root.after(500, lambda: playertotal.config(text=f"Player Total: {player_total.get()}"))
    root.after(500, lambda: dealertotal.config(text=f"Dealer Total: {dealer_total.get()}"))

def end_game(result):
    result_label.config(text=result)
    hit_button.config(state='disabled')
    stand_button.config(state='disabled')
    play_again_button.config(text="Play Again")
    update_totals()

def play_again():#game would never end , cards kept on queueing uo against other games 
    global player_width, dealer_width, player_cards, dealer_cards
    global player_total, dealer_total, current_bet

    root.after(100, lambda: playertotal.config(text=f"Player Total: 0"))
    root.after(100, lambda: dealertotal.config(text=f"Dealer Total: 0"))


    # Reset positions
    player_width = 220
    dealer_width = 450

    # Reset hands
    player_cards = []
    dealer_cards = []

    # Reset totals
    player_total.set(0)
    dealer_total.set(0)

    # Reset bet
    current_bet = 0
    bet_amount_label.config(text=f'You have placed a £{current_bet} bet')

    # Clear all card images     before cards would overlay other cards so game would crash etc 
    for widget in root.winfo_children():
        if isinstance(widget, Label) and widget != bet_amount_label and widget != result_label and widget != playertotal and widget != dealertotal:
            widget.destroy()

    # Deal new initial cards
    display_initial_cards()


    # Enable hit and stand buttons
    hit_button.config(state='normal')
    stand_button.config(state='normal')
    play_again_button.config(text="Quit")

# Main game logic variables
player_cards = []
dealer_cards = []
player_total = tk.IntVar(value=0)
dealer_total = tk.IntVar(value=0)

# UI Elements
hit_button = Button(root, text='Hit', bg='#FFFAFA', font=('arial', 12, 'normal'), command=hit)
hit_button.place(x=98, y=92)
stand_button = Button(root, text='Stand', bg='#FFFAFA', font=('arial', 12, 'normal'), command=stand)
stand_button.place(x=632, y=89)

Button(root, text='1', bg='#FFFAFA', font=('arial', 12, 'normal'), command=one).place(x=300, y=530)
Button(root, text='5', bg='#FFFAFA', font=('arial', 12, 'normal'), command=five).place(x=335, y=530)
Button(root, text='10', bg='#FFFAFA', font=('arial', 12, 'normal'), command=ten).place(x=370, y=530)
Button(root, text='20', bg='#FFFAFA', font=('arial', 12, 'normal'), command=twenty).place(x=415, y=530)
Button(root, text='50', bg='#FFFAFA', font=('arial', 12, 'normal'), command=fifty).place(x=462, y=530)
Button(root, text='100', bg='#FFFAFA', font=('arial', 12, 'normal'), command=hundred).place(x=510, y=530)
Button(root, text='max', bg='#FFFAFA', font=('arial', 12, 'normal'), command=max_bet).place(x=560, y=530)
Button(root, text='min', bg='#FFFAFA', font=('arial', 12, 'normal'), command=min_bet).place(x=610, y=530)
Button(root, text='Reset\nbet to 0', bg='#FFFAFA', font=('arial', 12, 'normal'), command=reset).place(x=700, y=530)

play_again_button = Button(root, text='Quit', bg='#FFFAFA', font=('arial', 12, 'normal'), command=play_again)
play_again_button.place(x=350, y=420)

Button(root, text='Submit Bet Amount', bg='#FFFAFA', font=('arial', 12, 'normal'), command=getInputBoxValue).place(x=355, y=650)
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

# Deal initial cards when the game starts
display_initial_cards()

root.mainloop()
