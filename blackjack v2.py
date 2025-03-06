import random

# Define card deck
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
         '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

def place_bet():
    while True:
        try:
            bet = input("Place your bet in USD (Default is $10): ")
            return int(bet) if bet.isdigit() and int(bet) > 0 else 10
        except ValueError:
            print("Invalid input. Please enter a number.")

def winner(balance, bet):
    round_winnings = bet * 1.5 
    balance += round_winnings
    print(f"You won! New balance: ${balance}")
    return balance

def loser(balance, bet):
    balance -= bet
    print(f"You lost! New balance: ${balance}")
    return balance

def create_shoe(decks = 8):
    """Create a shoe containing multiple decks of 52 cards."""
    shoe = [{'rank': rank, 'suit': suit, 'value': value} 
            for suit in suits for rank, value in ranks.items() for _ in range(decks)]
    shuffled_shoe = []
    while shoe:
        random_index = random.randint(0, len(shoe) - 1)
        picked_card = shoe.pop(random_index)
        shuffled_shoe.append(picked_card)
    return shuffled_shoe

def deal_card(shoe):
    if len(shoe) < 20:
        print("Reshuffling the shoe...")
        shoe[:] = create_shoe()
    return shoe.pop()

def calculate_hand_value(hand):
    value = sum(card['value'] for card in hand)
    ace_count = sum(1 for card in hand if card['rank'] == 'A')

    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1

    return value

def dealer_play(shoe):
    hand = [deal_card(shoe), deal_card(shoe)]
    while calculate_hand_value(hand) < 17:
        hand.append(deal_card(shoe))
    return hand

def player_play(shoe):
    hand = [deal_card(shoe), deal_card(shoe)]

    while True:
        hand_value = calculate_hand_value(hand)
        print("\nYour Hand:")
        for card in hand:
            print(f"{card['rank']} of {card['suit']}")
        print(f"Total Value: {hand_value}")

        if hand_value > 21:
            print("You Bust!")
            return hand

        move = input("Would you like to (H)it or (S)tand? ").strip().lower()
        if move == 'h':
            hand.append(deal_card(shoe))
        elif move == 's':
            break
        else:
            print("Invalid input. Please enter 'H' to hit or 'S' to stand.")

    return hand

def play_blackjack(balance):
    shoe = create_shoe()
    bet = place_bet()
    print("\n--- Player's Turn ---")
    player_hand = player_play(shoe)
    player_value = calculate_hand_value(player_hand)

    if player_value > 21:
        print("\nDealer Wins! You busted.")
        return loser(balance, bet)

    print("\n--- Dealer's Turn ---")
    dealer_hand = dealer_play(shoe)
    dealer_value = calculate_hand_value(dealer_hand)

    print("\nDealer's Hand:")
    for card in dealer_hand:
        print(f"{card['rank']} of {card['suit']}")
    print(f"Total Value: {dealer_value}")

    if dealer_value > 21:
        print("\nDealer Busts! You win!")
        return winner(balance, bet)
    elif player_value > dealer_value:
        print("\nYou win!")
        return winner(balance, bet)
    elif player_value < dealer_value:
        print("\nDealer wins!")
        return loser(balance, bet)
    else:
        print("\nIt's a tie!")
        print(f"Balance remains: ${balance}")
        return balance

# Run the game
balance = 100  # Starting balance
cont = "y"
while cont.lower() == "y":
    print(f"Current balance: ${balance}")
    balance = play_blackjack(balance)
    if balance <= 0:
        print("You ran out of money! Game over.")
        break
    cont = input("Continue? (y/n): ")
