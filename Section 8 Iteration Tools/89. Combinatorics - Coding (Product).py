print('#' * 52 + '  ### Combinatorics')
print('#' * 52 + '  There are a number of functions in `itertools` that are concerned with thing like'
                 '  permutations and combinations.')

import itertools

print('#' * 52 + '  #### Cartesian Product')


def matrix(n):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            yield f'{i} x {j} = {i*j}'

print(list(itertools.islice(matrix(10), 10, 20)))

print('#' * 52 + '  So, the Cartesian product of two iterables in general can be generated using a nested loop:')

l1 = ['x1', 'x2', 'x3', 'x4']
l2 = ['y1', 'y2', 'y3']
for x in l1:
    for y in l2:
        print((x, y), end=' ')
    print('')

print('#' * 52 + '  We can achieve the same result with the `product` function in `itertools`.')
print('#' * 52 + '  As usual, it is lazy as well.')

l1 = ['x1', 'x2', 'x3', 'x4']
l2 = ['y1', 'y2', 'y3']
print(list(itertools.product(l1, l2)))

print('#' * 52 + '  As a simple example, '
                 '  lets go back to the multiplication table we created using a generator function.')

def matrix(n):
    for i in range(1, n+1):
        for j in range(1, n+1):
            yield (i, j, i*j)

print(list(matrix(4)))

print('#' * 52 + '  ')

def matrix(n):
    for i, j in itertools.product(range(1, n+1), range(1, n+1)):
        yield (i, j, i*j)

print(list(matrix(4)))

print('#' * 52 + '  And of course this is now simple enough to even use just a generator expression:')

def matrix(n):
    return ((i, j, i*j)
            for i, j in itertools.product(range(1, n+1), range(1, n+1)))

print(list(matrix(4)))

print('#' * 52 + '  You will notice how we repeated the `range(1, n+1)` twice?')
print('#' * 52 + '  This is a great example of where `tee` can be useful:')

from itertools import tee

def matrix(n):
    return ((i, j, i*j)
            for i, j in itertools.product(*itertools.tee(range(1, n+1), 2)))

print(list(matrix(4)))

print('#' * 52 + '  #### Example 1')


def grid(min_val, max_val, step, *, num_dimensions=2):
    axis = itertools.takewhile(lambda x: x <= max_val,
                               itertools.count(min_val, step))

    # to handle multiple dimensions, we just need to repeat the axis that
    # many times - tee is perfect for that
    axes = itertools.tee(axis, num_dimensions)

    # and now we just need the product of all these iterables
    return itertools.product(*axes)

print(list(grid(-1, 1, 0.5)))

print('#' * 52 + '  And of course we can now do it in 3D as well:')

print(list(grid(-1, 1, 0.5, num_dimensions=3)))

print('#' * 52 + '  #### Example 2')

sample_space = list(itertools.product(range(1, 7), range(1, 7)))
print(sample_space)

print('#' * 52 + '  Now we want to filter out the tuples whose elements add up to 8:')

outcomes = list(filter(lambda x: x[0] + x[1] == 8, sample_space))
print(outcomes)

print('#' * 52 + '  And we can calculate the odds by dividing the number acceptable outcomes'
                 '  by the size of the sample space.')
print('#' * 52 + '  I will actually use a `Fraction` so we retain our result as a rational number:')

from fractions import Fraction
odds = Fraction(len(outcomes), len(sample_space))
print(odds)

print('#' * 52 + '  #### Permutations')

l1 = 'abc'
print(list(itertools.permutations(l1)))

print('#' * 52 + '  As you can see all the permutations are, by default, the same length as the original iterable.')
print('#' * 52 + '  We can create permutations of smaller length by specifying the `r` value:')

print(list(itertools.permutations(l1, 2)))

print('#' * 52 + '  The important thing to note is that elements are not repeated in the permutation. ')
print('#' * 52 + '  But the uniqueness of an element is **not** based on its value,'
                 '  but rather on its **position** in the original iterable.')

