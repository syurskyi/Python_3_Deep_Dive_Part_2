print('#' * 52 + '  Often we write classes that use some existing iterable for the data contained in our class')
print('#' * 52 + '  By default, that class is not iterable, and we would need to implement an iterator for our class'
                 '  and implement the `__iter__` method in our class to return new instances of that iterator.')
print('#' * 52 + '  But, if our underlying data structure for our class is already an iterable, '
                 '  theres a much quicker way of doing it - delegation.')

from collections import namedtuple

Person = namedtuple('Person', 'first last')

class PersonNames:
    def __init__(self, persons):
        try:
            self._persons = [person.first.capitalize()
                             + ' ' + person.last.capitalize()
                            for person in persons]
        except (TypeError, AttributeError):
            self._persons = []

persons = [Person('michaeL', 'paLin'), Person('eric', 'idLe'),
           Person('john', 'cLeese')]

person_names = PersonNames(persons)

print('#' * 52 + '  ')
print('#' * 52 + '  Technically we can see the underlying data by accessing the (pseudo) private variable `_persons`.')

print(person_names._persons)

print('#' * 52 + '  But we really would prefer making our `PersonNames` instances iterable.')
print('#' * 52 + '  To do so we need to implement the `__iter__` method that returns an iterator that can be used'
                 '  for iterating over the `_persons` list.')
print('#' * 52 + '  But lists are iterables, so they can provide an iterator, and that is precisely what we will do - '
                 '  we will **delegate** our own iterator, to the lists iterator:')


class PersonNames:
    def __init__(self, persons):
        try:
            self._persons = [person.first.capitalize()
                             + ' ' + person.last.capitalize()
                             for person in persons]
        except TypeError:
            self._persons = []

    def __iter__(self):
        return iter(self._persons)

print('#' * 52 + '  ')
print('#' * 52 + '  And now, `PersonNames` is iterable!')

persons = [Person('michaeL', 'paLin'), Person('eric', 'idLe'),
           Person('john', 'cLeese')]
person_names = PersonNames(persons)

for p in person_names:
    print(p)

print('#' * 52 + '  And of course we can sort, use list comprehensions, and so on - our PersonNames **is** an iterable.')
print('#' * 52 + '  Here we sort the names based on the full name, then split the names (on the space)'
                 '  and return a tuple of first name, last name:')

print([tuple(person_name.split()) for person_name in sorted(person_names)])

print('#' * 52 + '  Or, if we want to sort based on the last name:')

print(sorted(person_names, key=lambda x: x.split()[1]))