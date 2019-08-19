print('#' * 52 + '  Lets write a simple coroutine that will receive string data and'
                 '  print the reversed string to the console:')


def echo():
    while True:
        received = yield
        print(received[::-1])


e = echo()
print(next(e))  # prime the coroutine

e.send('stressed')
e.send('tons')

print('#' * 52 + '  And we can close the generator:')

e.close()

print('#' * 52 + '  Now lets write a simple delegator generator:')


def delegator():
    e = echo()
    yield from e


d = delegator()
print(next(d))

print('#' * 52 + '  Now, calling `next` on the delegator will establish the connection to the subgenerator and'
                 '  automatically prime it as well.')

from inspect import getgeneratorstate, getgeneratorlocals

print(getgeneratorlocals(d))
e = getgeneratorlocals(d)['e']

print(getgeneratorstate(d))
print(getgeneratorstate(e))

print('#' * 52 + '  We can now send data to the delegator, and it will pass that along to the subgenerator:')

print(d.send('stressed'))

print('#' * 52 + 'Lets modify our `echo` coroutine to both receive and yield a result, instead of just printing to the console:' )

def echo():
    output = None
    while True:
        received = yield output
        output = received[::-1]

e = echo()
next(e)

print(e.send('stressed'))

print('#' * 52 + '  And we can use delegation as follows:')

def delegator():
    yield from echo()

d = delegator()
next(d)

print(d.send('stressed'))

print('#' * 52 + '  Let s take a look at a more interesting example of `yield from`.')

l = [1, 2, [3, 4, [5, 6]], [7, [8, 9, 10]]]

def flatten(curr_item):
    if isinstance(curr_item, list):
        for item in curr_item:
            flatten(item)
    else:
        print(curr_item)

flatten(l)

print('#' * 52 + '  Now lets create a flattened list instead of just printing the results:')

def flatten(curr_item, output):
    if isinstance(curr_item, list):
        for item in curr_item:
            flatten(item, output)
    else:
        output.append(curr_item)

output = []
flatten(l, output)
print(output)

print('#' * 52 + '  This is not too bad to understand, but lets try it using generators and `yield from`:')

def flatten_gen(curr_item):
    if isinstance(curr_item, list):
        for item in curr_item:
            yield from flatten_gen(item)
    else:
        yield curr_item

for item in flatten_gen(l):
    print(item)

print('#' * 52 + '  And of course we can, if we prefer, make a list out of it:')

print(list(flatten_gen(l)))

print('#' * 52 + '  Technically we can expand this to cover any iterable types - not just lists:')

def is_iterable(item):
    try:
        iter(item)
    except:
        return False
    else:
        return True

def flatten_gen(curr_item):
    if is_iterable(curr_item):
        for item in curr_item:
            yield from flatten_gen(item)
    else:
        yield curr_item

l = [1, 2, (3, 4, {5, 6}), (7, 8, [9, 10])]

print(list(flatten_gen(l)))

print('#' * 52 + '  But there is potentially a slight wrinkle - strings:')

l = ['abc', [1, 2, (3, 4)]]

# print(list(flatten_gen(l))) # RecursionError: maximum recursion depth exceeded

print('#' * 52 + '  Why are we getting this recursion error?')
print('#' * 52 + '  That is because strings are iterables too - even a single character string!')
print('#' * 52 + '  So, two issues: we may not want to treat strings as iterables, and if we do, '
                 '  then we need to be careful with single character strings.')
print('#' * 52 + '  We are going to tweak our `is_iterable` function, and our `flatten` generator to handle '
                 '  these two issues:')

def is_iterable(item, *, str_is_iterable=True):
    try:
        iter(item)
    except:
        return False
    else:
        if isinstance(item, str):
            if str_is_iterable and len(item) > 1:
                return True
            else:
                return False
        else:
            return True

print(is_iterable([1, 2, 3]))
print(is_iterable('abc'))
print(is_iterable('a'))

print('#' * 52 + '  ')

print(is_iterable([1, 2, 3], str_is_iterable=False))
print(is_iterable('abc', str_is_iterable=False))
print(is_iterable('a', str_is_iterable=False))

print('#' * 52 + '  Good, now we can tweak our `flatten` generator'
                 '  so we can tell it whether to handle strings as iterables or not:')

def flatten_gen(curr_item, *, str_is_iterable=True):
    if is_iterable(curr_item, str_is_iterable=str_is_iterable):
        for item in curr_item:
            yield from flatten_gen(item, str_is_iterable=str_is_iterable)
    else:
        yield curr_item

print(l)
print(list(flatten_gen(l)))
print(list(flatten_gen(l, str_is_iterable=False)))

print('#' * 52 + '  Here we saw we could use `yield from` recursively.'
                 '  In fact a generator can be both a delegator and a subgenerator.')

def coro():
    while True:
        received = yield
        print(received)

def gen1():
    yield from gen2()


def gen2():
    yield from gen3()


def gen3():
    yield from coro()

g = gen1()
next(g)
print(g.send('hello'))
