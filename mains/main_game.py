#

import tkinter as tk
from tkinter import Label, Button, Entry 
from PIL import Image, ImageTk
import random
import os

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
cards = [(value + " of " + suit) for suit in suits for value in values]



#shuffle the cards
for i in range(len(cards)):
    j=random.randint(0, len(cards)-1)
    temp=cards[i]
    cards[i]=cards[j]
    cards[j]=temp
    #print(cards) # test to make sure cards got shuffled    


global balance
image_directory = "mains/PNG-cards-1.3/"
card_back = "mains/PNG-cards-1.3/card back red.png"
image_refs = []
bkg="r/mains/3217577-middle.png"
current_bet = 0 
balance = 100
player_width = 220
dealer_width = 450
length = 200
winnings=0
root = tk.Tk()
root.geometry('1080x720')
root.configure(background='#458B00')
root.title('BlackJack')




#get the user input from the text input box and display it
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
            update_balance(balance)
    except ValueError:
        bet_amount_label.config(text='Invalid input. Please enter a number.')

#update the bet amount label
def update_bet_amount(amount):
    global current_bet, balance
    if current_bet + amount > 100:
        bet_amount_label.config(text='You have exceeded the bet amount. Please try again.')
       
    else:
        current_bet += amount
        bet_amount_label.config(text=f'You have placed a £{current_bet} bet')
        
 


def update_balance(balance): #updates the balance when betting so label is updated accordingly
    global current_bet
    balance=balance-current_bet
    balance_label.config(text=f'balance is {balance}')





#called when buttons are clicked
def hit():
    print('Hit')
    player_hit()

def stand():
    print('Stand')
    flip_face_down_card()
    dealer_turn()

def bet_amount(amount):
    update_bet_amount(amount)
    update_balance(balance)
   
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

def min_bet(): #minimum bet eg 1
    global current_bet , balance
    current_bet = 1
    bet_amount_label.config(text=f'You have placed a £{current_bet} bet')
    update_balance(balance)

def reset(): # resets bet to 0
    global current_bet, balance
    current_bet = 0
    bet_amount_label.config(text=f'Bet amount reset to 0')
    update_balance(balance)



def card_value(card):#see if is a 10 value or 11 value , or regular card.
    value = card.split()[0]
    if value in ['Jack', 'Queen', 'King']:
        return 10
    elif value == 'Ace':
        return 11
    else:
        return int(value)

def deal_card(): #deals cards
    global cards
    if len(cards) == 0:
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        cards = [(value + " of " + suit) for suit in suits for value in values]
        random.shuffle(cards)
        print("reshuffling new deck")
    card = cards.pop(0)
    return card

def slide_card(image_label, final_x, final_y, flip_function=lambda: None, step=10, delay=10): # animations and stuff uses currenr psoitions, adds buffer for next card to overlapp
    current_x, current_y = image_label.winfo_x(), image_label.winfo_y()
    moved = False

    #move in the x direction
    if current_x < final_x:
        new_x = min(current_x + step, final_x) #current pos+overlap amount 
        image_label.place(x=new_x, y=current_y)
        moved = True
    elif current_x > final_x:
        new_x = max(current_x - step, final_x)
        image_label.place(x=new_x, y=current_y)
        moved = True
    else:
        new_x = final_x

    #move in the y direction
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


def flip_card(image_label, card_image): #chnages card back image for dealer to actual stored card image so player can see the card
    image_label.config(image=card_image)
    image_label.image = card_image

    update_totals()


def carddisplay(card, x, y): #complicated stuff for finding path for cards and opening them, resize , placing them etc
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

        slide_card(image_label, x, y, lambda: flip_card(image_label, tk_card_image)) #lambda delays flip_card call- once cards slide, then flip
    except FileNotFoundError:
        print(f"Error: File not found at {card_image_path}")


def display_initial_cards(): # dsiplays rhe 2 player cards and 2 dealers, one being flipped/hidden
    global player_width, dealer_width, face_down_label, face_down_card

    #deal and display two cards for player
    for _ in range(2):
        card = deal_card()
        carddisplay(card, player_width, length)
        card_value_int = card_value(card)
        player_cards.append(card_value_int)
        player_total.set(player_total.get() + card_value_int)
        player_width += 25
        root.after(800, lambda: playertotal.config(text=f"Player Total: {player_total.get()}"))
        check_player_status()
        check_initial_blackjack()


    #deal and display one face up card for dealer
    card = deal_card()
    carddisplay(card, dealer_width, length)
    card_value_int = card_value(card)
    dealer_cards.append(card_value_int)
    dealer_total.set(dealer_total.get() + card_value_int)
    dealer_width += 25
    root.after(800, lambda: dealertotal.config(text=f"Dealer Total: {dealer_total.get()}"))


    #display one fac down card for dealer
    face_down_card = deal_card()  #save the face down card for flippin later 
    try:
        card_back_image = Image.open(card_back)
        resized_card_back = card_back_image.resize((100, 150))
        tk_card_back = ImageTk.PhotoImage(resized_card_back)
        image_refs.append(tk_card_back)
        face_down_label = Label(root, image=tk_card_back)
        face_down_label.place(x=0, y=length)  #start from left and slide in
        slide_card(face_down_label, dealer_width, length)
    except FileNotFoundError:
        print(f"Error: File not found at {card_back}")

    check_initial_blackjack()


