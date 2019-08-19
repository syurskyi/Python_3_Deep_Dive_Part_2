print('#' * 52 + '  Lets go back to our `Squares` example:')


class Squares:
    def __init__(self, length):
        self.length = length
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.length:
            raise StopIteration
        else:
            result = self.i ** 2
            self.i += 1
            return result


sq = Squares(5)

print(next(sq))
print(next(sq))
print(next(sq))

print('#' * 52 + '  Of course, our iterator still suffers from not being able to "reset" it -'
                 '  we just have to create a new instance:')

sq = Squares(5)

print('#' * 52 + '  But now, we can also use a `for` loop:')

for item in sq:
    print(item)

print('#' * 52 + '  Now `sq` is **exhausted**, so if we try to loop through again:')

for item in sq:
    print(item)

print('#' * 52 + '  All we need to do is create a new iterator:')

sq = Squares(5)

for item in sq:
    print(item)

print('#' * 52 + '  Just like Python s built-in `next` function calls our `__next__` method,'
                 '  Python has a built-in function `iter` which calls the `__iter__` method:')

sq = Squares(5)

print(id(sq))

print(id(sq.__iter__()))

print(id(iter(sq)))

print('#' * 52 + '  And of course we can also use a list comprehension on our iterator object:')

sq = Squares(5)

print([item for item in sq if item % 2 == 0])

print('#' * 52 + '  We can even use any function that requires an iterable as an argument (iterators are iterable):')

sq = Squares(5)
print(list(enumerate(sq)))

print('#' * 52 + '  But of course we have to be careful, our iterator was exhausted, so if try that again:')

print(list(enumerate(sq)))

print('#' * 52 + '  we get an empty list - instead we have to create a new iterator first:')

sq = Squares(5)
print(list(enumerate(sq)))

print('#' * 52 + '  We can even use the `sorted` method on it:')

sq = Squares(5)
print(sorted(sq, reverse=True))

print('#' * 52 + '  #### Python Iterators Summary')

print('#' * 52 + '  The way Python applies a `for` loop to an iterator object is basically what we saw'
                 '  with the `while` loop and the `StopIteration` exception.')

sq = Squares(5)
while True:
    try:
        print(next(sq))
    except StopIteration:
        break

print('#' * 52 + '  In fact we can easily see this by tweaking our iterator a bit:')


class Squares:
    def __init__(self, length):
        self.length = length
        self.i = 0

    def __iter__(self):
        print('calling __iter__')
        return self

    def __next__(self):
        print('calling __next__')
        if self.i >= self.length:
            raise StopIteration
        else:
            result = self.i ** 2
            self.i += 1
            return result


sq = Squares(5)
for i in sq:
    print(i)

print('#' * 52 + '  As you can see Python calls `__next__` (and stops once a `StopIteration` exception is raised).')
print('#' * 52 + '  But you will notice that it also called the `__iter__` method.')
print('#' * 52 + '  In fact we will see this happening in other places too:')

sq = Squares(5)
print([item for item in sq if item % 2 == 0])

print('#' * 52 + '  ')

sq = Squares(5)
print(list(enumerate(sq)))

print('#' * 52 + '  ')

sq = Squares(5)
print(sorted(sq, reverse=True))

print('#' * 52 + '  Why is `__iter__` being called? After all, it just returns itself!')
print('#' * 52 + '  But lets see how we can mimic what Python is doing:')

sq = Squares(5)
sq_iterator = iter(sq)
print(id(sq), id(sq_iterator))
while True:
    try:
        item = next(sq_iterator)
        print(item)
    except StopIteration:
        break

