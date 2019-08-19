print('#' * 52 + '  ### Selecting and Filtering Iterators')


def gen_cubes(n):
    for i in range(n):
        print(f'yielding {i}')
        yield i ** 3


def is_odd(x):
    return x % 2 == 1


print(is_odd(4), is_odd(81))

print('#' * 52 + '  Now we can use that function (or we could have just used a lambda as well)'
                 '  with the `filter` function.')
print('#' * 52 + '  Note that the `filter` function is also lazy.')

filtered = filter(is_odd, gen_cubes(10))

print('#' * 52 + '  Notice that the `gen_cubes(10)` generator was not actually used (no print output).')
print('#' * 52 + '  We can however iterate through it:')

print(list(filtered))

print('#' * 52 + '  As we can see `filtered` will drop any values where the predicate is False.')
print('#' * 52 + '  We could easily reverse this to return not-odd (i.e. even) values:')


def is_even(x):
    return x % 2 == 0


print(list(filter(is_even, gen_cubes(10))))

print('#' * 52 + '  But we had to create a new function - instead we could use the `filterfalse` function'
                 '  in the `itertools` module that does the same work as `filter` but retains values where'
                 '  the predicate is False (instead of True as the `filter` function does).')
print('#' * 52 + '  The `filterfalse` function also uses lazy evaluation.')

from itertools import filterfalse

evens = filterfalse(is_odd, gen_cubes(10))

print(list(evens))

print('#' * 52 + ' The `takewhile` function in the `itertools` module will yield elements from an iterable, '
                 ' as long as a specific criteria (the predicate) is `True`.')
print('#' * 52 + ' As soon as the predicate is `False`, iteration is stopped - '
                 ' even if subsequent elements would have had a `True` predicate - this is not a filter, '
                 ' this basically iterate over an iterable as long as the predicate remains `True`.')

from math import sin, pi


def sine_wave(n):
    start = 0
    max_ = 2 * pi
    step = (max_ - start) / (n - 1)
    for _ in range(n):
        yield round(sin(start), 2)
        start += step


print(list(sine_wave(15)))

from itertools import takewhile

from itertools import takewhile

print(list(takewhile(lambda x: 0 <= x <= 0.9, sine_wave(15))))

print('#' * 52 + '  As you can see iteration stopped at `0.78`, even though we had values later'
                 '  that would have had a `True` predicate.')
print('#' * 52 + '  This is different from the `filter` function')

print(list(filter(lambda x: 0 <= x <= 0.9, sine_wave(15))))

print('#' * 52 + '  The `dropwhile` function on the other hand starts the iteration once the predicate becomes `False`:')

from itertools import dropwhile

l = [1, 3, 5, 2, 1]

print(list(dropwhile(lambda x: x < 5, l)))

print('#' * 52 + '  #### The *compress* function')

data = ['a', 'b', 'c', 'd', 'e']
selectors = [True, False, 1, 0]
print(list(zip(data, selectors)))

print('#' * 52 + '  And only retain the elements where the second value in the tuple is truthy:')

print([item for item, truth_value in zip(data, selectors) if truth_value])

print('#' * 52 + '  The `compress` function works the same way,'
                 '  except that it is evaluated lazily and returns an iterator:')

from itertools import compress

print(list(compress(data, selectors)))
