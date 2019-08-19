print('#' * 52 + '  We know that sequence types can be sliced:')

l = [1, 2, 3, 4, 5]

print(l[0:2])

print('#' * 52 + '  Equivalently we can use the `slice` object:')

s = slice(0, 2)

print(l[s])

print('#' * 52 + '  But this does not work with iterables that are not also sequence types:')

import math


def factorials(n):
    for i in range(n):
        yield math.factorial(i)


facts = factorials(100)
# print(facts[0:2]) #  TypeError: 'generator' object is not subscriptable


print('#' * 52 + '  But we could write a function to mimic this. Lets try a simplistic approach'
                 '  that will only work for a consecutive slice:')


def slice_(iterable, start, stop):
    for _ in range(0, start):
        next(iterable)

    for _ in range(start, stop):
        yield (next(iterable))


print(list(slice_(factorials(100), 1, 5)))

print('#' * 52 + '  This is quite simple, however we dont support a `step` value.')
print('#' * 52 + '  The `itertools` module has a function, `islice` which implements this for us:')

print(list(factorials(10)))

print('#' * 52 + '  Now lets use the `islice` function to obtain the first 3 elements:')

from itertools import islice

print(islice(factorials(10), 0, 3))

print('#' * 52 + '  `islice` is itself a lazy iterator, so we can iterate through it:')

print(list(islice(factorials(10), 0, 3)))

print('#' * 52 + '  We can even use a step value:')

print(list(islice(factorials(10), 0, 10, 2)))

print('#' * 52 +'It does not support negative indices, or step values, but it does support None for all the arguments.')

print(list(islice(factorials(10), None, None, 2)))

print('#' * 52 + '  This function can be very useful when dealing with infinite iterators for example.')

def factorials():
    index = 0
    while True:
        yield math.factorial(index)
        index += 1

facts = factorials()
for _ in range(5):
    print(next(facts))

print('#' * 52 + '  Or we could use `islice` as follows:')

print(list(islice(factorials(), 5)))

print('#' * 52 + '  One thing to note is that `islice` is a lazy iterator,'
                 '  but when we use a `step` value, there is no magic,')
print('#' * 52 + '   Python still has to call `next` on our iterable - it just doesnt always yield it back to us.')

def factorials():
    index = 0
    while True:
        print(f'yielding factorial({index})...')
        yield math.factorial(index)
        index += 1

print(list(islice(factorials(), 9)))

print('#' * 52 + '  ')

print(list(islice(factorials(), None, 10, 2)))

print('#' * 52 + '  As you can see, even though 5 elements were yielded from `islice`,'
                 '  it still had to call our generator 10 times!')

print('#' * 52 + '  The same thing happens if we skip elements in the slice,'
                 '  it still has to call next for the skipped elements:')

print(list(islice(factorials(), 5, 10)))

print('#' * 52 + '  The other thing to watch out for is that islice is an **iterator** -'
                 '  which means it becomes exhausted, **even if you pass an iterable such as a list to it**!')

l = [1, 2, 3, 4, 5]

s = islice(l, 0, 3)

print(list(s))

print(list(s))

print('#' * 52 + '  Furthermore, keep in mind that `islice` iterates over our iterable in order to yield'
                 '  the appropriate values.')

print('#' * 52 + '  This means that if we use an iterator, that iterator will get consumed, and possibly exhausted:')

facts = factorials()

print(next(facts), next(facts), next(facts), next(facts))

print('#' * 52 + '  If we now start slicing `facts` with `islice`, remember that the first four values'
                 '  of `facts` have already been consumed!')

print(list(islice(facts, 0, 3)))

print('#' * 52 + '  And of course, `islice` further consumed our iterator:')

print(next(facts))