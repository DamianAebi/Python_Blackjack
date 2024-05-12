import random
from enum import Enum


class CardType(Enum):
    NUMBER_CARD = 1,
    FACE_CARD = 2,
    ACE = 3
    NONE = 4


class CardFace(Enum):
    JACK = 1,
    QUEEN = 2,
    KING = 3,
    NONE = 4


class CardSuit(Enum):
    HEARTS = 1,
    CLUBS = 2,
    SPADES = 3,
    DIAMONDS = 4,
    NONE = 5


SUIT_SYMBOL_DICT = {
    CardSuit.HEARTS: '♥',
    CardSuit.CLUBS: '♣',
    CardSuit.SPADES: '♠',
    CardSuit.DIAMONDS: '♦'
}


class Card:
    def __init__(self, card_suit: CardSuit = CardSuit.NONE, card_type: CardType = CardType.NONE,
                 card_face: CardFace = CardFace.NONE, card_number: int = 0, card_value: int = 0,
                 card_covered: bool = False):
        self.card_suit = card_suit
        self.card_type = card_type
        self.card_face = card_face
        self.card_number = card_number
        self.card_value = card_value
        self.card_covered = card_covered

    def __str__(self):
        match self.card_type:
            case CardType.NUMBER_CARD:
                return f"{self.card_number} of {SUIT_SYMBOL_DICT[self.card_suit]}"
            case CardType.FACE_CARD:
                return f"{self.card_face.name} of {SUIT_SYMBOL_DICT[self.card_suit]}"
            case CardType.ACE:
                return f"ACE of {SUIT_SYMBOL_DICT[self.card_suit]}"
            case _:
                return "Something went wrong when printing this card."


class Deck:
    def __init__(self):
        self.cards = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def populate_deck(self, amount_of_decks: int = 1):
        """Method that adds all 52 possible playing cards as Card-objects to the deck."""
        card_suits = [CardSuit.HEARTS, CardSuit.CLUBS, CardSuit.SPADES, CardSuit.DIAMONDS]
        card_types = [CardType.NUMBER_CARD, CardType.FACE_CARD, CardType.ACE]
        card_faces = [CardFace.JACK, CardFace.QUEEN, CardFace.KING]
        for i in range(amount_of_decks):
            for card_suit in card_suits:
                for card_type in card_types:
                    match card_type:
                        case CardType.FACE_CARD:
                            for card_face in card_faces:
                                card = Card(card_suit, card_type, card_face, 0, 10)
                                self.add_card(card)
                        case CardType.NUMBER_CARD:
                            for j in range(9):
                                card = Card(card_suit, card_type, CardFace.NONE, j + 2, j + 2)
                                self.add_card(card)
                        case CardType.ACE:
                            card = Card(card_suit, card_type)
                            self.add_card(card)
                        case _:
                            print("Something went wrong whilst populating the Deck.")

    def draw_card(self, card_amount: int = 1, card_covered: bool = False) -> list[Card]:
        """Draw a random card from the deck."""
        # if the deck is empty, populate a new deck
        if len(self.cards) <= 0:
            print("Deck is empty. Populating new deck.")
            self.populate_deck(1)

        # pop a random card out of the deck and add it to the list to return
        card_list = []
        for i in range(card_amount):
            card_list.append(
                self.cards.pop(
                    random.randint(0, len(self.cards) - 1)
                )
            )

        # set cards to card_covered if desired
        if card_covered:
            for card in card_list:
                card.card_covered = True

        return card_list
