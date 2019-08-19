print('#' * 52 + '  ### Yield From - Throwing Exceptions')


class CloseCoroutine(Exception):
    pass


def echo():
    try:
        while True:
            received = yield
            print(received)
    except CloseCoroutine:
        return 'coro was closed'
    except GeneratorExit:
        print('closed method was called')


e = echo()
next(e)

# e.throw(CloseCoroutine, 'just closing') # StopIteration: coro was closed

e = echo()
next(e)
e.close()

print('#' * 52 + '  As we can see the difference between `throw` and `close` is that although `close` causes '
                 '  an exception to be raised in the generator, Python essentially silences it.')

print('#' * 52 + '  It works the same way when we delegate to the coroutine in a delegator:')


def delegator():
    result = yield from echo()
    yield 'subgen closed and returned:', result
    print('delegator closing...')


d = delegator()
next(d)
d.send('hello')

print(d.throw(CloseCoroutine))

print('#' * 52 + '  Now what happens if the `throw` in the subgenerator does not close subgenerator'
                 '  but instead silences the exception and yields a value instead?')


class CloseCoroutine(Exception):
    pass


class IgnoreMe(Exception):
    pass


def echo():
    try:
        while True:
            try:
                received = yield
                print(received)
            except IgnoreMe:
                yield "I'm ignoring you..."
    except CloseCoroutine:
        return 'coro was closed'
    except GeneratorExit:
        print('closed method was called')

d = delegator()
next(d)

d.send('python')

result = d.throw(IgnoreMe, 1000)

print(result)

print(d.send('rocks!'))
d.close()

print('#' * 52 + '  ')
print('#' * 52 + '  ')
print('#' * 52 + '  ')

def echo():
    try:
        output = None
        while True:
            try:
                received = yield output
                print(received)
            except IgnoreMe:
                output = "I'm ignoring you..."
            else:
                output = None
    except CloseCoroutine:
        return 'coro was closed'
    except GeneratorExit:
        print('closed method was called')

d = delegator()
next(d)

print(d.send('hello'))
print(d.throw(IgnoreMe))
print(d.send('python'))
d.close()

print('#' * 52 + '  ppens if we do not handle the error in the subgenerator and simply let the exception propagate up?')
print('#' * 52 + '  Who gets the exception, the delegator, or the caller?')

def echo():
    while True:
        received = yield
        print(received)

def delegator():
    yield from echo()

d = delegator()
next(d)

# d.throw(ValueError) # ValueError:

print('#' * 52 + '  OK, so we, the caller see the exception.')
print('#' * 52 + '  But did the delegator see it too? i.e. can we catch the exception in the delegator?')

def delegator():
    try:
        yield from echo()
    except ValueError:
        print('got the value error')

d = delegator()
next(d)

# d.throw(ValueError) # StopIteration:

print('#' * 52 + '  #### Example')

print('#' * 52 + '  Suppose we have a coroutine that creates running averages, '
                 '  and we want to occasionally write the current data to a file:')

class WriteAverage(Exception):
    pass

def averager(out_file):
    total = 0
    count = 0
    average = None
    with open(out_file, 'w') as f:
        f.write('count,average\n')
        while True:
            try:
                received = yield average
                total += received
                count += 1
                average = total / count
            except WriteAverage:
                if average is not None:
                    print('saving average to file:', average)
                    f.write(f'{count},{average}\n')

avg = averager('sample.csv')
next(avg)

print(avg.send(1))
print(avg.send(2))

print(avg.throw(WriteAverage))

print(avg.send(3))
print(avg.send(2))
print(avg.throw(WriteAverage))

avg.close()

print('#' * 52 + '  Now we can read the data back and make sure it worked as expected:')

with open('sample.csv') as f:
    for row in f:
        print(row.strip())

print('#' * 52 + '  Of course we can use a delegator as well.')
print('#' * 52 + '  Maybe the delegator is charged with figuring out the output file name.')
print('#' * 52 + '  Here we will just hardcode it inside the delegator')

def delegator():
    yield from averager('sample.csv')

d = delegator()
next(d)

print(d.send(1))
print(d.send(2))
print(d.send(3))
print(d.send(4))

print(d.throw(WriteAverage))

print(d.send(5))
print(d.throw(WriteAverage))

d.close()

with open('sample.csv') as f:
    for row in f:
        print(row.strip())

