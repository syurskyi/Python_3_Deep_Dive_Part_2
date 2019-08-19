print('#' * 52 + '  ### Zipping')

l1 = [1, 2, 3, 4, 5]
l2 = [1, 2, 3, 4]
l3 = [1, 2, 3]

print(list(zip(l1, l2, l3)))

print('#' * 52 + '  Of course, this works with iterators and generators too:')


def integers(n):
    for i in range(n):
        yield i


def squares(n):
    for i in range(n):
        yield i ** 2


def cubes(n):
    for i in range(n):
        yield i ** 3

iter1 = integers(6)
iter2 = squares(5)
iter3 = cubes(4)

print(list(zip(iter1, iter2, iter3)))

print('#' * 52 + '  Sometimes we want to zip up iterables but completely iterate all the iterables,'
                 '  and not stop at the shortest.')
print('#' * 52 + '  And that is how the `zip_longest` function from `itertools` works:')

from itertools import zip_longest

help(zip_longest)

print('#' * 52 + '  As you can see, we can only specify a single default value, this means'
                 '  that default will be used for any provided iterable once it has been fully iterated.')

l1 = [1, 2, 3, 4, 5]
l2 = [1, 2, 3, 4]
l3 = [1, 2, 3]

print(list(zip_longest(l1, l2, l3, fillvalue='N/A')))

print('#' * 52 + '  Of course, since this zips over the longest iterable, beware of using an infinite iterable!')
print('#' * 52 + '  You dont have to worry about this with the normal `zip` function'
                 '  as long as at least one of the iterables is finite:')

def squares():
    i = 0
    while True:
        yield i ** 2
        i += 1

def cubes():
    i = 0
    while True:
        yield i ** 3
        i += 1

iter1 = squares()
iter2 = cubes()
print(list(zip(range(10), iter1, iter2)))


