from Blackjack.blackjack_deck import Deck
from Blackjack.blackjack_participants import Player, Dealer
from Utils.general_untility import Utils


class Game:
    def __init__(self, amount_of_decks: int = 1):
        print("Welcome to BlackJack!")
        self.player_chips = 0
        self.goal = 0
        self.deck = Deck()
        self.deck.populate_deck(amount_of_decks)
        self.player = Player()
        self.dealer = Dealer()
        self.start_game()

    def start_game(self):
        # ask for chips
        while True:
            chip_input = Utils.validated_input("How many chips do you want?: ", int)

            if chip_input not in range(1, 100000):
                print("Please enter a number between one and a million")
                continue

            break

        # ask for goal
        while True:
            goal_input = Utils.validated_input("How many chips do you want to reach?: ", int)

            if goal_input <= chip_input:
                print("Goal has to be bigger than amount of chips.")
                continue

            break

        self.player.total_chips = chip_input
        self.goal = goal_input

        # start rounds for as long as the player still has chips and didn't achieve the goal yet
        while 0 < self.player.total_chips < self.goal:
            self.start_round()

        # check if he won or lost at the end
        if self.player.total_chips >= self.goal:
            print("Congratulations, you reached your goal. You won!!!!")
        else:
            print("Your chips ran out. You lost the game.")

    def start_round(self):
        """Method to play a Blackjack-round"""
        print(f"Starting new round. Current score: {self.player.total_chips}/{self.goal}")

        # get player bet
        while True:
            bet = Utils.validated_input("Place your bet: ", int)
            if not self.player.try_place_bet(bet):
                print("Try betting again.")
                continue

            break

        # player draws 2, dealer 1 face up 1 face down
        self.player.draw(self.deck, 2)
        self.dealer.draw(self.deck, 1, False)
        self.dealer.draw(self.deck, 1, True)
        self.print_game()
        self.player.set_hit(True)

        # For as long as the player is below 21 and wants to play, he can take cards
        while self.player.get_hand_value() <= 21 and self.player.hit:
            hit_input = -1
            # ask player if he wants to stay or hit
            while hit_input == -1:
                hit_input = input("Do you want another card? Type 1 or 0: ")
                match hit_input:
                    case "1":
                        hit_input = True
                    case "0":
                        hit_input = False
                    case _:
                        print("Input invalid. Try again.")
                        hit_input = -1
            # if he wants to hit, draw a card, else go on
            if hit_input:
                self.player.draw(self.deck, 1)
                self.print_game()
            else:
                self.player.set_hit(False)

        # if the player's hand values more than 21, he lost
        if self.player.get_hand_value() > 21:
            print(f"Your hand values more than 21 (current value: {self.player.get_hand_value()}). You lost the round.")
            self.loose_round()
            return

        # dealer uncovers his card that was face-down
        self.dealer.uncover()
        self.print_game()

        # if he has Blackjack, he wins
        if self.dealer.get_hand_value() == 21:
            print(f"Dealer has Blackjack. You lost the round.")
            self.loose_round()
            return

        # whilst his hand is less than 17, he draws card
        while self.dealer.get_hand_value() < 17:
            self.dealer.draw(self.deck, 1)

        self.print_game()

        self.evaluate_round()

    def evaluate_round(self):
        """Method to evaluate if the player won, lost or tied"""
        if self.dealer.get_hand_value() > 21:
            print(
                f"Dealer's hand values more than 21 "
                f"(current value: {self.dealer.get_hand_value()}). You won the round.")
            self.win_round()
            return

        if self.dealer.get_hand_value() > self.player.get_hand_value():
            print(
                f"Dealer's hand values more than yours (Dealer: {self.dealer.get_hand_value()} "
                f"You: {self.player.get_hand_value()}). You lost the round.")
            self.loose_round()
            return

        if self.dealer.get_hand_value() == self.player.get_hand_value():
            print("Dealer has the same amount of points as you. It's a tie.")
            self.tie_round()
            return

        if self.player.get_hand_value() > self.dealer.get_hand_value():
            print(
                f"Your hand values more than the dealer's. (Your hand: {self.player.get_hand_value()} "
                f"Dealer: {self.dealer.get_hand_value()}). You won the round.")
            self.win_round()
            return

    def loose_round(self):
        self.player.bet = 0
        self.cleanup()

    def tie_round(self):
        self.player.total_chips += self.player.bet
        self.player.bet = 0
        self.cleanup()

    def win_round(self):
        self.player.total_chips += 2 * self.player.bet
        self.player.bet = 0
        self.cleanup()

    def cleanup(self):
        self.player.hand.clear()
        self.dealer.hand.clear()
        print(f"Total chips: {self.player.total_chips}.")

    def print_game(self):
        """Method to print the table somewhat nicely"""
        pv = self.player.get_hand_value()
        dv = self.dealer.get_hand_value()
        ph = self.player.hand
        dh = self.dealer.hand
        longer_index = max(len(self.player.hand), len(self.dealer.hand))
        output = """

                                 BLACKJACK TABLE                                     
-------------------------------------------------------------------------------------
                                                                                     
             YOU:                                         DEALER:                    
                                                                                     
      hand:                                         hand:                            
"""
        for i in range(longer_index):
            player_card_str = ""
            dealer_card_str = ""
            if len(ph) - 1 >= i:
                player_card_str = str(ph[i]) if not ph[i].card_covered else "X"
            if len(dh) - 1 >= i:
                dealer_card_str = str(dh[i]) if not dh[i].card_covered else "X"
            output += f"{6 * " "}{player_card_str}{(46 - len(player_card_str)) * " "}{dealer_card_str} \n"

        output += \
            f"""
                                                                                     
      total value: {pv}                               total value: {dv}                
-------------------------------------------------------------------------------------

"""
        print(output)


game = Game(amount_of_decks=1)
