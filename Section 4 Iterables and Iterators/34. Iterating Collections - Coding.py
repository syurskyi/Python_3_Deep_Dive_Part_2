s = {'x', 'y', 'b', 'c', 'a'}
for item in s:
    print(item)

print('#' * 52 + '   we cannot use indexing to access elements in a set')

# s[0] # TypeError: 'set' object does not support indexing

print('#' * 52 + '  ')


class Squares:
    def __init__(self):
        self.i = 0

    def next_(self):
        result = self.i ** 2
        self.i += 1
        return result

sq = Squares()

print(sq.next_())
print(sq.next_())
print(sq.next_())

print('#' * 52 + '  How do we re-start the iteration from the beginning?')
print('#' * 52 + '  We cant - we have to create a new instance of `Squares`:')

sq = Squares()
for i in range(10):
    print(sq.next_())

print('#' * 52 + '  We even are able to iterate over the squares.')
print('#' * 52 + '  We will even implement a `__len__` method to support the `len()` function:')


class Squares:
    def __init__(self, length):
        self.length = length
        self.i = 0

    def next_(self):
        if self.i >= self.length:
            raise StopIteration
        else:
            result = self.i ** 2
            self.i += 1
            return result

    def __len__(self):
        return self.length

sq = Squares(3)

print(len(sq))

print(sq.next_())
print(sq.next_())
print(sq.next_())

# print(sq.next_()) # StopIteration:

print('#' * 52 + '  So now, we can essentially loop over the collection in a very similar way to how we did it'
                 '  with sequences and the `__getitem__` method:')


sq = Squares(5)
while True:
    try:
        print(sq.next_())
    except StopIteration:
        # reached end of iteration
        # stop looping
        break

print('#' * 52 + '  There are two issues here.')

# print(sq.next_()) # StopIteration:

print('#' * 52 + '  The second problem is that we cant use a `for` loop - '
                 '  Python does not know about our `next_()` method:')

# for i in Squares(10):  # TypeError: 'Squares' object is not iterable
#     print(i)


print('#' * 52 + '  Much like Python s `len()` function and the `__len__()` method,'
                 '  Python has a built-in `next()` function - it calls the `__next__()`'
                 '  method in our class if there is one.')


class Squares:
    def __init__(self, length):
        self.length = length
        self.i = 0

    def __next__(self):
        if self.i >= self.length:
            raise StopIteration
        else:
            result = self.i ** 2
            self.i += 1
            return result

    def __len__(self):
        return self.length

sq = Squares(3)
print(next(sq))
print(next(sq))
print(next(sq))

# print(next(sq)) # StopIteration:

print('#' * 52 + '  So that s nice, makes typing a bit easier -'
                 '  our loop we wrote earlier would look something like this now:')

sq = Squares(5)
while True:
    try:
        print(next(sq))
    except StopIteration:
        break

print('#' * 52 + '  You will notice that technically our `Squares` class could be built as a sequence type -'
                 '  it was just a very simple example.')

import random


class RandomNumbers:
    def __init__(self, length, *, range_min=0, range_max=10):
        self.length = length
        self.range_min = range_min
        self.range_max = range_max
        self.num_requested = 0

    def __len__(self):
        return self.length

    def __next__(self):
        if self.num_requested >= self.length:
            raise StopIteration
        else:
            self.num_requested += 1
            return random.randint(self.range_min, self.range_max)

print('#' * 52 + '  We can now iterate over instances of this object:')

numbers = RandomNumbers(10)
print(len(numbers))

while True:
    try:
        print(next(numbers))
    except StopIteration:
        break

print('#' * 52 + '  We still cannot use a `for` loop, and if we want to restart the iteration,'
                 '  we have to create a new object every time.')

numbers = RandomNumbers(10)

# for item in numbers:
#     print(item)     # TypeError: 'RandomNumbers' object is not iterable