class CyclicIterator:
    def __init__(self, lst):
        self.lst = lst
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        result = self.lst[self.i % len(self.lst)]
        self.i += 1
        return result


iter_cycl = CyclicIterator('NSWE')

for i in range(10):
    print(next(iter_cycl))

print('#' * 52 + '  So, now we can tackle our original problem:')

n = 10
iter_cycl = CyclicIterator('NSWE')
for i in range(1, n + 1):
    direction = next(iter_cycl)
    print(f'{i}{direction}')

print('#' * 52 + '  And re-working this into a list comprehension:')

n = 10
iter_cycl = CyclicIterator('NSWE')
print([f'{i}{next(iter_cycl)}' for i in range(1, n + 1)])

print('#' * 52 + '  We need to repeat the array [N, S, W, E] for as many times as we have elements in our range'
                 '  of integers - we can even create way more than we need - because when we `zip` it up'
                 '  with the range of integers, the smallest length iterable will be used:')

n = 10
print(list(zip(range(1, n + 1), 'NSWE' * (n // 4 + 1))))

print([f'{i}{direction}'
       for i, direction in zip(range(1, n + 1), 'NSWE' * (n // 4 + 1))])

print('#' * 52 + '  There is actually an even easier way yet, and that is to use our `CyclicIterator`,'
                 '  but instead of building it ourselves, we can simply use the one provided by Python'
                 '  in the standard library!!')

import itertools

n = 10
iter_cycl = CyclicIterator('NSWE')
print([f'{i}{next(iter_cycl)}' for i in range(1, n + 1)])

print('#' * 52 + '  and using itertools:')

n = 10
iter_cycl = itertools.cycle('NSWE')
print([f'{i}{next(iter_cycl)}' for i in range(1, n+1)])