print('#' * 52 + '  ### Chaining and Teeing Iterators')

l1 = (i ** 2 for i in range(4))
l2 = (i ** 2 for i in range(4, 8))
l3 = (i ** 2 for i in range(8, 12))

print('#' * 52 + '  And we want to essentially iterate through all the values as if they were a single iterator.')

for gen in (l1, l2, l3):
    for item in gen:
        print(item)

print('#' * 52 + '  In fact, we could even create our own generator function to do this:')


def chain_iterables(*iterables):
    for iterable in iterables:
        yield from iterable


l1 = (i ** 2 for i in range(4))
l2 = (i ** 2 for i in range(4, 8))
l3 = (i ** 2 for i in range(8, 12))

for item in chain_iterables(l1, l2, l3):
    print(item)

print('#' * 52 + '  But, a much simpler way is to use `chain` in the `itertools` module:')

from itertools import chain

l1 = (i**2 for i in range(4))
l2 = (i**2 for i in range(4, 8))
l3 = (i**2 for i in range(8, 12))

for item in chain(l1, l2, l3):
    print(item)

print('#' * 52 + '  Note that `chain` expects a variable number of positional arguments,'
                 '  each of which should be an iterable.')
print('#' * 52 + '  It will not work if we pass it a single iterable:')

l1 = (i**2 for i in range(4))
l2 = (i**2 for i in range(4, 8))
l3 = (i**2 for i in range(8, 12))

lists = [l1, l2, l3]
for item in chain(lists):
    print(item)

print('#' * 52 + '  As you can see, it simply took our list and handed it back directly - '
                 ' there was nothing else to chain with:')

l1 = (i**2 for i in range(4))
l2 = (i**2 for i in range(4, 8))
l3 = (i**2 for i in range(8, 12))

lists = [l1, l2, l3]
for item in chain(lists):
    for i in item:
        print(i)

print('#' * 52 + '  Instead, we could use unpacking:')

l1 = (i**2 for i in range(4))
l2 = (i**2 for i in range(4, 8))
l3 = (i**2 for i in range(8, 12))

lists = [l1, l2, l3]
for item in chain(*lists):
    print(item)

print('#' * 52 + '  Unpacking works with iterables in general, so even the following would work just fine:')

def squares():
    yield (i**2 for i in range(4))
    yield (i**2 for i in range(4, 8))
    yield (i**2 for i in range(8, 12))

for item in chain(*squares()):
    print(item)

print('#' * 52 + '  But, unpacking is not lazy!! Here is a simple example that shows this, '
                 '  and why we have to be careful using unpacking if we want to preserve lazy evaluation:')

def squares():
    print('yielding 1st item')
    yield (i**2 for i in range(4))
    print('yielding 2nd item')
    yield (i**2 for i in range(4, 8))
    print('yielding 3rd item')
    yield (i**2 for i in range(8, 12))

def read_values(*args):
    print('finised reading args')

read_values(*squares())

print('#' * 52 + '  Instead we can use an alternate "constructor" for chain, that takes a single iterable (of iterables)'
                 '  and lazily iterates through the outer iterable as well:')

c = chain.from_iterable(squares())

for item in c:
    print(item)

print('#' * 52 + '  Note also, that we can easily reproduce the same behavior of either chain quite easily:')

def chain_(*args):
    for item in args:
        yield from item

def chain_iter(iterable):
    for item in iterable:
        yield from item

print('#' * 52 + '  And we can use those just as we saw before with `chain` and `chain.from_iterable`:')

c = chain_(*squares())

print('#' * 52 + '  ')

c = chain_iter(squares())
for item in c:
    print(item)

print('#' * 52 + '  ### "Copying" an Iterator')
print('#' * 52 + '  Sometimes we may have an iterator that we want to use multiple times for some reason.')
print('#' * 52 + '  As we saw, iterators get exhausted, so simply making multiple references to the same iterator '
                 '  will not work - they will just point to the same iterator object.')
print('#' * 52 + '  What we would really like is a way to "copy" an iterator and use these copies independently'
                 '  of each other.')
print('#' * 52 + '  We can use `tee` in `itertools`:')

from itertools import tee

def squares(n):
    for i in range(n):
        yield i**2

gen = squares(10)
print(gen)

iters = tee(squares(10), 3)

print(iters)

print(type(iters))

print('#' * 52 + '  As you can see `iters` is a **tuple** contains 3 iterators - lets put them into some variables'
                 '  and see what each one is:')

iter1, iter2, iter3 = iters

print(next(iter1), next(iter1), next(iter1))
print(next(iter2), next(iter2))
print(next(iter3))

print('#' * 52 + '  As you can see, `iter1`, `iter2`, and `iter3` are essentially three independent "copies" '
                 '  of our original iterator (`squares(10)`)')
print('#' * 52 + '  Note that this works for any iterable, so even sequence types such as lists:')

l = [1, 2, 3, 4]

lists = tee(l, 2)

print(lists[0])

print(lists[1])

print('#' * 52 + '  But you will notice that the elements of `lists` are not lists themselves!')

print(list(lists[0]))

print(list(lists[0]))

print('#' * 52 + '  As you can see, the elements returned by `tee` are actually `iterators` - '
                 '  even if we used an iterable such as a list to start off with!')

print(lists[1] is lists[1].__iter__())

print('__next__' in dir(lists[1]))


