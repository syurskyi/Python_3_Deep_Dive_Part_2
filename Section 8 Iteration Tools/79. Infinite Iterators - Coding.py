print('#' * 52 + '  There are three functions in the `itertools` module that produce infinite iterators:'
                 ' `count`,'
                 ' `cycle`'
                 ' and `repeat`.')

from itertools import (
    count,
    cycle,
    repeat,
    islice)

print('#' * 52 + '  #### count')
print('#' * 52 + '  The `count` function is similar to range, except it does not have a `stop` value.'
                 '  It has both a `start` and a `step`:')

g = count(10)

print(list(islice(g, 5)))

g = count(10, step=2)

print(list(islice(g, 5)))

print('#' * 52 + '  Unlike the `range` function, whose arguments must always be integers,'
                 '  `count` works with floats as well:')

g = count(10.5, 0.5)

print(list(islice(g, 5)))

print('#' * 52 + '  In fact, we can even use other data types as well:')

g = count(1 + 1j, 1 + 2j)

print(list(islice(g, 5)))

print('#' * 52 + '  We can even use Decimal numbers:')

from decimal import Decimal

g = count(Decimal('0.0'), Decimal('0.1'))

print(list(islice(g, 5)))

print('#' * 52 + '  ')
print('#' * 52 + '  ### Cycle')
print('#' * 52 + '  `cycle` is used to repeatedly loop over an iterable:')

g = cycle(('red', 'green', 'blue'))
print(list(islice(g, 8)))

print('#' * 52 + '  One thing to note is that this works **even**'
                 '  if the argument is an iterator (i.e. gets exhausted after the first complete iteration over it)!')


def colors():
    yield 'red'
    yield 'green'
    yield 'blue'


cols = colors()

print(list(cols))

print(list(cols))

print('#' * 52 + '  As expected, `cols` was exhausted after the first iteration.')
print('#' * 52 + '  Now lets see how `cycle` behaves:')

cols = colors()
g = cycle(cols)

print(list(islice(g, 10)))

print('#' * 52 + '  As you can see, `cycle` iterated over the elements of iterator, and continued the iteration'
                 '  even though the first run through the iterator technically exhausted it.')

print('#' * 52 + '  A simple application of `cycle` is dealing a deck of cards into separate hands:')

from collections import namedtuple

Card = namedtuple('Card', 'rank suit')


def card_deck():
    ranks = tuple(str(num) for num in range(2, 11)) + tuple('JQKA')
    suits = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
    for suit in suits:
        for rank in ranks:
            yield Card(rank, suit)


hands = [list() for _ in range(4)]

print(hands)
print('#' * 52 + '  ')

index = 0
for card in card_deck():
    index = index % 4
    hands[index].append(card)
    index += 1

print(hands)

print('#' * 52 + '  You notice how we had to use the `mod` operator and an `index` to **cycle** through the hands.')
print('#' * 52 + '  So, we can use the `cycle` function instead:')

hands = [list() for _ in range(4)]

index_cycle = cycle([0, 1, 2, 3])
for card in card_deck():
    hands[next(index_cycle)].append(card)

print(hands)

print('#' * 52 + '  But we really can simplify this even further - why are we cycling through the indices?')
print('#' * 52 + '  Why not simply cycle through the hand themselves, and append the card to the hands?')

hands = [list() for _ in range(4)]

hands_cycle = cycle(hands)
for card in card_deck():
    next(hands_cycle).append(card)

print(hands)

print('#' * 52 + '  ')
print('#' * 52 + '  #### Repeat')
print('#' * 52 + '  The `repeat` function is used to create an iterator that just returns the same value'
                 '  again and again.')
print('#' * 52 + '  By default it is infinite, but a count can be specified optionally:')

g = repeat('Python')
for _ in range(5):
    print(next(g))

print('#' * 52 + '  And we also optionally specify a count to make the iterator finite:')

# print(list(g))

print('#' * 52 + '  The important thing to note as well, is that the "value" that is returned is'
                 '  the **same** object every time!')

l = [1, 2, 3]
result = list(repeat(l, 3))
print(result)
print(l is result[0], l is result[1], l is result[2])

print('#' * 52 + '   If you try to use repeat to create three separate instances of a list, you will actually end up'
                 '   with shared references:')

print(result[0], result[1], result[2])
result[0][0] = 100

print(result[0], result[1], result[2])

print('#' * 52 + '  If you want to end up with three separate copies of your argument, then you wiill need to use'
                 '  a copy mechanism (either shallow or deep depending on your needs).')

l = [1, 2, 3]
result = [item[:] for item in repeat(l, 3)]

print(result)

print(l is result[0], l is result[1], l is result[2])
result[0][0] = 100
print(result)
