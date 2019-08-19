_SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
_RANKS = tuple(range(2, 11)) + tuple('JQKA')
from collections import namedtuple

Card = namedtuple('Card', 'rank suit')


class CardDeck:
    def __init__(self):
        self.length = len(_SUITS) * len(_RANKS)

    def __len__(self):
        return self.length

    def __iter__(self):
        return self.CardDeckIterator(self.length)

    class CardDeckIterator:
        def __init__(self, length):
            self.length = length
            self.i = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.i >= self.length:
                raise StopIteration
            else:
                suit = _SUITS[self.i // len(_RANKS)]
                rank = _RANKS[self.i % len(_RANKS)]
                self.i += 1
                return Card(rank, suit)


deck = CardDeck()

for card in deck:
    print(card)

print('#' * 52 + '  One option is to generate a list of all the cards in the deck, then use a slice.')
print('#' * 52 + '  What about iterating in reverse?')
print('#' * 52 + '  Using the same technique we generate a list that contains all the cards, reverse the list,'
                 '  and then iterate over the reversed list.')

deck = list(CardDeck())
print(deck[:-8:-1])

print('#' * 52 + '  And to iterate backwards:')

deck = list(CardDeck())
deck = deck[::-1]
for card in deck:
    print(card)

print('#' * 52 + '  This is kind of inefficient since we had to generate the entire list of cards, to then reverse it,'
                 '  and then only pick the first 7 cards from that reversed list.')
print('#' * 52 + '  Maybe we can try Pythons built-in `reversed` function instead:')

deck = CardDeck()
# deck = reversed(deck) # TypeError: 'CardDeck' object is not reversible

print('#' * 52 + '  We need to somehow define a "reverse" iteration option for our iterator!')
print('#' * 52 + '  We do so by defining the __reversed__ special method in our iterable and instructing out'
                 '  iterator to return elements in reverse order.')
print('#' * 52 + '  If the `__reversed__` method is in our iterable, Python will use that to get the iterator'
                 '  when we call the `reverse()` function:')

_SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
_RANKS = tuple(range(2, 11)) + ('J', 'Q', 'K', 'A')
from collections import namedtuple

Card = namedtuple('Card', 'rank suit')


class CardDeck:
    def __init__(self):
        self.length = len(_SUITS) * len(_RANKS)

    def __len__(self):
        return self.length

    def __iter__(self):
        return self.CardDeckIterator(self.length)

    def __reversed__(self):
        return self.CardDeckIterator(self.length, reverse=True)

    class CardDeckIterator:
        def __init__(self, length, *, reverse=False):
            self.length = length
            self.reverse = reverse
            self.i = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.i >= self.length:
                raise StopIteration
            else:
                if self.reverse:
                    index = self.length - 1 - self.i
                else:
                    index = self.i
                suit = _SUITS[index // len(_RANKS)]
                rank = _RANKS[index % len(_RANKS)]
                self.i += 1
                return Card(rank, suit)


deck = CardDeck()
for card in deck:
    print(card)

deck = reversed(CardDeck())
for card in deck:
    print(card)

print('#' * 52 + '  #### Reversing Sequences')
print('#' * 52 + '  I just want to point out that if we have a custom **sequence** type'
                 '  we dont need to worry about this.')


class Squares:
    def __init__(self, length):
        self.squares = [i ** 2 for i in range(length)]

    def __len__(self):
        return len(self.squares)

    def __getitem__(self, s):
        return self.squares[s]

sq = Squares(10)

for num in Squares(5):
    print(num)

print('#' * 52 + '  ')

for num in reversed(Squares(5)):
    print(num)

print('#' * 52 + '  As you can see Python was able to automatically reverse the sequence for us.')
print('#' * 52 + '  Also worth noting is that the `__len__` method **must** be implemented for `reversed()` to work:')


class Squares:
    def __init__(self, length):
        self.squares = [i ** 2 for i in range(length)]

    #     def __len__(self):
    #         return len(self.squares)

    def __getitem__(self, s):
        return self.squares[s]

# for num in reversed(Squares(5)):
#     print(num)                         # TypeError: object of type 'Squares' has no len()

print('#' * 52 + '  In addition, we can override what is returned when the `reversed()`'
                 '  function is called on our custom sequence type.')
print('#' * 52 + '  Here, I will return a the list of the integers themselves instead of squares'
                 '  just to make this really stand out:')


class Squares:
    def __init__(self, length):
        self.length = length
        self.squares = [i ** 2 for i in range(length)]

    def __len__(self):
        return len(self.squares)

    def __getitem__(self, s):
        return self.squares[s]

    def __reversed__(self):
        print('__reversed__ called')
        return [i for i in range(self.length - 1, -1, -1)]

for num in Squares(5):
    print(num)

for num in reversed(Squares(5)):
    print(num)


