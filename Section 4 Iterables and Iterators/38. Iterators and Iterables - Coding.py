print('#' * 52 + '  Lets start with a simple example that has those issues:')


class Cities:
    def __init__(self):
        self._cities = ['Paris', 'Berlin', 'Rome', 'Madrid', 'London']
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._cities):
            raise StopIteration
        else:
            item = self._cities[self._index]
            self._index += 1
            return item


print('#' * 52 + '  Now, we have an **iterator** object, but we need to re-create it every time we want to start'
                 '  the iterations from the beginning:')

cities = Cities()
print(list(enumerate(cities)))

cities = Cities()
print([item.upper() for item in cities])

cities = Cities()
print(sorted(cities))

print('#' * 52 + '  So, we basically have to "restart" an iterator by **creating a new one each time**.')
print('#' * 52 + '  But in this case, we are also re-creating the underlying data every time - seems wasteful!')
print('#' * 52 + '  Instead, maybe we can split the **iterator** part of our code from the **data** part of our code.')


class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']

    def __len__(self):
        return len(self._cities)


class CityIterator:
    def __init__(self, city_obj):
        # cities is an instance of Cities
        self._city_obj = city_obj
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index += 1
            return item

cities = Cities()
iter_1 = CityIterator(cities)

for city in iter_1:
    print(city)

iter_2 = CityIterator(cities)
print([city.upper() for city in iter_2])

print('#' * 52 + '  So, we are almost at a solution now. At least we can create the **iterator**'
                 '  objects without having to recreate the `Cities` object every time.')
print('#' * 52 + '  But, we still have to remember to create a new iterator,'
                 '  **and** we can no longer iterate over the `cities` object anymore!')

# for city in cities:
#     print(city)     # TypeError: 'Cities' object is not iterable

print('#' * 52 + '  Whenever we iterated our iterator, the first thing Python did was call `__iter__`.')


class CityIterator:
    def __init__(self, city_obj):
        # cities is an instance of Cities
        print('Calling CityIterator __init__')
        self._city_obj = city_obj
        self._index = 0

    def __iter__(self):
        print('Calling CitiyIterator instance __iter__')
        return self

    def __next__(self):
        print('Calling __next__')
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index += 1
            return item

iter_1 = CityIterator(cities)
print('#' * 52 + '  ')
for city in iter_1:
    print(city)

print('#' * 52 + '  We actually have everything we need to now make `Cities` an **iterable**'
                 '  since we already have the `CityIterator` created:')


class CityIterator:
    def __init__(self, city_obj):
        # cities is an instance of Cities
        print('Calling CityIterator __init__')
        self._city_obj = city_obj
        self._index = 0

    def __iter__(self):
        print('Calling CitiyIterator instance __iter__')
        return self

    def __next__(self):
        print('Calling __next__')
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index += 1
            return item


class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']

    def __len__(self):
        return len(self._cities)

    def __iter__(self):
        print('Calling Cities instance __iter__')
        return CityIterator(self)

cities = Cities()

for city in cities:
    print(city)

print('#' * 52 + '  And watch what happens if we try to run that loop again:')

for city in cities:
    print(city)

print('#' * 52 + '  A new **iterator** was created when the `for` loop started.')
print('#' * 52 + '  In fact, same happens for anything that is going to iterate our iterable -'
                 '  it first calls the `__iter__` method of the itrable to get a **new** iterator,'
                 '  then uses the iterator to call `__next__`.')

print(list(enumerate(cities)))
print('#' * 52 + '  ')
print(sorted(cities, reverse=True))

print('#' * 52 + '  Now we can put the iterator class inside our `Cities` class to keep the code self-contained:')

del CityIterator  # just to make sure CityIterator is not in our global scope


class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']

    def __len__(self):
        return len(self._cities)

    def __iter__(self):
        print('Calling Cities instance __iter__')
        return self.CityIterator(self)

    class CityIterator:
        def __init__(self, city_obj):
            # cities is an instance of Cities
            print('Calling CityIterator __init__')
            self._city_obj = city_obj
            self._index = 0

        def __iter__(self):
            print('Calling CitiyIterator instance __iter__')
            return self

        def __next__(self):
            print('Calling __next__')
            if self._index >= len(self._city_obj):
                raise StopIteration
            else:
                item = self._city_obj._cities[self._index]
                self._index += 1
                return item

