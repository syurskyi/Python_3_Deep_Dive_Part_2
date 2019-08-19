from collections import namedtuple

Card = namedtuple('Card', 'rank, suit')
SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
RANKS = tuple(range(2, 11)) + tuple('JQKA')


def card_gen():
    for i in range(len(SUITS) * len(RANKS)):
        suit = SUITS[i // len(RANKS)]
        rank = RANKS[i % len(RANKS)]
        card = Card(rank, suit)
        yield card


for card in card_gen():
    print(card)

print('#' * 52 + '  But we can really simplify this further!')
print('#' * 52 + '  We dont have to use these indices at all!')


def card_gen():
    for suit in SUITS:
        for rank in RANKS:
            card = Card(rank, suit)
            yield card


for card in card_gen():
    print(card)

print('#' * 52 + '  We can now make it into an iterable:')


class CardDeck:
    SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
    RANKS = tuple(range(2, 11)) + tuple('JQKA')

    def __iter__(self):
        return CardDeck.card_gen()

    @staticmethod
    def card_gen():
        for suit in CardDeck.SUITS:
            for rank in CardDeck.RANKS:
                card = Card(rank, suit)
                yield card


deck = CardDeck()
print([card for card in deck])

print('#' * 52 + '  And of course we can do it again:')

print([card for card in deck])

print('#' * 52 + '  One thing we dont have here is the support for `reversed`:')

# reversed(CardDeck()) # TypeError: 'CardDeck' object is not reversible

print('#' * 52 + '  But we can add it in by implementing the `__reversed__`'
                 '  method and returning an iterator that iterates the deck in reverse order.')


class CardDeck:
    SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
    RANKS = tuple(range(2, 11)) + tuple('JQKA')

    def __iter__(self):
        return CardDeck.card_gen()

    def __reversed__(self):
        return CardDeck.reversed_card_gen()

    @staticmethod
    def card_gen():
        for suit in CardDeck.SUITS:
            for rank in CardDeck.RANKS:
                card = Card(rank, suit)
                yield card

    @staticmethod
    def reversed_card_gen():
        for suit in reversed(CardDeck.SUITS):
            for rank in reversed(CardDeck.RANKS):
                card = Card(rank, suit)
                yield card


rev = reversed(CardDeck())
print([card for card in rev])

