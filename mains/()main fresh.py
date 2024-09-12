import random
import time
from decimal import Decimal

suits = ['Hearts','Diamonds','Clubs','Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
cards = [(value + " of " + suit) for suit in suits for value in values]
random.shuffle(cards)

time.sleep(0.3)
print("\nbeat dealer = 1.5x bet (3:2)")
time.sleep(0.3)
print("blackjack = 2x bet")
time.sleep(0.3)
print("\ndealer stands on 17\n")
time.sleep(0.3)

balance=100

def addfunds():
    global balance
    print("max staring balance is 100")
    balance=int(input("how much you want to add to balance\n"))
    if balance>100:
        print('inputted balance over 100')
        addfunds()
    if balance>0:
        print("funds added to balance")
        time.sleep(0.3)
        betamount()
    if balance==0:
        print("cant add 0")
        time.sleep(0.3)
        addfunds()
    else:
        print("invalid response")
        addfunds()

def betamount():
    global bet,balance
    print("================================")
    print("            NEW GAME")
    print("================================\n")

    print('')
    print('balance is',balance,'\n')
    time.sleep(0.3)
    if balance>0:
        bet=int(input("enter bet amount:\n"))
        print("bet amount is",bet,'\n')
        if bet<=balance:
            if bet>=0 and bet<=100:
                cardgen()
            else:
                print("invalid bet amount, max 100")
                betamount()
        else:
            print("invalid bet amount, insufficient funds")
            time.sleep(0.3)
            betamount()
    else:
        print("cant bet , balance is 0 ")
        time.sleep(0.3)
        end()


def card_value(card):
    #gets card integer value 
    value = card.split()[0]
    if value in ['Jack', 'Queen', 'King']:
        return 10
    elif value == 'Ace':
        return 11
    else:
        return int(value)

def deal_card():
    global card , cards
    # Check if the deck is empty 
    if len(cards) == 0: 
        print("deck empty, reshuffling")
        #makes new shuffled deck if empty
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        cards = [(value + " of " + suit) for suit in suits for value in values]
        random.shuffle(cards)

    #gets fist card from list and pops it off stack
    card = cards.pop(0) 
    return card_value(card)
    
def end():
    #now does something , not a lot but still smt
    time.sleep(0.5)
    print("main screen:")
    time.sleep(0.15)
    print('1) play again')
    time.sleep(0.15)
    print('2) settings')
    time.sleep(0.15)
    print('3) add funds')
    time.sleep(0.15)
    choice=int(input('4) exit game\n'))
    if choice==1:
        playagain()
    if choice==2:
        print("not done yet")
        end()
    if choice==3:
        addfunds()
    if choice==4:
        print("ok  b y e ")
        exit()
    
    

def cardgen():
    #getting the initial 2 cards for player and dealer , doesnt display dealers first card
    global playertotal, dealer_total, playerace , dealerace , players_cards, dealercardval, balance, bet
    playertotal = 0
    playerace = False
    dealer_total = 0
    dealerace = False
    
    #dealers cards
    global dealer_cards
    dealer_cards = []
    dealercardval=[]
    for i in range(2):
        card_value_int = deal_card()
        dealer_cards.append(card)
        dealercardval.append(card_value_int)
        if card_value_int == 11:
            dealerace = True
        dealer_total += card_value_int

    print("Dealers card", dealer_cards[0])
    time.sleep(0.5)
    print("other dealer card hidden\n")
    time.sleep(0.2)
    print("Dealer's total:",dealercardval[0],'\n')
    time.sleep(0.2)
    
    #players cards
    for _ in range(2):
        players_cards=[]
        card_value_int = deal_card()
        print('your card:',card)
        time.sleep(0.5)
        players_cards.append(card)
        if card_value_int == 11:
            playerace = True
        playertotal += card_value_int
    
    print("\nPlayer's total", playertotal,'\n')
    time.sleep(0.2)


    #card checks for first 2 cards(bust ,blackjack ,push ),checks after hit in hitstand() function
    if playertotal > 21 and playerace:
        playertotal -= 10
        playerace = False
        print("Ace value is now 1",playertotal)
        time.sleep(0.2)
        print(playertotal)
        time.sleep(0.2)
        

    
    if playertotal > 21:
        print('Bust')
        time.sleep(0.5)
        balance=balance-bet
        print('you have lost',bet,'\n')
        print('Dealers cards were:',' , '.join(map(str, dealer_cards)))
        time.sleep(0.5)
        print('dealers total was' ,dealer_total)
        time.sleep(0.5)
        end()
    if playertotal==21 :
        print("blackjack")
        time.sleep(0.5)
        balance=balance+(bet*2)
        print('you have won',bet*2)
        print("\n")
        time.sleep(0.5)
        print('Dealers cards were:',' , '.join(map(str, dealer_cards)))
        time.sleep(0.3)
        print('dealers total was' ,dealer_total)
        time.sleep(0.3)
        playagain()
        
    else:
        hitstand()

def hitstand():
    #gets cards after hit ,checks and outputs ,goes to dealers turn if stand
    global playertotal, playerace , dealer_cards , balance , bet 
    while True:
        action = input('Hit or Stand\n').strip().lower()
        time.sleep(0.5)
        if action == 'h':
            card_value_int = deal_card()
            print("your card is...")
            time.sleep(2)
            print(card)
            #card checking after hitting for bust ,blackjack ,push etc
            if card_value_int == 11:
                if playertotal + 11 > 21:
                    playertotal += 1
                else:
                    playertotal += 11
                    playerace = True
            else:
                playertotal += card_value_int
            print("Player's total:", playertotal,'\n')
            time.sleep(0.3)
            if playertotal > 21:
                #if player busts and have ace ,ace converted from 11 to 1 to reduce score to continue 
                if playerace:
                    playertotal -= 10
                    playerace = False
                    print("Ace value is now 1")
                    time.sleep(0.5)
                    print("new player total =",playertotal)
                    time.sleep(0.5)
                    continue
                else:
                    #once bust ,displays dealers cards and cards value total 
                    print('Bust\n')
                    balance=balance-bet
                    print('you have lost',bet,'\n')
                    time.sleep(0.5)
                    print('Dealers cards were:',' , '.join(map(str, dealer_cards)))
                    print('')
                    time.sleep(0.5)
                    print('dealers total was' ,dealer_total,'\n')
                    time.sleep(0.5)
                    playagain()
            if playertotal==21 :
                print("blackjack")
                time.sleep(0.5)
                balance=balance+(bet*2)
                print('you have won',bet*2)
                time.sleep(0.5)
                playagain()
                
        elif action == 's':
            #dealers turn if stand
            dealer_turn()
            break
        else:
            print('Invalid input H or S')

def dealer_turn():
    #gets dealers cards after player stands , then checks for push ,bust ,blackjack ,dealer win etc
    global dealertotal, dealerace , dealer_total,balance, bet
    #outputs the dealers crad that was hidden at start, and total w both cards 
    print('dealers hidden card was',dealer_cards[1])
    time.sleep(0.3)
    print('\ndealer total=',dealer_total,'\n')
    time.sleep(0.3)
    dealertotal = dealer_total
    dealerace = False
    #dealer stands on 17 . must hit on <=16
    while dealertotal < 17:
        card_value_int = deal_card()
        print("dealer hits.....\n")
        time.sleep(2)
        print(card,'\n')
        if card_value_int == 11:
            dealerace = True
        dealertotal += card_value_int
        print("Dealer's total:", dealertotal,'\n')
        time.sleep(0.3)
        if dealertotal > 21:
            #if dealer busts + has ace , ace = 1
            if dealerace:
                dealertotal -= 10
                dealerace = False
                print("Ace value is now 1")
                time.sleep(0.5)
                print('New dealer total=',dealertotal)
                time.sleep(0.5)
            else:
                print('Dealer Busts You win')
                time.sleep(0.5)
                balance=balance+(bet*1.5)
                print('you have won',bet*1.5)
                time.sleep(0.5)
                playagain()
                return
    #checking for win ,loss ,blackjack ,push etc  
    if dealertotal > playertotal:
        print('Dealer Wins')
        time.sleep(0.5)
        print('you have lost',bet)
        balance=balance-bet
        time.sleep(0.5)
        playagain()
    elif dealertotal == playertotal:
        print('Push')
        time.sleep(0.5)
    if dealertotal<22 and dealertotal<playertotal:
        print('You Win')
        balance=balance+(bet*1.5)
        print('you have won',bet)
        time.sleep(0.5)
    if dealertotal==21 and playertotal==21:
        print('both blackjack, push')
        time.sleep(0.5)
    else: 
        playagain()

def playagain():
    # .strip() removes spaces before+after input , easier for erroe checking
    print('')
    print('balance is',balance,'\n')
    option = input("Wanna play again?\n").strip().lower()
    time.sleep(0.2)
    while option not in ['yes', 'y', 'no', 'n']:
        print("Invalid input. Please enter 'yes' or 'no'.")
        option = input("Wanna play again?\n").strip().lower()
    if option in ['yes', 'y']:
        betamount()
    else:
        print("alr")
        end()



#suiiiiii

betamount()