def check_initial_blackjack():#checks to see if the forst 2 cards are blackjack eg ace + king=21
    global balance,winnings
    if player_total.get() == 21:
        end_game("Blackjack! Player wins.")
        winnings=current_bet*2
        balance=balance+winnings
        winnings_label.config(text=f'winnings is {winnings}')

        update_balance(balance)


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


def player_hit(): #player hit, gets another card and updates position for card to correctly ovberlap 
    global player_width
    card = deal_card()
    carddisplay(card, player_width, length)
    card_value_int = card_value(card)
    player_cards.append(card_value_int)
    player_total.set(player_total.get() + card_value_int)
    player_width += 25
    check_player_status()


def check_player_status(): #checks if the player has won etc and gets their total
    global balance,winnings
    if player_total.get() > 21:
        if 11 in player_cards:
            player_total.set(player_total.get() - 10)
            player_cards[player_cards.index(11)] = 1
        else:
            flip_face_down_card()
            end_game("Bust! Dealer wins.")
    elif player_total.get() == 21:
        end_game("Blackjack! Player wins.")
        winnings=current_bet*2
        balance=balance+winnings
        winnings_label.config(text=f'winnings is {winnings}')
        update_balance(balance)


def dealer_turn(): #dealers turn when player stands , gets card and updates position for obverlap
    global dealer_width
    while dealer_total.get() < 17: #dealer autohits when less than 17
        card = deal_card()
        card_value_int = card_value(card)
        dealer_cards.append(card_value_int)
        dealer_total.set(dealer_total.get() + card_value_int)
        carddisplay(card, dealer_width, length)
        dealer_width += 25
    check_winner()


def check_winner(): # checks to see who has won and update balance accordingly based on bet amount.
    global balance,winnings
    if dealer_total.get() > 21:
        end_game("Dealer busts! Player wins.")
        winnings=current_bet*1.5
        balance=balance+winnings
        winnings_label.config(text=f'winnings is {winnings}')
        update_balance(balance)
    elif player_total.get() > dealer_total.get():
        end_game("Player wins!")
        winnings=current_bet*1.5
        balance=balance+winnings
        winnings_label.config(text=f'winnings is {winnings}')
        update_balance(balance)
    elif dealer_total.get() == player_total.get():
        end_game("Push!")
        winnings=0
        balance=balance+current_bet
        winnings_label.config(text=f'winnings is {winnings}')
        update_balance(balance)
    else:
        end_game("Dealer wins!")


def update_totals(): # updates the total lables
    root.after(500, lambda: playertotal.config(text=f"Player Total: {player_total.get()}"))
    root.after(500, lambda: dealertotal.config(text=f"Dealer Total: {dealer_total.get()}"))


def end_game(result): #disables buttons so no undesired sideeffects and displays at top th result
    result_label.config(text=result)
    hit_btn.config(state='disabled')
    stand_btn.config(state='disabled')
    play_again_btn.config(text="Play Again")
    bet_btn1.config(state='disabled')
    bet_btn5.config(state='disabled')
    bet_btn10.config(state='disabled')
    bet_btn20.config(state='disabled')
    bet_btn50.config(state='disabled')
    bet_btn100.config(state='disabled')
    bet_btn_max.config(state='disabled')
    bet_btn_min.config(state='disabled')
    bet_btn_reset.config(state='disabled')
    bet.config(state='disabled')
    betbox.config(state='disabled')
    play_again_btn.config(state='normal')
    
    update_totals()

def play_again():#game would never end , cards kept on queueing uo against other games 
    global player_width, dealer_width, player_cards, dealer_cards
    global player_total, dealer_total, current_bet

    root.after(100, lambda: playertotal.config(text=f"Player Total: 0")) #lambda allows root.after to work propely , oterwise need sperate fucntion to call after 100ms
    root.after(100, lambda: dealertotal.config(text=f"Dealer Total: 0"))
    root.after(100, lambda: result_label.config(text=f"BlackJack Pays 3:2"))
    
    #reset positions where card should go
    player_width = 220
    dealer_width = 450

    #reset cards
    player_cards = []
    dealer_cards = []

    #reset totals
    player_total.set(0)
    dealer_total.set(0)

    #reset bet
    current_bet = 0
    bet_amount_label.config(text=f'You have placed a £{current_bet} bet')

    #clear all card images     before cards would overlay other cards so game would crash etc 
    for widget in root.winfo_children():
        if isinstance(widget, Label) and widget != bet_amount_label and widget != result_label and widget != playertotal and widget != dealertotal and widget != balance_label and widget !=winnings_label :
            widget.destroy()#destoys all labels that arent excluded above

    # deal new initial cards
    display_initial_cards()




    #enable hit and stand buttons
    hit_btn.config(state='normal')
    stand_btn.config(state='normal')
    play_again_btn.config(text="play again")
    quit_btn.config(text='quit')
    bet_btn1.config(state='normal')
    bet_btn5.config(state='normal')
    bet_btn10.config(state='normal')
    bet_btn20.config(state='normal')
    bet_btn50.config(state='normal')
    bet_btn100.config(state='normal')
    bet_btn_max.config(state='normal')
    bet_btn_min.config(state='normal')
    bet_btn_reset.config(state='normal')
    bet.config(state='normal')
    betbox.config(state='normal')
    play_again_btn.config(state='disabled')
  




