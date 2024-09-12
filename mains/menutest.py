import tkinter as tk
from tkinter import Label, Button, Entry, colorchooser
from PIL import Image, ImageTk
import random
import os

# Global variables
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
cards = [(value + " of " + suit) for suit in suits for value in values]
random.shuffle(cards)

# Create image references
image_directory = "/Users/ethan/Library/CloudStorage/GoogleDrive-ethanos999@gmail.com/Other computers/Main PC/() School Work  as at 30 04 21 E PC/A-Levels/Computer Science/()Campion School Work/CourseWork code/Blackjack py/PT1/()MainCode/()tkinter/mains/PNG-cards-1.3/"
card_back = "/Users/ethan/Library/CloudStorage/GoogleDrive-ethanos999@gmail.com/Other computers/Main PC/() School Work  as at 30 04 21 E PC/A-Levels/Computer Science/()Campion School Work/CourseWork code/Blackjack py/PT1/()MainCode/()tkinter/card back red.png"
image_refs = []
current_bet = 0
balance = 100
player_width = 220
dealer_width = 450
player_length = 200
dealer_length = 200

root = tk.Tk()
root.geometry('1200x800')
root.configure(background='#458B00')
root.title('BlackJack')

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

def update_bet_amount(amount):
    global current_bet
    if current_bet + amount > 100:
        bet_amount_label.config(text='You have exceeded the bet amount. Please try again.')
    else:
        current_bet += amount
        bet_amount_label.config(text=f'You have placed a £{current_bet} bet')

def hit():
    print('Hit')
    player_hit()
    update_totals()

def stand():
    print('Stand')
    dealer_turn()
    update_totals()

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

def card_value(card):
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

def carddisplay(card, x, y):
    global image_refs
    image_path = os.path.join(image_directory, card.replace(" ", "_") + ".png")
    try:
        image = Image.open(image_path)
        resized_image = image.resize((100, 150))
        tk_image = ImageTk.PhotoImage(resized_image)
        image_refs.append(tk_image)
        image_label = Label(root, image=tk_image)
        image_label.place(x=x, y=y)
    except FileNotFoundError:
        print(f"Error: File not found at {image_path}")

def display_initial_cards():
    global player_width, dealer_width

    for _ in range(2):
        card = deal_card()
        carddisplay(card, player_width, player_length)
        card_value_int = card_value(card)
        player_cards.append(card_value_int)
        player_total.set(player_total.get() + card_value_int)
        player_width += 25

    card = deal_card()
    carddisplay(card, dealer_width, dealer_length)
    card_value_int = card_value(card)
    dealer_cards.append(card_value_int)
    dealer_total.set(dealer_total.get() + card_value_int)
    dealer_width += 25

    try:
        card_back_image = Image.open(card_back)
        resized_card_back = card_back_image.resize((100, 150))
        tk_card_back = ImageTk.PhotoImage(resized_card_back)
        image_refs.append(tk_card_back)
        image_label = Label(root, image=tk_card_back)
        image_label.place(x=dealer_width, y=dealer_length)
    except FileNotFoundError:
        print(f"Error: File not found at {card_back}")

    playertotal.config(text=f"Player Total: {player_total.get()}")
    dealertotal.config(text=f"Dealer Total: {dealer_total.get()}")

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
    playertotal.config(text=f"Player Total: {player_total.get()}")
    dealertotal.config(text=f"Dealer Total: {dealer_total.get()}")

def end_game(result):
    result_label.config(text=result)
    update_totals()

def play_again():
    global player_width, dealer_width, player_cards, dealer_cards
    global player_total, dealer_total, current_bet

    player_width = 220
    dealer_width = 450
    player_cards = []
    dealer_cards = []
    player_total.set(0)
    dealer_total.set(0)
    current_bet = 0
    bet_amount_label.config(text=f'You have placed a £{current_bet} bet')

    for widget in root.winfo_children():
        if isinstance(widget, Label) and widget != bet_amount_label and widget != result_label and widget != playertotal and widget != dealertotal:
            widget.destroy()

    display_initial_cards()
    result_label.config(text='')

def start_game():

    for widget in root.winfo_children():
        widget.destroy()
    display_game_screen()

def show_settings():
    for widget in root.winfo_children():
        widget.destroy()
    display_settings_screen()

