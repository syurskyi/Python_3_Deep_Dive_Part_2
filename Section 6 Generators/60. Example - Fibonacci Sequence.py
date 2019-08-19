print('#' * 52 + '  ### Example: Fibonacci Sequence')

def fib_recursive(n):
    if n <= 1:
        return 1
    else:
        return fib_recursive(n-1) + fib_recursive(n-2)

print([fib_recursive(i) for i in range(7)])

print('#' * 52 + '  But this quickly becomes an issue as `n` grows larger:')

from timeit import timeit

print(timeit('fib_recursive(10)', globals=globals(), number=10))
print(timeit('fib_recursive(28)', globals=globals(), number=10))
print(timeit('fib_recursive(29)', globals=globals(), number=10))

print('#' * 52 + '  We can alleviate this by using memoization:')

from functools import lru_cache

@lru_cache()
def fib_recursive(n):
    if n <= 1:
        return 1
    else:
        return fib_recursive(n-1) + fib_recursive(n-2)

print(timeit('fib_recursive(10)', globals=globals(), number=10))
print(timeit('fib_recursive(29)', globals=globals(), number=10))

print('#' * 52 + '  As you can see, performance is greatly improved, but we still have a recursion depth limit:')

@lru_cache()
def fib_recursive(n):
    if n <= 1:
        return 1
    else:
        return fib_recursive(n-1) + fib_recursive(n-2)

# fib_recursive(2000) # RecursionError: maximum recursion depth exceeded while calling a Python object

print('#' * 52 + '  So we can use a non-recursive approach to calculate the `n-th` Fibonacci number:')

def fib(n):
    fib_0 = 1
    fib_1 = 1
    for i in range(n-1):
        fib_0, fib_1 = fib_1, fib_0 + fib_1
    return fib_1

print([fib(i) for i in range(7)])

print('#' * 52 + '  This works well for large `n` values too:')

print(timeit('fib(5000)', globals=globals(), number=10))

print('#' * 52 + '  So now, lets create an iterator approach so we can iterate over the sequence,'
                 '  but without materializing it (i.e. we want to use lazy evaluation, not eager evaluation)')
print('#' * 52 + '  Our first approach is going to be a custom iterator and iterable:')


class Fib:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return self.FibIter(self.n)

    class FibIter:
        def __init__(self, n):
            self.n = n
            self.i = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.i >= self.n:
                raise StopIteration
            else:
                result = fib(self.i)
                self.i += 1
                return result

fib_iterable = Fib(7)

for num in fib_iterable:
    print(num)

print('#' * 52 + '  Of course, we can also use the second form of the `iter` function too,'
                 '  but we have to create a closure first:')

def fib_closure():
    i = 0
    def inner():
        nonlocal i
        result = fib(i)
        i += 1
        return result
    return inner

fib_numbers = fib_closure()
fib_iter = iter(fib_numbers, fib(7))
for num in fib_iter:
    print(num)

print('#' * 52 + '  Instead, we can use a generator function very effectively here.')

def fib(n):
    fib_0 = 1
    fib_1 = 1
    for i in range(n-1):
        fib_0, fib_1 = fib_1, fib_0 + fib_1
    return fib_1

print([fib(i) for i in range(7)])

print('#' * 52 + '  Now lets modity it into a generator function:')

def fib_gen(n):
    fib_0 = 1
    fib_1 = 1
    for i in range(n-1):
        fib_0, fib_1 = fib_1, fib_0 + fib_1
        yield fib_1

print([num for num in fib_gen(7)])

print('#' * 52 + '  Were almost there. Were missing the first two Fibonacci numbers in the sequence -' \
                                          '  we need to yield those too.')

def fib_gen(n):
    fib_0 = 1
    yield fib_0
    fib_1 = 1
    yield fib_1
    for i in range(n-1):
        fib_0, fib_1 = fib_1, fib_0 + fib_1
        yield fib_1

print([num for num in fib_gen(7)])

print('#' * 52 + '  And finally we are returning one number too many if `n`'
                 '  is meant to indicate the length of the sequence:')

def fib_gen(n):
    fib_0 = 1
    yield fib_0
    fib_1 = 1
    yield fib_1
    for i in range(n-2):
        fib_0, fib_1 = fib_1, fib_0 + fib_1
        yield fib_1

print([num for num in fib_gen(7)])

print('#' * 52 + '  Lets time it as well to compare it with the other methods:')

print(timeit('[num for num in Fib(5_000)]', globals=globals(), number=1))

print('#' * 52 + '  ')

fib_numbers = fib_closure()
sentinel = fib(5_001)

print(timeit('[num for num in iter(fib_numbers, sentinel)]', globals=globals(), number=1))

print('#' * 52 + '  ')

print(timeit('[num for num in fib_gen(5_000)]', globals=globals(), number=1))