#main game logic variables
player_cards = []
dealer_cards = []
player_total = tk.IntVar(value=0)
dealer_total = tk.IntVar(value=0)


#ui stuff buttons labels etc
hit_btn = Button(root, text='Hit', bg='#FFFAFA', font=('arial', 12, 'normal'), command=hit)
hit_btn.place(x=98, y=92)
stand_btn = Button(root, text='Stand', bg='#FFFAFA', font=('arial', 12, 'normal'), command=stand)
stand_btn.place(x=632, y=89)


#bet button labels and corresponding functions
bet_btn1=Button(root, text='1', bg='#FFFAFA', font=('arial', 12, 'normal'), command=one)
bet_btn1.place(x=270, y=530)
bet_btn5=Button(root, text='5', bg='#FFFAFA', font=('arial', 12, 'normal'), command=five)
bet_btn5.place(x=335, y=530)
bet_btn10=Button(root, text='10', bg='#FFFAFA', font=('arial', 12, 'normal'), command=ten)
bet_btn10.place(x=370, y=530)
bet_btn20=Button(root, text='20', bg='#FFFAFA', font=('arial', 12, 'normal'), command=twenty)
bet_btn20.place(x=415, y=530)
bet_btn50=Button(root, text='50', bg='#FFFAFA', font=('arial', 12, 'normal'), command=fifty)
bet_btn50.place(x=462, y=530)
bet_btn100=Button(root, text='100', bg='#FFFAFA', font=('arial', 12, 'normal'), command=hundred)
bet_btn100.place(x=510, y=530)
bet_btn_max=Button(root, text='max', bg='#FFFAFA', font=('arial', 12, 'normal'), command=max_bet)
bet_btn_max.place(x=560, y=530)
bet_btn_min=Button(root, text='min', bg='#FFFAFA', font=('arial', 12, 'normal'), command=min_bet)
bet_btn_min.place(x=610, y=530)
bet_btn_reset=Button(root, text='Reset\nbet to 0', bg='#FFFAFA', font=('arial', 12, 'normal'), command=reset)
bet_btn_reset.place(x=700, y=525)


#play again + quit button
play_again_btn = Button(root, text='play again', bg='#FFFAFA', font=('arial', 12, 'normal'), command=play_again)
play_again_btn.place(x=350, y=420)
quit_btn = Button(root, text='quit', bg='#FFFAFA', font=('arial', 12, 'normal'), command=quit)
quit_btn.place(x=200, y=420)


#input box for bet input that you can type into and corresponing fuct
betbox=Button(root, text='Submit Bet Amount', bg='#FFFAFA', font=('arial', 12, 'normal'), command=getInputBoxValue)
betbox.place(x=355, y=650)
bet = Entry(root)
bet.place(x=360, y=625)
Label(root, text='Bet Amount Input:', bg='#458B00', font=('arial', 12, 'normal')).place(x=360, y=600)
bet_amount_label = Label(root, text=f'You have placed a £{current_bet} bet', bg='#458B00', font=('arial', 12, 'normal'))
bet_amount_label.place(x=360, y=680)


#result labels shows who won the game, as well as the player totals taht show the hand values for player+dealer
result_label = Label(root, text='BlackJack Pays 3:2', bg='#458B00', font=('arial', 32, 'bold'))
result_label.place(x=220, y=30)
playertotal = Label(root, text='Player Total: 0', bg='#458B00', font=('arial', 12, 'normal'))
playertotal.place(x=170, y=100)
dealertotal = Label(root, text='Dealer Total: 0', bg='#458B00', font=('arial', 12, 'normal'))
dealertotal.place(x=500, y=100)

winnings_label= Label(root, text=f'Winnings:{winnings}', bg='#458B00', font=('arial', 12, 'normal'))
winnings_label.place(x=650, y=500)

#displays balance value
balance_label = Label(root, text=f'balance is :{balance}', bg='#458B00', font=('arial', 12, 'normal'))
balance_label.place(x=650,y=575)


#disables play again as defult until roubnd ends and you can play again
play_again_btn.config(state='disabled')





#deal initial cards when game starts
display_initial_cards()

#roooooooot
root.mainloop()
