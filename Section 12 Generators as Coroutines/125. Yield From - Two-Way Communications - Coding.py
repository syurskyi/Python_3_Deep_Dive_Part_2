def squares(n):
    for i in range(n):
        yield i ** 2

def delegator(n):
    for value in squares(n):
        yield value

gen = delegator(5)
for _ in range(5):
    print(next(gen))

print('#' * 52 + '  Alternatively we could write the same thing this way:')

def delegator(n):
    yield from squares(n)

gen = delegator(5)
for _ in range(5):
    print(next(gen))

print('#' * 52 + '  When we use `yield from subgen` we are **delegating** to `subgen`.')
print('#' * 52 + '  The generator that delegates to the other generator is called the **delegator** and the generator'
                 '  that it delegates to is called the **subgenerator**.')
print('#' * 52 + '  So in our example `squares(n)` was the subgenerator, and `delegator()` was the delegator.')
print('#' * 52 + '  The context that contains the code making `next` calls to the delegator, '
                 '  is called the **callers context**, or simply the **caller**.')
print('#' * 52 + '  ')
print('#' * 52 + '  We will want to inspect the delegator and the subgenerator, so lets import what we will need'
                 '  from the `inspect` module:')

from inspect import getgeneratorstate, getgeneratorlocals

def song():
    yield "I'm a lumberjack and I'm OK"
    yield "I sleep all night and I work all day"

def play_song():
    count = 0
    s = song()
    yield from s
    yield 'song finished'
    print('player is exiting...')

player = play_song()

print(getgeneratorstate(player))
print(getgeneratorlocals(player))

print('#' * 52 + '  As you can see, no local variables have been created in `player` yet - '
                 '  that is because it is created, not actually started.')

print(next(player))
print('#' * 52 + '  Now lets look at the state of things:')

print(getgeneratorstate(player))
print(getgeneratorlocals(player))

print('#' * 52 + '  We can now get a handle to the subgenerator `s`:')

s = getgeneratorlocals(player)['s']

print(getgeneratorstate(s))

print('#' * 52 + '  As we can see the subgenerator is suspended.')

print(next(player))
print(getgeneratorstate(player))
print(getgeneratorstate(s))

print(next(player))
print(getgeneratorstate(player))
print(getgeneratorstate(s))

print('#' * 52 + '  ')

# print(next(player))  #

print('#' * 52 + '  ')

print('#' * 52 + '  We get the `StopIteration` exception because `player` returned, and now both the delegator and'
                 '  the subgenerator are in a closed state:')

print(getgeneratorstate(player))
print(getgeneratorstate(s))

print('#' * 52 + '  Important to note here is that when the subgenerator returned,'
                 '  the delegator **continued running normally**.')
print('#' * 52 + '  Lets make a tweak to our `player` generator to make this even more evident:')

def player():
    count = 1
    while True:
        print('Run count:', count)
        yield from song()
        count += 1

p = player()

print(next(p), next(p))
print('#' * 52 + '  ')
print(next(p), next(p))
print('#' * 52 + '  ')
print(next(p), next(p))


