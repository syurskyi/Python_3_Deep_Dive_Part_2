print(
    '#' * 52 + '  As we have seen before, the `iter()` function is used to request an iterator object from an iterable.')

l = [1, 2, 3, 4]

l_iter = iter(l)

print(type(l_iter))

print('#' * 52 + '  And we can use that iterator to iterate the collection by calling `next()`'
                 '  until a `StopIteration` exception is raised.')

print(next(l_iter))
print(next(l_iter))

print('#' * 52 + '  We also saw how sequence types are also iterable even though they are not actual iterables -'
                 '  they do not have an `__iter__` method, but instead they have a `__getitem__` method.')
print('#' * 52 + '  Python had no problem iterating a sequence object - in fact behind the scenes'
                 '  an iterator is built by Python in order to iterate using the `__getitem__` method:')


class Squares:
    def __init__(self, n):
        self._n = n

    def __len__(self):
        return self._n

    def __getitem__(self, i):
        if i >= self._n:
            raise IndexError
        else:
            return i ** 2


sq = Squares(5)

for i in sq:
    print(i)

sq_iter = iter(sq)

print('#' * 52 + '  And we now have an iterator for `sq`!')

print(type(sq_iter))
print('__next__' in dir(sq_iter))

print('#' * 52 + '  What happens is that Python will first try to get the iterator by invoking the `__iter__`'
                 '  method on our object.')
print('#' * 52 + '  If it does not have that method, it will look for `__getitem__` next - '
                 '  if its there it will create an iterator for us that will leverage `__getitem__` '
                 '  and the fact that sequence indices should start at 0.')
print('#' * 52 + '  If neither `__iter__` nor `__getitem__` are found, then we will get an exception such as this one:')

# for i in 10:
#     print(i) # TypeError: 'int' object is not iterable

print('#' * 52 + '  ')
print('#' * 52 + '  ')
print('#' * 52 + '  Here is how we might build an iterator using the `__getitem__` method ourselves -'
                 '  not that we have to do that since Python does it for us.')


class Squares:
    def __init__(self, n):
        self._n = n

    def __len__(self):
        return self._n

    def __getitem__(self, i):
        if i >= self._n:
            raise IndexError
        else:
            return i ** 2


class SquaresIterator:
    def __init__(self, squares):
        self._squares = squares
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._i >= len(self._squares):
            raise StopIteration
        else:
            result = self._squares[self._i]
            self._i += 1
            return result


sq = Squares(5)
sq_iterator = SquaresIterator(sq)

print(type(sq_iterator))
print('#' * 52 + '  ')
print(next(sq_iterator))
print(next(sq_iterator))
print(next(sq_iterator))
print(next(sq_iterator))
print(next(sq_iterator))

print('#' * 52 + '  The iterator is now exhausted, so:')

# print(next(sq_iterator)) # StopIteration:

print('#' * 52 + '  Technically, we dont actually need to implement the `__len__` method in our sequence type,'
                 '  but since we are using it in our iterator, we will have to think of something else - '
                 '  we can leverage the fact that the sequence will raise an IndexError if the index is out of bounds:')


class SquaresIterator:
    def __init__(self, squares):
        self._squares = squares
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self._squares[self._i]
            self._i += 1
            return result
        except IndexError:
            raise StopIteration()


sq_iterator = SquaresIterator(sq)

for i in sq_iterator:
    print(i)

print('#' * 52 + '  #### How to test if an object is iterable')


class SimpleIter:
    def __init__(self):
        pass

    def __iter__(self):
        return 'Nope'


s = SimpleIter()
print('__iter__' in dir(s))

print('#' * 52 + '  However, if we call `iter()` on `SimpleIter`, look at what happens:')

# print(iter(s))  # TypeError: iter() returned non-iterator of type 'str'

print('#' * 52 + '  So the best way, if you have some need to detect if something is iterable or not, is the following:')

def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

print(is_iterable(SimpleIter()))
print(is_iterable(Squares(5)))