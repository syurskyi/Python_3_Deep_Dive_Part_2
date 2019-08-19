print('#' * 52 + '  In this example we are going to create a counter function (using a closure)')
print('#' * 52 + '  - its a pretty simplistic function - `counter()` will return a closure')
print('#' * 52 + '  that we can then call to increment an internal counter by `1` every time it is called:')


def counter():
    i = 0

    def inc():
        nonlocal i
        i += 1
        return i

    return inc


print('#' * 52 + '  This function allows us to create a simple counter, which we can use as follows:')

cnt = counter()
print(cnt())
print(cnt())

print('#' * 52 + '  Technically we can make an iterator to iterate over this counter:')


class CounterIterator:
    def __init__(self, counter_callable):
        self.counter_callable = counter_callable

    def __iter__(self):
        return self

    def __next__(self):
        return self.counter_callable()


print('#' * 52 + '  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('#' * 52 + '  Do note that this is an **infinite** iterable!')
print('#' * 52 + '  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

cnt = counter()
cnt_iter = CounterIterator(cnt)
for _ in range(5):
    print(next(cnt_iter))

print('#' * 52 + '  So basically we were able to create an **iterator** from some arbitrary callable.')
print('#' * 52 + '  But one issue is that we have an **inifinite** iterable.')
print('#' * 52 + '  One way around this issue, would be to specify a "stop" value when the iterator'
                 '  should decide to end the iteration.')


class CounterIterator:
    def __init__(self, counter_callable, sentinel):
        self.counter_callable = counter_callable
        self.sentinel = sentinel

    def __iter__(self):
        return self

    def __next__(self):
        result = self.counter_callable()
        if result == self.sentinel:
            raise StopIteration
        else:
            return result


print('#' * 52 + '  Now we can essentially provide a value that if returned from the callable will result in'
                 '  a `StopIteration` exception, essentially terminating the iteration:')

cnt = counter()
cnt_iter = CounterIterator(cnt, 5)
for c in cnt_iter:
    print(c)

print('#' * 52 + '  Now there is technically an issue here: the cnt_iter is still "alive" -'
                 '  our iterator raised a `StopIteration` exception, but if we call it again,'
                 '  it will happily resume from where it left off!')

print(next(cnt_iter))

print('#' * 52 + '  We really should make sure the iterator has been consumed, so lets fix that:')


class CounterIterator:
    def __init__(self, counter_callable, sentinel):
        self.counter_callable = counter_callable
        self.sentinel = sentinel
        self.is_consumed = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.is_consumed:
            raise StopIteration
        else:
            result = self.counter_callable()
            if result == self.sentinel:
                self.is_consumed = True
                raise StopIteration
            else:
                return result


print('#' * 52 + '  Now it should behave as a normal iterator that cannot continue iterating once'
                 '  the first `StopIteration` exception has been raised:')

cnt = counter()
cnt_iter = CounterIterator(cnt, 5)
for c in cnt_iter:
    print(c)

# next(cnt_iter) # StopIteration:

print('#' * 52 + '  Lets see the help on `iter`:')

help(iter)

print('#' * 52 + '  As we can see `iter` has a second form, that takes in a callable and a sentinel value.')
print('#' * 52 + '  And it will result in exactly what we have been doing,'
                 '  but without having to create the iterator class ourselves!')

cnt = counter()
cnt_iter = iter(cnt, 5)
for c in cnt_iter:
    print(c)

# next(cnt_iter) # StopIteration:

print('#' * 52 + '  Both of these approaches can be made to work with any callable.')
print('#' * 52 + '  For example, you may want to iterater through random numbers until'
                 '  a specific random number is generated:')

import random

random.seed(0)
for i in range(10):
    print(i, random.randint(0, 10))

print('#' * 52 + '  As you can see in this example (I set my seed to 0 to have repeatable results),'
                 '  the number `8` is reached at the `5`th iteration.')

random_iterator = iter(lambda: random.randint(0, 10), 8)

random.seed(0)

for num in random_iterator:
    print(num)

print('#' * 52 + '  Lets try a countdown example like the one we discussed in the lecture.')
print('#' * 52 + '  We will use a closure to get our countdown working')


def countdown(start=10):
    def run():
        nonlocal start
        start -= 1
        return start

    return run


takeoff = countdown(10)
for _ in range(15):
    print(takeoff())

print('#' * 52 + '  So the countdown function works,'
                 '  but we would like to be able to iterate over it and stop the iteration once we reach 0.')

takeoff = countdown(10)
takeoff_iter = iter(takeoff, -1)

for val in takeoff_iter:
    print(val)