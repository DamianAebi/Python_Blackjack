from Blackjack.blackjack_deck import CardType, Deck


class Participant:
    def __init__(self):
        self.hand = []

    def draw(self, deck: Deck, card_amount: int = 1, card_covered: bool = False, name: str = "") -> None:
        for card in deck.draw_card(card_amount, card_covered):
            self.hand.append(card)

        print(name, "drew", card_amount, "cards. Hand now looks like this:")

    def get_hand_value(self) -> int:
        """Returns the total value of all cards in the hand"""
        # first, sum all non-ace cards up.
        hand_value = sum(card.card_value for card in self.hand if card.card_type != CardType.ACE)

        # then, for each ace, check if it can be 11, else it's 1
        aces = [card for card in self.hand if card.card_type == CardType.ACE]
        for ace in aces:
            if hand_value + 11 <= 21:
                ace.card_value = 11
            else:
                ace.card_value = 1

            hand_value += ace.card_value

        # handle edge-case where multiple aces overshoot 21 because they don't know of each other
        while hand_value > 21 and len(aces) > 1 and any(ace.card_value == 11 for ace in aces):
            # setting aces to 1 one at a time, for as long as the hand_value overshoots 21
            for ace in aces:
                if ace.card_value == 11:
                    hand_value -= ace.card_value
                    ace.card_value = 1
                    hand_value += ace.card_value
                    break

        # if the card is covered, don't count its value
        for card in self.hand:
            if card.card_covered:
                hand_value -= card.card_value

        return hand_value


class Dealer(Participant):
    def __init__(self):
        super().__init__()

    def uncover(self) -> None:
        print("Dealer is uncovering his hand:")
        for card in self.hand:
            card.card_covered = False

    def draw(self, deck: Deck, card_amount: int = 1, card_covered: bool = False, name: str = "Dealer") -> None:
        """Calls draw function of super class and passes 'Dealer' as the name."""
        super().draw(deck, card_amount, card_covered, name)


class Player(Participant):
    def __init__(self):
        super().__init__()
        self.total_chips = 0
        self.bet = 0
        self.hit = True

    def try_place_bet(self, amount_of_chips: int) -> bool:
        """
        Tries placing a bet.
            - If given bet amount is too high or low, it returns False
            - If given bet amount is valid, bet is added and it returns True
        """
        if amount_of_chips < 1:
            print("You need to bet at least 1 chip.")
            return False
        if self.total_chips - amount_of_chips < 0:
            print(
                f"You don't have enough chips to place a bet of {amount_of_chips}. "
                f"You only have {self.total_chips} left."
            )
            return False

        self.total_chips -= amount_of_chips
        self.bet += amount_of_chips
        print(f"Bet {amount_of_chips} chips. {self.total_chips} chips left.")
        return True

    def set_hit(self, hit: bool) -> None:
        self.hit = hit

    def draw(self, deck: Deck, card_amount: int = 1, card_covered: bool = False, name: str = "Player") -> None:
        """Calls draw function of super class and passes 'Player' as the name."""
        super().draw(deck, card_amount, card_covered, name)
