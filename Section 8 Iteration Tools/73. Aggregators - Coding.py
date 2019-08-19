print('#' * 52 + '  We have already used many built-in aggregators.')

def squares(n):
    for i in range(n):
        yield i**2

print(list(squares(5)))

print('#' * 52 + '  We can find the `min` and `max` of elements in an iterable:')

print(min(squares(5)))
print(max(squares(5)))

print('#' * 52 + '  Be careful, all these aggregation functions will **exhaust** any iterator being used.')

sq = squares(5)

print(max(sq))
# print(min(sq))  # ValueError: min() arg is an empty sequence

print('#' * 52 + '  ValueError: min() arg is an empty sequence')

print(list(squares(5)))
print(sum(squares(5)))

print('#' * 52 + '  #### The `any` function')

class Person:
    pass

p = Person()

print(bool(p))

print('#' * 52 + '  For numbers, anything other than `0` is truthy, and strings, lists, tuples,'
                 '  dictionaries, etc are falsy if they are empty.')


class MySeq:
    def __init__(self, n):
        self.n = n

    def __len__(self):
        return self.n

    def __getitem__(self, s):
        pass

my_seq = MySeq(0)
print(bool(my_seq))

my_seq = MySeq(10)
print(bool(my_seq))

print('#' * 52 + '  The `any` function can be used to quickly test if any element is **truthy**:')

print(any([0, '', None]))

print(any([0, '', None, 'hello']))

print('#' * 52 + '  Basically, the `any` function is like doing an `or` between all the elements of the iterable,'
                 '  and casting the result to a Boolean:')

result = 0 or '' or None or 'hello'
print(result, bool(result))

print('#' * 52 + '  #### The `all` Function')

print(all([1, 'abc', [1, 2], range(5)]))
print(all([1, 'abc', [1, 2], range(5), '']))

print('#' * 52 + '  In practice, we often need to test if all elements of an iterable satisfy some criteria,'
                 '  not necessarily whether the elements are truthy or falsy.')
print('#' * 52 + '  Suppose we want to test if an iterable contains only numeric values.')

from numbers import Number

print(isinstance(10, Number), isinstance(10.5, Number))
print(isinstance(2+3j, Number))

print('#' * 52 + '  ')

from decimal import Decimal

print(isinstance(Decimal('10.3'), Number))
print(isinstance(True, Number))

print('#' * 52 + '  On the other hand:')

print(isinstance('100', Number))
print(isinstance([10, 20], Number))

print('#' * 52 + '  Now suppose we have a list (or iterable in general) and we want to see if they are all numbers:')
print('#' * 52 + '  We could proceed with a rather clunky approach this way:')

l = [10, 20, 30, 40]

is_all_numbers = True
for item in l:
    if not isinstance(item, Number):
        is_all_numbers = False
        break
print(is_all_numbers)

l = [10, 20, 30, 40, 'hello']

is_all_numbers = True
for item in l:
    if not isinstance(item, Number):
        is_all_numbers = False
        break
print(is_all_numbers)

print('#' * 52 + '  Now we can actually simplify this a little, by using the `else` clause of the `for`loop - '
                 '  remember that the `else` clause of a `for` loop will execute if the loop terminated normally'
                 '  (i.e. did not `break` out of the loop).')

l = [10, 20, 30, 40, 'hello']
is_all_numbers = False
for item in l:
    if not isinstance(item, Number):
        break
else: # nobreak --> all numbers
    is_all_numbers = True
print(is_all_numbers)

print('#' * 52 + '  We can use the `map` function to apply a function'
                 '  (with a single parameter) to all the elements of an iterable:')

print(map(str, [0, 1, 2, 3, 4]))

print('#' * 52 + '  Now `map` is lazy, so lets put it into a list to see what it contains:')

print(list(map(str, [0, 1, 2, 3, 4])))

print('#' * 52 + '  The function we actually want to use is the `isinstance` function -'
                 '  but that requires **two** parameters - the element we are testing,'
                 '  and the `type` we are testing for.')
print('#' * 52 + '  Somehow we need to create a form of `isinstance` that only requires a single variable'
                 '  and simply holds the type (`Number`) fixed.')

def is_number(x):
    return is_instance(x, Number)

print(lambda x: isinstance(x, Number))

print('#' * 52 + '  So now, lets map that function to our iterable:')

print(l)

print(list(map(lambda x: isinstance(x, Number), l)))
print('#' * 52 + '  And of course, **now** we can use the `all` function to determine'
                 '  if all the elements are numbers or not:')

l = [10, 20, 30, 40, 'hello']
print(all(map(lambda x: isinstance(x, Number), l)))

l = [10, 20, 30, 40]
print(all(map(lambda x: isinstance(x, Number), l)))

print('#' * 52 + '  A lot less typing than the first approach we did!')
print('#' * 52 + '  If you dont like using `map` for some reason, we can easily use a generator expression as well:')

l = [10, 20, 30, 40]
print(all(isinstance(x, Number) for x in l))

l = [10, 20, 30, 40, 'hello']
print(all(isinstance(x, Number) for x in l))

print('#' * 52 + '  Suppose we have a file and we want to make sure'
                 '  that all the rows in the file have length > some number.')

with open('car-brands.txt') as f:
    for row in f:
        print(len(row), row, end='')
        print()
        print()

print('#' * 52 + '  We can easily test to make sure that every brand in our file is at least 3 characters long:')

with open('car-brands.txt') as f:
    result = all(map(lambda row: len(row) >= 3, f))
print(result)

print('#' * 52 + '  And we can test to see if any line is more than 10 characters:')

with open('car-brands.txt') as f:
    result = any(map(lambda row: len(row) > 10, f))
print(result)

print('#' * 52 + '  More than 13?')

with open('car-brands.txt') as f:
    result = any(map(lambda row: len(row) > 13, f))
print(result)

print('#' * 52 + '  Of course, we can also do this using generator expressions instead of `map`:')

with open('car-brands.txt') as f:
    result = any(len(row) > 13 for row in f)
print(result)
