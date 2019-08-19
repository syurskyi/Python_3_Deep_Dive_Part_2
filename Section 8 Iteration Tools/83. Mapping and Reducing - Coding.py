print('#' * 52 + '  The `map` function applies a given function (that takes a single argument) '
                 '  to an iterable of values and yields (lazily) the result of applying the function '
                 '  to each element of the iterable.')

maps = map(lambda x: x**2, range(5))

print(list(maps))

print('#' * 52 + '  Keep in mind that `map` returns an iterator, so it will become exhausted:')

print(list(maps))

print('#' * 52 + '  Of course, we can supply multiple values to a function by using an iterable of iterables'
                 '  (e.g. tuples) and unpacking the tuple in the function - but we still only use a single argument:')

def add(t):
    return t[0] + t[1]

print(list(map(add, [(0,0), [1,1], range(2,4)])))

print('#' * 52 + '  Remember how we can unpack an iterable into separate positional arguments?')

def add(x, y):
    return x + y

t = (2, 3)
print(add(*t))

print('#' * 52 + '  It would be nice if we could do that with the `map` function as well.')

# list(map(add, [(0,0), (1,1), (2,2)])) # TypeError: add() missing 1 required positional argument: 'y'

print('#' * 52 + '  But of course that is not going to work, since `add` expects two arguments,'
                 '  and only a single one (the tuple) was provided.')
print('#' * 52 + '  This is where `starmap` comes in - it will essentially `*` each element of'
                 '  the iterable before passing it to the function defined in the map:')

from itertools import starmap
print(list(starmap(add, [(0,0), (1,1), (2,2)])))

print('#' * 52 + '  #### Accumulation')
print('#' * 52 + '  You should already know the `sum` function - '
                 '  it simply calculates the sum of all the elements in an iterable:')

print(sum([10, 20, 30]))

from functools import reduce
print(reduce(lambda x, y: x*y, [1, 2, 3, 4]))

print('#' * 52 + '  We can even specify a "start" value:')

print(reduce(lambda x, y: x*y, [1, 2, 3, 4], 10))

print('#' * 52 + '  You will note that with both `sum` and `reduce`,'
                 '  only the final result is shown - none of the intermediate results are available.')
print('#' * 52 + '  Sometimes we want to see the intermediate results as well.')
print('#' * 52 + '  Lets see how we might try it with the `sum` function:|')

def sum_(iterable):
    it = iter(iterable)
    acc = next(it)
    yield acc
    for item in it:
        acc += item
        yield acc

for item in sum_([10, 20, 30]):
    print(item)

print('#' * 52 + '  Of course, this is just going to work for a sum.')
print('#' * 52 + '  We may want the same functionality with arbitrary binary functions,'
                 '  just like `reduce` was more general than `sum')


def running_reduce(fn, iterable, start=None):
    it = iter(iterable)
    if start is None:
        accumulator = next(it)
    else:
        accumulator = start
    yield accumulator

    for item in it:
        accumulator = fn(accumulator, item)
        yield accumulator

print('#' * 52 + '  Lets try a running sum first.')
print('#' * 52 + '  We will use the `operator` module instead of using lambdas.')

import operator

print(list(running_reduce(operator.add, [10, 20, 30])))

print('#' * 52 + '  Now we can also use other binary operators, such as multiplication:')

print(list(running_reduce(operator.mul, [1, 2, 3, 4])))

print('#' * 52 + '  And of course, we can even set a "start" value:')

print(list(running_reduce(operator.mul, [1, 2, 3, 4], 10)))

print('#' * 52 + '  While this certainly works, we really dont need to code this ourselves - that is exactly what'
                 '  the `accumulate` function in `itertools` does for us.')

from itertools import accumulate

print(list(accumulate([10, 20, 30])))

print('#' * 52 + '  We can find the running product of an iterable:')

print(list(accumulate([1, 2, 3, 4], operator.mul)))