def quit_game():
    root.quit()

def set_background_color():
    color = colorchooser.askcolor()[1]
    if color:
        root.configure(background=color)

def display_start_screen():

    
    root.geometry('900x600')
    root.configure(background='#458B00')
    root.title('start')

    Button(root, text='Play Game', bg='#FFFAFA', font=('arial', 24, 'normal'), command=start_game).pack(pady=20)
    Button(root, text='Settings', bg='#FFFAFA', font=('arial', 24, 'normal'), command=show_settings).pack(pady=20)
    Button(root, text='Quit', bg='#FFFAFA', font=('arial', 24, 'normal'), command=quit_game).pack(pady=20)

def display_settings_screen():
    Label(root, text='Settings', bg='#458B00', font=('arial', 32, 'bold')).pack(pady=20)
    Button(root, text='Change Background Color', bg='#FFFAFA', font=('arial', 24, 'normal'), command=set_background_color).pack(pady=20)
    Button(root, text='Back to Main Menu', bg='#FFFAFA', font=('arial', 24, 'normal'), command=display_start_screen).pack(pady=20)

def display_game_screen():
    
    
    global bet, bet_amount_label, result_label, playertotal, dealertotal

    Button(root, text='Hit', bg='#FFFAFA', font=('arial', 12, 'normal'), command=hit).place(x=98, y=92)
    Button(root, text='Stand', bg='#FFFAFA', font=('arial', 12, 'normal'), command=stand).place(x=632, y=89)

    Button(root, text='Back to Main Menu', bg='#FFFAFA', font=('arial', 24, 'normal'), command=display_start_screen).pack(pady=20)


    Button(root, text='1', bg='#FFFAFA', font=('arial', 12, 'normal'), command=one).place(x=300, y=530)
    Button(root, text='5', bg='#FFFAFA', font=('arial', 12, 'normal'), command=five).place(x=335, y=530)
    Button(root, text='10', bg='#FFFAFA', font=('arial', 12, 'normal'), command=ten).place(x=370, y=530)
    Button(root, text='20', bg='#FFFAFA', font=('arial', 12, 'normal'), command=twenty).place(x=415, y=530)
    Button(root, text='50', bg='#FFFAFA', font=('arial', 12, 'normal'), command=fifty).place(x=462, y=530)
    Button(root, text='100', bg='#FFFAFA', font=('arial', 12, 'normal'), command=hundred).place(x=510, y=530)
    Button(root, text='max', bg='#FFFAFA', font=('arial', 12, 'normal'), command=max_bet).place(x=560, y=530)
    Button(root, text='min', bg='#FFFAFA', font=('arial', 12, 'normal'), command=min_bet).place(x=610, y=530)
    Button(root, text='Reset\nbet to 0', bg='#FFFAFA', font=('arial', 12, 'normal'), command=reset).place(x=700, y=530)

    Label(root, text='Betting Options:', bg='#458B00', font=('arial', 12, 'bold')).place(x=355, y=500)
    Button(root, text='Play Again', bg='#FFFAFA', font=('arial', 12, 'normal'), command=play_again).place(x=355, y=400)

    Button(root, text='Submit Bet Amount', bg='#FFFAFA', font=('arial', 12, 'normal'), command=getInputBoxValue).place(x=355, y=650)
    bet = Entry(root)
    bet.place(x=360, y=625)
    Label(root, text='Bet Amount Input:', bg='#458B00', font=('arial', 12, 'normal')).place(x=360, y=600)
    bet_amount_label = Label(root, text=f'You have placed a £{current_bet} bet', bg='#458B00', font=('arial', 12, 'normal'))
    bet_amount_label.place(x=360, y=680)

    result_label = Label(root, text='', bg='#458B00', font=('arial', 32, 'bold'))
    result_label.place(x=280, y=20)
    playertotal = Label(root, text='Player Total: 0', bg='#458B00', font=('arial', 12, 'normal'))
    playertotal.place(x=170, y=100)
    dealertotal = Label(root, text='Dealer Total: 0', bg='#458B00', font=('arial', 12, 'normal'))
    dealertotal.place(x=500, y=100)

    # Deal initial cards when the game starts
    display_initial_cards()

# Initialize the start screen
display_start_screen()

root.mainloop()