print('#' * 52 + '  When a function requires an iterable for one of its arguments, '
                 ' it will also work with any iterator (since iterators are themselves iterables).')
print('#' * 52 + '  But things can go wrong if you do that!')
print('#' * 52 + '  Lets say we have an iterator that returns a collection of random numbers,'
                 '  and we want, for each such collection, find the minimum amd maximum value:')

import random


class Randoms:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        else:
            self.i += 1
            return random.randint(0, 100)

random.seed(0)
l = list(Randoms(10))
print(l)

print('#' * 52 + '  Now we can easily find the min and max values:')

print(min(l), max(l))

print('#' * 52 + '  But watch what happens if we do this:')

random.seed(0)
l = Randoms(10)

print(min(l))
# print(max(l))  #  ValueError: max() arg is an empty sequence

print('#' * 52 + '  That is because when `min` ran, it iterated over the **iterator** `Randoms(10)`.')
print('#' * 52 + '  When we called `max` on the same iterator, it had already been exhausted -'
                 '  i.e. the argument to max was now empty!')
print('#' * 52 + '  So, be really careful when using iterators!')

f = open('cars.csv')
for row in f:
    print(row, end='')
f.close()

def parse_data_row(row):
    row = row.strip('\n').split(';')
    return row[0], float(row[1])

def max_mpg(data):
    # get an iterator for data (which should be an iterable of some kind)
    max_mpg = 0
    for row in data:
        _, mpg = parse_data_row(row)
        if mpg > max_mpg:
            max_mpg = mpg
    return max_mpg

print('#' * 52 + '  ')

f = open('cars.csv')
next(f)
next(f)
print(max_mpg(f))
f.close()

def list_data(data, mpg_max):
    for row in data:
        car, mpg = parse_data_row(row)
        mpg_perc = mpg / mpg_max * 100
        print(f'{car}: {mpg_perc:.2f}%')

f = open('cars.csv')
next(f), next(f)
list_data(f, 46.6)
f.close()

print('#' * 52 + '  Now lets try and put these together:')

with open('cars.csv') as f:
    next(f)
    next(f)
    max_ = max_mpg(f)
    print(f'max={max_}')
    list_data(f, max_)

print('#' * 52 + '  No output from `list_data`!!')
print('#' * 52 + '  That is because when we called `list_data`'
                 '  we had already exhausted the data file in the call to `max_mpg`.')
print('#' * 52 + '  Our only option is to either create the iterator twice:')

with open('cars.csv') as f:
    next(f), next(f)
    max_ = max_mpg(f)

with open('cars.csv') as f:
    next(f), next(f)
    list_data(f, max_)

print('#' * 52 + '  or we could read the entire data set into a list first - but of course'
                 '  if the file is huge we will have some potential for running out memory:')

with open('cars.csv') as f:
    data = [row for row in f][2:]

with open('cars.csv') as f:
    data = f.readlines()[2:]

max_ = max_mpg(data)
list_data(data, max_)

print('#' * 52 + '  We may even write functions that need to iterate more than once over an iterable.')


def list_data(data):
    max_mpg = 0
    for row in data:
        _, mpg = parse_data_row(row)
        if mpg > max_mpg:
            max_mpg = mpg

    for row in data:
        car, mpg = parse_data_row(row)
        mpg_perc = mpg / max_mpg * 100
        print(f'{car}: {mpg_perc:.2f}%')

print('#' * 52 + '  But this will not work if we pass an iterator as the argument:')


def list_data(data):
    if iter(data) is data:
        raise ValueError('data cannot be an iterator.')
    max_mpg = 0
    for row in data:
        _, mpg = parse_data_row(row)
        if mpg > max_mpg:
            max_mpg = mpg

    for row in data:
        car, mpg = parse_data_row(row)
        mpg_perc = mpg / max_mpg * 100
        print(f'{car}: {mpg_perc:.2f}%')

# with open('cars.csv') as f:
#     next(f)
#     next(f)
#     list_data(f)       # ValueError: data cannot be an iterator.

print('#' * 52 + '  or this way:')


def list_data(data):
    if iter(data) is data:
        data = list(data)

    max_mpg = 0
    for row in data:
        _, mpg = parse_data_row(row)
        if mpg > max_mpg:
            max_mpg = mpg

    for row in data:
        car, mpg = parse_data_row(row)
        mpg_perc = mpg / max_mpg * 100
        print(f'{car}: {mpg_perc:.2f}%')

with open('cars.csv') as f:
    next(f)
    next(f)
    list_data(f)
