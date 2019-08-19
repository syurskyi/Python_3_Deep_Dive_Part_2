print('#' * 52 + '  ### Generator States')


def gen(s):
    for c in s:
        yield c


print('#' * 52 + '  We create an generator object by calling the generator function:')

g = gen('abc')

print(next(g))
print(next(g))

print('#' * 52 + '  Every time we call `next`, the generator function runs,'
                 '  or is in a **running** state until the next yield is encountered,'
                 '  or no more results are yielded and the function actually returns:')

print(next(g))

# print(next(g)) # StopIteration:

print('#' * 52 + '  We can actually request the state of a generator programmatically by usin'
                 '  the `inspect` modules `getgeneratorstate()` function:')

from inspect import getgeneratorstate

g = gen('abc')
print(getgeneratorstate(g))

print('#' * 52 + '  We can start running the generator by calling `next`:')

print(next(g))

print('#' * 52 + '  And the state is now:')

print(getgeneratorstate(g))

print('#' * 52 + '  Once we exhaust the generator:')

# print(next(g), next(g), next(g)) # StopIteration:

print(next(g))
print(next(g))
# print(next(g))
print(getgeneratorstate(g))

print('#' * 52 + '  The generator is now in a closed state:')

print(getgeneratorstate(g))

print('#' * 52 + '  Now we havent seen the running state - to do that we just need to print'
                 '  the state from inside the generator')
print('#' * 52 + '   - but to do that we need to have a reference to the generator object itself.')
print('#' * 52 + '  This is not that easy to do, so I m going to cheat and assume that the generator object'
                 '  will be referenced by a global variable `global_gen`:')

def gen(s):
    for c in s:
        print(getgeneratorstate(global_gen))
        yield c

global_gen = gen('abc')

print(next(global_gen))

print('#' * 52 + '  ')
print('#' * 52 + '  ')
print('#' * 52 + '  ')

def square(i):
    print(f'squaring {i}')
    return i ** 2

def squares(n):
    for i in range(n):
        yield square(i)
        print ('right after yield')

sq = squares(5)
print(next(sq))

print('#' * 52 + '  As you can see `square(i)` was evaluated,'
                 ' **then** the value was yielded, and the genrator was suspended exactly at the point'
                 ' the `yield` statement was encountered:')

print(next(sq))
