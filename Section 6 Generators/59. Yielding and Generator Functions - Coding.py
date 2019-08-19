print('#' * 52 + '  ### Yielding and Generators')

import math

class FactIter:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        else:
            result = math.factorial(self.i)
            self.i += 1
            return result

fact_iter = FactIter(5)

for num in fact_iter:
    print(num)

print('#' * 52 + '  We could achieve the same thing using the `iter` methods second form -'
                 '  we just have to know our sentinel value - in this case it would be'
                 '  the factorial of n+1 where n is the last integers factorial we want our iterator to produce:')

def fact():
    i = 0
    def inner():
        nonlocal i
        result = math.factorial(i)
        i += 1
        return result
    return inner

fact_iter = iter(fact(), math.factorial(5))

for num in fact_iter:
    print(num)

print('#' * 52 + '  ')
print('#' * 52 + '  ')
print('#' * 52 + '  ')

def my_func():
    print('line 1')
    yield 'Flying'
    print('line 2')
    yield 'Circus'

print(my_func())

print('#' * 52 + '  So, executing `my_func()`, returned a generator object - it did not actually "run"'
                 '  the body of `my_func` (none of our print statements actually ran).')
print('#' * 52 + '  To do that, we need to use the `next()` function. ')

gen_my_func = my_func()
print(next(gen_my_func))
print('#' * 52 + '  ')
print(next(gen_my_func))

print('#' * 52 + '  And lets call it one more time:')

# print(next(gen_my_func)) # StopIteration:

print('#' * 52 + '  An **iterator**!')
print('#' * 52 + '  And in fact that is exactly what Python generators are - they **are** iterators. ')
print('#' * 52 + '  If generators are iterators, they should implement the iterator **protocol**.')

gen_my_func = my_func()
print('__iter__' in dir(gen_my_func))
print('__next__' in dir(gen_my_func))

print('#' * 52 + '  And so we just have an iterator, which we can use with the `iter()` function and the `next()`'
                 '  function like any other iterator:')

print(gen_my_func)

print('#' * 52 + '  ')

def squares(sentinel):
    i = 0
    while True:
        if i < sentinel:
            result = i**2
            i += 1
            yield result
        else:
            return 'all done!'

sq = squares(3)
print(next(sq))
print(next(sq))
print(next(sq))
# print(next(sq))   # StopIteration: all done!

print('#' * 52 + '  But, we can simplify this slightly:')

def squares(sentinel):
    i = 0
    while True:
        if i < sentinel:
            yield i**2
            i += 1 # note how we can incremenet **after** the yield
        else:
            return 'all done!'

for num in squares(5):
    print(num)

print('#' * 52 + '  So now lets see how we could re-write our initial `factorial` example:')


def factorials(n):
    for i in range(n):
        yield math.factorial(i)

for num in factorials(5):
    print(num)

print('#' * 52 + '  Note that a generator **is** an iterator, but not vice-versa - '
                 '  iterators are not necessarily generators,'
                 '  just like sequences are iterables, but iterables are not necessarily sequences.')
print('#' * 52 + '  Another thing to note is that since generators are iterators,'
                 '  they also  become exhausted (consumed) just like an iterator does.')

facts = factorials(5)
print(list(facts))
print(list(facts))

# next(facts)  # StopIteration: