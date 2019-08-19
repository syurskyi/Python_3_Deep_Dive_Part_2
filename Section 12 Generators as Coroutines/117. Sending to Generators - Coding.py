print('#' * 52 + '  ### Sending data to Generators')

def echo():
    while True:
        received = yield
        print('You said:', received)

e = echo()

from inspect import getgeneratorstate

print(getgeneratorstate(e))
print(next(e))

print(getgeneratorstate(e))

print(e.send('python'))

print('#' * 52 + '  And now the generator continued running until it hit a `yield` again - '
                 '  which it does since we have our yield inside an infinite loop:')

print(e.send('I said'))

print('#' * 52 + '  So, the `send` method essentially resume the generator just as the `__next__` does - '
                 '  but it also sends in some data that we can capture if we want to, inside the generator.')
print('#' * 52 + '  What happens if we do call `next()` or `__next__` instead of `send()`?')
print('#' * 52 + '  The same as if we had sent the `None` value:')

print(next(e))
print(e.send(None))

print('#' * 52 + '  You might be asking whether we could have used `send` with all the generators'
                 '  we had written so far - sure!')
print('#' * 52 + '  The `yield` keyword is an expression, and you dont have to '
                 '  assign the result of an expression to a variable:')

print(10 < 100)

print('#' * 52 + '  That was an expression, and it was perfectly fine not to assign it to a variable.')

def squares(n):
    for i in range(n):
        yield i**2

sq = squares(5)

print(next(sq))
print(sq.send(100))
print(sq.send(100))

print('#' * 52 + '  Now, the only thing is that we cannot change a generator from `created` to `suspended`'
                 '  using the `send()` function - we **have** to call `next` first.')
print('#' * 52 + '  In other words this will not work:')

e = echo()
# print(e.send('hello')) #  TypeError: can't send non-None value to a just-started generator

print('#' * 52 + '  We need to **start** or **prime** the generator first, using, `next` which will run the code'
                 '  until the `yield` expression is encountered.')

print(next(e))
print(e.send('hello'))

print('#' * 52 + '  At this point we can see that generators can be used to both send and receive data.')
print('#' * 52 + '  You might be asking yourself whether it is possible to do both **at the same time** - '
                 '  i.e. use ` yield` to both yield data and receive data (upon resumption).')
print('#' * 52 + '  The answer is yes, but its kind of mind bending, and unless you actually need to do so, '
                 '  resist the temptation to do it - it can be extremely confusing:')

def squares(n):
    for i in range(n):
        received = yield i ** 2
        print('received:', received)

sq = squares(5)
print(next(sq))

yielded = sq.send('hello')
print('yielded:', yielded)

yielded = sq.send('hello')
print('yielded:', yielded)

print('#' * 52 + '  Of course, once the generator no longer `yields`, but `returns` we will get'
                 '  the same `StopIteration` exception:')

def echo(max_times):
    for i in range(max_times):
        received = yield
        print('You said:', received)
    print("that's all, folks!")

e = echo(3)
print(next(e))

e.send('python')
e.send('is')

print('#' * 52 + '  The next `send` is going to resume the generator, it will print what we send it,'
                 '  and continue running - but this time the loop is done,')
print('#' * 52 + '  so it will print our final `that is all, folks`,'
                 '  and the function will return (`None`) and hence cause a `StopIteration` exception to be raised:')

# e.send('awesome')  # StopIteration:

print('#' * 52 + '  Consider this example where we want a generator/coroutine that maintains (and yields)'
                 '  a running average of values we send it.')
print('#' * 52 + '  Lets first see how we would do it without using a coroutine -'
                 '  instead we will use a closure so we can maintain the state (`total` and `count`):')

def averager():
    total = 0
    count = 0
    def inner(value):
        nonlocal total
        nonlocal count
        total += value
        count += 1
        return total / count
    return inner

def running_averages(iterable):
    avg = averager()
    for value in iterable:
        running_average = avg(value)
        print(running_average)

print(running_averages([1, 2, 3, 4]))

print('#' * 52 + '  And now the same, but using a coroutine:')

def running_averager():
    total = 0
    count = 0
    running_average = None
    while True:
        value = yield running_average
        total += value
        count += 1
        running_average = total / count

def running_averages(iterable):
    averager = running_averager()
    next(averager)  # prime generator
    for value in iterable:
        running_average = averager.send(value)
        print(running_average)

print(running_averages([1, 2, 3, 4]))