cities = Cities()
print(list(enumerate(cities)))

print('#' * 52 + '  Technically we can even get an iterator instance ourselves directly,'
                 '  by calling `iter()` on the `cities` object:')

iter_1 = iter(cities)
iter_2 = iter(cities)

print('#' * 52 + '  As you can see, Python created and returned two different instances of the `CityIterator` object.')

print(id(iter_1), id(iter_2))

print('#' * 52 + '  #### Mixing Iterables and Sequences')
print('#' * 52 + '  `Cities` is an iterable, but it is not a sequence type:')

cities = Cities()
print(len(cities))
# cities[1]       # TypeError: 'Cities' object does not support indexing

print('#' * 52 + '  Since our Cities **could** also be a sequence,'
                 '  we could also decide to implement the `__getitem__` method to make it into a sequence:')


class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']

    def __len__(self):
        return len(self._cities)

    def __getitem__(self, s):
        print('getting item...')
        return self._cities[s]

    def __iter__(self):
        print('Calling Cities instance __iter__')
        return self.CityIterator(self)

    class CityIterator:
        def __init__(self, city_obj):
            # cities is an instance of Cities
            print('Calling CityIterator __init__')
            self._city_obj = city_obj
            self._index = 0

        def __iter__(self):
            print('Calling CitiyIterator instance __iter__')
            return self

        def __next__(self):
            print('Calling __next__')
            if self._index >= len(self._city_obj):
                raise StopIteration
            else:
                item = self._city_obj._cities[self._index]
                self._index += 1
                return item

cities = Cities()
print(cities[0])
print(next(iter(cities)))

print('#' * 52 + '  Now that Cities is both a sequence type (`__getitem__`) and an iterable (`__iter__`),'
                 '  when we loop over `cities`, is Python going to use `__getitem__` or `__iter__`?')

cities = Cities()
for city in cities:
    print(city)

print('#' * 52 + '  ### Python Built-In Iterables and Iterators')
print('#' * 52 + '  The way iterables and iterators work in our custom `Cities`'
                 '  example is exactly the way Python iterables work too.')

l = [1, 2, 3]

iter_l = iter(l)
#or could use iter_1 = l.__iter__()

print(type(iter_l))
print(next(iter_l))
print(next(iter_l))
print(next(iter_l))

# print(next(iter_l)) # StopIteration:
print('#' * 52 + '  Since `iter_l` is an iterator, it also implements the `__iter__` method,'
                 '  which just returns the iterator itself:')

print(id(iter_l), id(iter(iter_l)))

print('__next__' in dir(iter_l))
print('__iter__' in dir(iter_l))

print('#' * 52 + '  Since the list `l` is an iterable it also implements the `__iter__` method:')

print('__iter__' in dir(l))

print('#' * 52 + '  but does not implement a `__next__` method:')

print('__next__' in dir(l))

print('#' * 52 + '  Of course, since lists are also sequence types, they also implement the `__getitem__` method:')

print('__getitem__' in dir(l))

print('#' * 52 + '  Sets and dictionaries on the other hand are not sequence types:')

print('__getitem__' in dir(set))
print('__iter__' in dir(set))
print('#' * 52 + '  ')
s = {1, 2, 3}
print('__next__' in dir(iter(s)))
print('__iter__' in dir(dict))

print('#' * 52 + '  But what does the iterator for a dictionary actually return?')
print('#' * 52 + '  It iterates over what?')
print('#' * 52 + '  You shoudl probably already guess the answer to that one!')

d = dict(a=1, b=2, c=3)
iter_d = iter(d)
print(next(iter_d))

print('#' * 52 + '  Dictionary iterators will iterate over the **keys** of the dictionary.')
print('#' * 52 + '  To iterate over the values, we could use the `values()` method which returns'
                 '  an **iterable** over the values of the dictionary:')

iter_vals = iter(d.values())
print(next(iter_vals))

print('#' * 52 + '  And to iterate over both the keys and values, dictionaries provide an `items()` iterable:')

iter_items = iter(d.items())
print(next(iter_items))

