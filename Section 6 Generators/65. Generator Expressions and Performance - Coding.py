print('#' * 52 + '  Recall how list comprehensions worked:')

l = [i ** 2 for i in range(5)]

print(l)

print('#' * 52 + '  We can easily create a **generator** by using `()` parentheses instead of the `[]` brackets:')

g = (i ** 2 for i in range(5))

print('#' * 52 + '  Note that `g` is a generator, and is also lazily evaluated:')

print(type(g))

for item in g:
    print(item)

print('#' * 52 + '  And now the generator has been exhausted:')

for item in g:
    print(item)

print('#' * 52 + '  Scoping works the same way with generator expressions as with list comprehensions,')
print('#' * 52 + '  generator expressions are created by Python using a function, and therefore have local scopes'
                 '  and can access enclosing nonlocal and global scopes.')

import dis

exp = compile('[i**2 for i in range(5)]', filename='<string>', mode='eval')
dis.dis(exp)
print('#' * 52 + '  ')

exp = compile('(i ** 2 for i in range(5))', filename='<string>', mode='eval')
dis.dis(exp)

print('#' * 52 + '  We can iterate over the same list comprehension multiple times, since it is an iterable.')
print('#' * 52 + '  However, we can only iterate over a comprehension expression once, since it is an iterator.')

l = [i * 2 for i in range(5)]
print(type(l))

g = (i ** 2 for i in range(5))

print(type(g))

print('#' * 52 + '  Using a list comprehension ')

start = 1
stop = 10

mult_list = [[i * j
              for j in range(start, stop + 1)]
             for i in range(start, stop + 1)]

print(mult_list)

print('#' * 52 + '  The equivalent generator expression would be:')

start = 1
stop = 10

mult_list = ((i * j
              for j in range(start, stop + 1))
             for i in range(start, stop + 1))

print(mult_list)
print('#' * 52 + '  We can iterate through mult_list:')

table = list(mult_list)
print(table)

print('#' * 52 + '  But you will notice that our rows are themselves generators!')
print('#' * 52 + '  To fully materialize the table we need to iterate through the row generators too:')

table_rows = [list(gen) for gen in table]

print(table_rows)

print('#' * 52 + '  Of course, we can mix list comprehensions and generators. ')
print('#' * 52 + '  In this modification, we will make the rows list comprehensions,'
                 '  and retain the generator expression in the outer comprehension:')

start = 1
stop = 10

mult_list = ([i * j
              for j in range(start, stop + 1)]
             for i in range(start, stop + 1))

for item in mult_list:
    print(item)

print('#' * 52 + '  Lets try Pascals triangle again:')

from math import factorial


def combo(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))


size = 10  # global variable
pascal = [[combo(n, k) for k in range(n + 1)] for n in range(size + 1)]

print(pascal)

print('#' * 52 + '  We can now use generator expressions for either one or both of the nested list comprehensions. '
                 '  In this case I will use it for both:')

size = 10  # global variable
pascal = ((combo(n, k) for k in range(n + 1)) for n in range(size + 1))

print([list(row) for row in pascal])

print('#' * 52 + '  #### Timings')

from timeit import timeit

size = 600

print(timeit('[[combo(n, k) for k in range(n+1)] for n in range(size+1)]', globals=globals(), number=1))
print(timeit('((combo(n, k) for k in range(n+1)) for n in range(size+1))', globals=globals(), number=1))
print(timeit('([combo(n, k) for k in range(n+1)] for n in range(size+1))', globals=globals(), number=1))

print('#' * 52 + '  In fact, we can quickly create a **huge** Pascal triangle using the generator approach:')

size = 100_000

print(timeit('([combo(n, k) for k in range(n+1)] for n in range(size+1))', globals=globals(), number=1))

print('#' * 52 + '  What about timing both creating **and** iterating though all the elements?')


def pascal_list(size):
    l = [[combo(n, k) for k in range(n + 1)] for n in range(size + 1)]
    for row in l:
        for item in row:
            pass


def pascal_gen(size):
    g = ((combo(n, k) for k in range(n + 1)) for n in range(size + 1))
    for row in g:
        for item in row:
            pass


size = 600
print(timeit('pascal_list(size)', globals=globals(), number=1))

print('#' * 52 + '  ')

size = 600
timeit('pascal_gen(size)', globals=globals(), number=1)

print('#' * 52 + '  #### Memory Usage')

import tracemalloc

def pascal_list(size):
    l = [[combo(n, k) for k in range(n+1)] for n in range(size+1)]
    for row in l:
        for item in row:
            pass
    stats = tracemalloc.take_snapshot().statistics('lineno')
    print(stats[0].size, 'bytes')

def pascal_gen(size):
    g = ((combo(n, k) for k in range(n+1)) for n in range(size+1))
    for row in g:
        for item in row:
            pass
    stats = tracemalloc.take_snapshot().statistics('lineno')
    print(stats[0].size, 'bytes')

tracemalloc.stop()
tracemalloc.clear_traces()
tracemalloc.start()
print(pascal_list(300))

print('#' * 52 + '  ')

tracemalloc.stop()
tracemalloc.clear_traces()
tracemalloc.start()
pascal_gen(300)

