print('#' * 52 + '  ### Making an Iterable from a Generator')


def squares_gen(n):
    for i in range(n):
        yield i ** 2


sq = squares_gen(5)
print(sq)

for num in sq:
    print(num)

print('#' * 52 + '  But, `sq` was an iterator - so now its been exhausted:')

# next(sq)  # StopIteration:

sq = squares_gen(5)

print([num for num in sq])
print('#' * 52 + '  ')

print('#' * 52 + '  So, lets wrap this in an iterable:')


class Squares:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return squares_gen(self.n)


sq = Squares(5)

print([num for num in sq])
print('#' * 52 + '  And we can do it again:')
print([num for num in sq])

print('#' * 52 + '  ')
print('#' * 52 + '  We can put those pieces of code together if we prefer:')


class Squares:
    def __init__(self, n):
        self.n = n

    @staticmethod
    def squares_gen(n):
        for i in range(n):
            yield i ** 2

    def __iter__(self):
        return Squares.squares_gen(self.n)


sq = Squares(5)

print([num for num in sq])

print('#' * 52 + '  #### Generators used with other Generators')

def squares(n):
    for i in range(n):
        yield i ** 2

sq = squares(5)
enum_sq = enumerate(sq)
print(next(sq))
print(next(sq))

print('#' * 52 + '  Since we have consumed two elements from `sq`, when we now use `enumerate`'
                 '  it will have two less elements from sq:')

print(next(enum_sq))