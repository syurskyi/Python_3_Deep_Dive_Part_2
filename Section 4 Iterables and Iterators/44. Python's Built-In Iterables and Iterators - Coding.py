print('#' * 52 + '  Python has a lot of built-in functions that return iterators or iterables.')

r_10 = range(10)

print('__iter__' in dir(r_10))

print('#' * 52 + '  But it is not an **iterator**:')

print('__next__' in dir(r_10))

print('#' * 52 + '  However, we can request an iterator by calling the `__iter__` method,'
                 '  or simply using the `iter()` function:')

r_10_iter = iter(r_10)

print('__iter__' in dir(r_10_iter))
print('__next__' in dir(r_10_iter))


print('#' * 52 + '  Most built-in iterables in Python use lazy evaluation (including the `range`) function - i.e.'
                 '  when we execute `range(10)` Python does no pre-compute a "list" of all the elements in the range.')

print([num for num in range(10)])

print('#' * 52 + '  The `zip` function on the other hand returns an iterator:')

z = zip([1, 2, 3], 'abc')

print(z)

print('#' * 52 + '  It is an **iterator**:')

print('__iter__' in dir(z))
print('__next__' in dir(z))

print('#' * 52 + ' Just like `range()` though, it also uses lazy evaluation,'
                 ' so we need to iterate through the iterator and make a list for example in order to see the contents:')

print(list(z))

print('#' * 52 + '  Even reading a file line by line is done using lazy evaluation:')

with open('cars.csv') as f:
    print(type(f))
    print('__iter__' in dir(f))
    print('__next__' in dir(f))

print('#' * 52 + '  As you can see, the `open()` function returns an **iterator** (of type `TextIOWrapper`),'
                 '  and we can read lines from the file one by one using the `next()` function,'
                 '  or calling the `__next__()` method.')
print('#' * 52 + '  The class also implements a `readline()` method we can use to get the next row:')

with open('cars.csv') as f:
    print(next(f))
    print(f.__next__())
    print(f.readline())

print('#' * 52 + '  Of course we can just iterate over all the lines using a `for` loop as well:')

with open('cars.csv') as f:
    for row in f:
        print(row, end='')

print('#' * 52 + '  The `TextIOWrapper` class also provides a method `readlines()`'
                 '  that will read the entire file and return a list containing all the rows:')

with open('cars.csv') as f:
    l = f.readlines()

print(l)

print('#' * 52 + '  So you might be wondering which method to use? Use the `readlines()` method,'
                 '  or use the iterator methods?')
print('#' * 52 + '  Especially if you ending up reading the entire file - would one method be better than the other?')
print('#' * 52 + '  Consider this example, where we want to find out all the different origins in the file'
                 '  (last column of each row) - lets do this using both approaches.')

origins = set()
with open('cars.csv') as f:
    rows = f.readlines()
for row in rows[2:]:
    origin = row.strip('\n').split(';')[-1]
    origins.add(origin)
print(origins)

origins = set()
with open('cars.csv') as f:
    next(f), next(f)
    for row in f:
        origin = row.strip('\n').split(';')[-1]
        origins.add(origin)
print(origins)

print('#' * 52 + '  The `enumerate` function is another lazy iterator:')

e = enumerate('Python rocks!')

print('__iter__' in dir(e))
print('__next__' in dir(e))

print(iter(e))

print('#' * 52 + '  As we can see, the object and its iterator are the same object.')
print('#' * 52 + '  But `enumerate` is also lazy, so we need to iterate through it in order to recover all the elements:')

print(list(e))

print('#' * 52 + '  Of course, once we have exhausted the iterator, we cannot use it again:')

print(list(e))

print('#' * 52 + '  The dictionary object provides methods that return iterables for the keys,'
                 '  values or tuples of key/value pairs:')

d = {'a': 1, 'b': 2}
keys = d.keys()

print('__iter__' in dir(keys), '__next__' in dir(keys))

print('#' * 52 + '  More simply, we can just test to see if `iter(keys)` **is** the same object as `keys` -'
                 '  if not then we are dealing with an iterable.')

print(iter(keys) is keys)

print('#' * 52 + '  So we have an iterable.')
print('#' * 52 + '  Similarly for `.values()` and `.items()`:')

values = d.values()
print(iter(values) is values)
