print('#' * 52 + '  ### Yield From - Closing and Return')


def subgen():
    try:
        while True:
            received = yield
            print(received)
    finally:
        print('subgen: closing...')


def delegator():
    s = subgen()
    yield from s
    yield 'delegator: subgen closed'
    print('delegator: closing...')


d = delegator()
next(d)

print('#' * 52 + '  At this point, both the delegator and the subgenerator are primed and suspended:')

from inspect import getgeneratorstate, getgeneratorlocals

print(getgeneratorlocals(d))

s = getgeneratorlocals(d)['s']
print(getgeneratorstate(d))
print(getgeneratorstate(s))

print('#' * 52 + '  We can send data to the delegator:')

print(d.send('hello'))

print('#' * 52 + '  We can even send data directly to the subgenerator since we now have a handle on it:')

print(s.send('python'))

print('#' * 52 + '  In fact, we can close it too:')

s.close()

print('#' * 52 + '  So, what is the state of the delegator now?')

print(getgeneratorstate(d))

print('#' * 52 + '  But the subgenerator closed, so lets see what happens when we call `next` on `d`:')

print(next(d))

print('#' * 52 + '  As you can see, the generator code resume right after the `yield from`, '
                 '  and we can do this one more time to close the delegator:')

# next(d) #  StopIteration:

print('#' * 52 + '  But what happens if we close the delegator instead of just closing the subgenerator?')

d = delegator()
next(d)
s = getgeneratorlocals(d)['s']
print(getgeneratorstate(d))
print(getgeneratorstate(s))
print(d.close())

print('#' * 52 + '  As you can see the subgenerator also closed. Is the delegator closed too?')

print(getgeneratorstate(d))
print(getgeneratorstate(s))

print('#' * 52 + '  So closing the delegator will close not only the delegator itself,'
                 '  but also close the currently active subgenerator (if any).')
print('#' * 52 + '  We should notice that when we closed the subgenerator directly'
                 '  no apparent exception was raised in our context.')

def subgen():
    try:
        while True:
            received = yield
            print(received)
    finally:
        print('subgen: closing...')
        return 'subgen: return value'

s = subgen()
next(s)
s.send('hello')
s.close()

print('#' * 52 + '   the `StopIteration` exception was silenced.')
print('#' * 52 + '   Lets do this a different way,'
                 '   since we know the `StopIteration` exception should contain the return value:')

s = subgen()
next(s)
s.send('hello')
# s.throw(GeneratorExit, 'force exit') # StopIteration: subgen: return value

print('#' * 52 + '  OK, so now we can see that the `StopIteration` exception contains the return value.')
print('#' * 52 + '  The `yield from` actually captures that value as its return value - '
                 '  in other words `yield from` is not just a statement, it is in fact, '
                 '  like `yield`, also an expression.')

def subgen():
    try:
        yield 1
        yield 2
    finally:
        print('subgen: closing...')
        return 100

def delegator():
    s = subgen()
    result = yield from s
    print('subgen returned:', result)
    yield 'delegator suspended'
    print('delegator closing')

d = delegator()

print(next(d))
print(next(d))
print(next(d))
