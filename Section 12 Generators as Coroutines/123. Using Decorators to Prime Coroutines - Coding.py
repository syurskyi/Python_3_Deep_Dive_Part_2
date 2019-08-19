### Using decorators to prime coroutines


def coroutine(gen_fn):
    def inner():
        gen = gen_fn()
        next(gen)
        return gen
    return inner

@coroutine
def echo():
    while True:
        received = yield
        print(received)

ec = echo()

import inspect
print(inspect.getgeneratorstate(ec))

print('#' * 52 + '  As you can see our generator was automatically advanced from CREATED to SUSPENDED -'
                 '  and we can now use it straight away:')

ec.send('hello')

print('#' * 52 + '  Now, we still need to expand this slightly to accomodate passing arguments'
                 '  to our generator function (coroutine):')

def coroutine(gen_fn):
    def inner(*args, **kwargs):
        gen = gen_fn(*args, **kwargs)
        next(gen)
        return gen
    return inner

import math

@coroutine
def power_up(p):
    result = None
    while True:
        received = yield result
        result = math.pow(received, p)

squares = power_up(2)
cubes = power_up(3)

print(squares.send(2))
print(cubes.send(2))

print('#' * 52 + '  What happens if we send the wrong type in?')


# squares.send('abc') # TypeError: must be real number, not str

print('#' * 52 + '  And now our generator stops functioning, it is in a closed state:')

print(inspect.getgeneratorstate(squares))

print('#' * 52 + ' In this particular case, we dont want our generator to close down - '
                 ' it should simply yield None and ignore the exception, so it can continue working:')

@coroutine
def power_up(p):
    result = None
    while True:
        received = yield result
        try:
            result = math.pow(received, p)
        except TypeError:
            result = None

squares = power_up(2)
print(squares.send(2))
squares.send('abc')
print(squares.send(3))

print('#' * 52 + '  Of course, we can close the generator ourselves still:')

squares.close()
print(inspect.getgeneratorstate(squares))
