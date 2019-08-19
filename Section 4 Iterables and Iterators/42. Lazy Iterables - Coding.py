print('#' * 52 + '  Lets look at an example of a lazy class property:')

import math


class Circle:
    def __init__(self, r):
        self.radius = r

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, r):
        self._radius = r
        self.area = math.pi * r ** 2


c = Circle(1)
print(c.area)

c.radius = 2

print(c.radius, c.area)

print('#' * 52 + '  But instead of doing it this way, we could just calculate the area every time it is'
                 ' requested without actually storing the value:')


class Circle:
    def __init__(self, r):
        self.radius = r

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, r):
        self._radius = r

    @property
    def area(self):
        return math.pi * self.radius ** 2

c = Circle(1)
print(c.area)
c.radius = 2
print(c.area)

print('#' * 52 + ' But the area is always recalculated, '
                 ' so we may take a hybrid approach where we want to store the area so we dont need to recalculate'
                 ' it every time (ecept when the radius is modified), but delay calculating'
                 ' the area until it is requested - that way if it is never requested,'
                 ' we didnt waste the CPU cycles to calculate it, or the memory to store it.')


class Circle:
    def __init__(self, r):
        self.radius = r

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, r):
        self._radius = r
        self._area = None

    @property
    def area(self):
        if self._area is None:
            print('Calculating area...')
            self._area = math.pi * self.radius ** 2
        return self._area

c = Circle(1)

print(c.area)
print(c.area)

c.radius = 2
print(c.area)

print('#' * 52 + '  We can sometimes do something similar with iterables - we dont actually have to store every item'
                 '  of the collection - we may be able to just calculate the item as needed.')


class Factorials:
    def __init__(self, length):
        self.length = length

    def __iter__(self):
        return self.FactIter(self.length)

    class FactIter:
        def __init__(self, length):
            self.length = length
            self.i = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.i >= self.length:
                raise StopIteration
            else:
                result = math.factorial(self.i)
                self.i += 1
                return result

facts = Factorials(5)
print(list(facts))

print('#' * 52 + '  So as you can see, we do not store the values of the iterable,'
                 '  instead we just calculate the items as needed.')

print('#' * 52 + '  In fact, now that we have this iterable, we dont even need it to be finite:')


class Factorials:
    def __iter__(self):
        return self.FactIter()

    class FactIter:
        def __init__(self):
            self.i = 0

        def __iter__(self):
            return self

        def __next__(self):
            result = math.factorial(self.i)
            self.i += 1
            return result

factorials = Factorials()
fact_iter = iter(factorials)

for _ in range(10):
    print(next(fact_iter))