print(list(itertools.permutations('aaa')))

print('#' * 52 + '  This means that the following will yield what looks like the same permutations'
                 '  when considering the **values** of the iterable:')

print(list(itertools.permutations('aba', 2)))

print('#' * 52 + '  #### Combinations')

print(list(itertools.combinations([1, 2, 3, 4], 2)))

print('#' * 52 + '  As you can see `(4, 3)` is not included in the result since, as a combination, '
                 ' it is the same as `(3, 4)` - order is not important.')

print(list(itertools.combinations_with_replacement([1, 2, 3, 4], 2)))

print('#' * 52 + '  #### Example 3')

print('#' * 52 + '  A simple application of this might be to calculate the odds of pulling four consecutive aces'
                 '  from a deck of 52 cards.')
print('#' * 52 + '  That is very easy to figure out, but we could use a brute force approach by calculating '
                 '  all the 4-combinations (without repetition) from a deck of 52 cards.')

SUITS = 'SHDC'
RANKS = tuple(map(str, range(2, 11))) + tuple('JQKA')

print(RANKS)

print('#' * 52 + '  I wanted all the elements in my `RANKS` to be strings - just to have a consistent data type,'
                 '  and to show you how handy `map` can be!')

deck = [rank + suit for suit in SUITS for rank in RANKS]
print(deck[0:5])

print('#' * 52 + '  Hmm... A nested loop. Maybe `product` would work well here!')

deck = [rank + suit for suit, rank in itertools.product(SUITS, RANKS)]

print('#' * 52 + '  I would much prefer having a named tuple for the deck, so lets do that as well:')

from collections import namedtuple
Card = namedtuple('Card', 'rank suit')

deck = [Card(rank, suit) for suit, rank in itertools.product(SUITS, RANKS)]
deck = (Card(rank, suit) for suit, rank in itertools.product(SUITS, RANKS))

sample_space = itertools.combinations(deck, 4)

deck = (Card(rank, suit) for suit, rank in itertools.product(SUITS, RANKS))
sample_space = itertools.combinations(deck, 4)
total = 0
acceptable = 0
for outcome in sample_space:
    total += 1
    for card in outcome:
        if card.rank != 'A':
            break
    else:
        # else block is executed if loop terminated without a break
        acceptable += 1
print(f'total={total}, acceptable={acceptable}')
print('odds={}'.format(Fraction(acceptable, total)))
print('odds={:.10f}'.format(acceptable/total))

print('#' * 52 + '  I also want to point out that we could use the `all` function instead'
                 '  of that inner `for` loop and the `else` block.')
print('#' * 52 + '  Remember that `all(iterable)` will evaluate to True if all the elements of the iterable are truthy.')
print('#' * 52 + '  Now in our case, since ranks are non-empty strings, they will always be truthy,'
                 '  so we cant use `all` directly:')

print(all(['A', 'A', '10', 'J']))

print('#' * 52 + '  Instead we can use the `map` function, yet again!, to test if the value is an A or not:')

l1 = ['K', 'A', 'A', 'A']
l2 = ['A', 'A', 'A', 'A']

print(list(map(lambda x: x == 'A', l1)))
print(list(map(lambda x: x == 'A', l2)))

print('#' * 52 + '  So now we can use `all` (and we dont have to create a list):')

print(all(map(lambda x: x == 'A', l1)))
print(all(map(lambda x: x == 'A', l2)))

print('#' * 52 + '  So, we could rewrite our algorithm as follows:')

deck = (Card(rank, suit) for suit, rank in itertools.product(SUITS, RANKS))
sample_space = itertools.combinations(deck, 4)
total = 0
acceptable = 0
for outcome in sample_space:
    total += 1
    if all(map(lambda x: x.rank == 'A', outcome)):
        acceptable += 1

print(f'total={total}, acceptable={acceptable}')
print('odds={}'.format(Fraction(acceptable, total)))
print('odds={:.10f}'.format(acceptable/total))




