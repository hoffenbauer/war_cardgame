"""
A simple War card game meant to be played by the computer.
One card is drawn from each player's deck. Their values are compared and
the player with the highest card gets both. If there is a tie (called a
war), a set of five cards is drawn from each player and the value of the
last one is compared. While at war, if a new tie occurs, five more cards
are drawn from each player and the last one is once again compared. This
process is repeated until one of the players wins the war. This player,
then, receives all cards, the two initial ones and the whole stack of
war. If a tie happens, both in a regular round or during war, and the
player does not enough cards to draw, the game ends and the player with
more cards wins.
"""

from random import shuffle
from itertools import product

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine','Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7,
          'eight':8, 'nine':9, 'ten':10, 'jack':11,
          'queen':12, 'king':13, 'ace':14}
all_cards = product(suits,ranks)

class Card:
    """
    Creates the cards for the game with rank and suit, respectively from
    ranks and suits tuples; value is attributed based on the values (...)
    dictionary and used for comparison.
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank.lower()]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    """
    Creates a deck of 52 cards using the Card class.
    """
    def __init__(self):
        self.cards = [Card(suit, rank) for suit, rank in all_cards]

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        """
        Shuffles the deck of cards.
        """
        shuffle(self.cards)

class Player():
    """
    Creates a player with the actions for the match as methods.
    """
    def __init__(self, name):
        self.name = name
        self.war_deck = None
        self.cards = []

    def __str__(self):
        return f"{self.name} has {len(self.cards)} cards."

    def draw_card(self):
        """
        Draws the first card of the player deck.
        """
        return self.cards.pop(0)

    def add_card(self, cards_to_add):
        """
        Adds the card(s) won in the round to the player's deck.
        """
        return self.cards.extend(cards_to_add)

    def war(self):
        """
        Draws the five first cards of the player deck in case there's war (tie).
        """
        self.war_deck = self.cards[:5]
        del self.cards[:5]
        return self.war_deck

player1 = Player('Player_1')
player2 = Player('Player_2')

game_deck = Deck()
game_deck.shuffle()

player1.cards = game_deck.cards[:26]
player2.cards = game_deck.cards[26:]

def check_winner():
    """
    Checks if either player has no cards, therefore ending the game.
    """
    winner = False, 'winner_name'

    if len(player1.cards) == 0 :
        winner = True, "Player 2 wins!"
    elif len(player2.cards) == 0:
        winner = True, "Player 1 wins!"
    return winner

def play_game():
    """
    Compares the cards drawn from each player. If a tie happens,
    the war rules apply until a player draws a higher card.
    """
    game_round = 1
    game_won = False
    war_stack = []

    while not game_won:

        p1_round = player1.draw_card()
        p2_round = player2.draw_card()

        print("Round ", game_round)
        print(f"{p1_round} vs {p2_round}")

        if p1_round.value > p2_round.value:
            player1.add_card([p1_round, p2_round])
        elif p1_round.value < p2_round.value:
            player2.add_card([p1_round, p2_round])
        else:
            while True:

                if len(player1.cards) < 4:
                    player1.add_card([p1_round])
                    player2.add_card([p2_round])
                    print("Player 1 is out of cards, Player 2 wins!")
                    game_won = True
                    break
                if len(player2.cards) < 4:
                    player1.add_card([p1_round])
                    player2.add_card([p2_round])
                    print("Player 2 is out of cards, Player 1 wins!")
                    game_won = True
                    break
                #Both players have enough cards.
                p1_war_deck = player1.war()
                p2_war_deck = player2.war()
                war_stack += p1_war_deck + p2_war_deck
                print(f"{p1_war_deck[-1]} vs {p2_war_deck[-1]}")

                if p1_war_deck[-1].value > p2_war_deck[-1].value:
                    player1.add_card(war_stack)
                    player1.add_card([p1_round, p2_round])
                    war_stack = []
                    break
                if p1_war_deck[-1].value < p2_war_deck[-1].value:
                    player2.add_card(war_stack)
                    player2.add_card([p1_round, p2_round])
                    war_stack = []
                    break

        game_round += 1
        print(f"P1: {len(player1.cards)}, P2: {len(player2.cards)}\n")
        if check_winner()[0]:
            print(check_winner()[1])
            break
    print("Game over!")
