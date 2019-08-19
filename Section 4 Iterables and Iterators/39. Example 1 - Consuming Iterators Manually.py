print('#' * 52 + '  Lets quickly see how do this again, using a string as the underlying iterable:')

s = 'I sleep all night, and I work all day'

iter_s = iter(s)

print(next(iter_s))
print(next(iter_s))
print(next(iter_s))
print(next(iter_s))
print(next(iter_s))

print('#' * 52 + '  Lets first load the data and see what it looks like:')

with open('cars.csv') as file:
    for line in file:
        print(line)

print('#' * 52 + '  As we can see, the values are delimited by `;`'
                 '  and the first two lines consist of the column names, and column types.')
print('#' * 52 + '  The reason for the spacing between each line is that each line ends with a newline,'
                 '  and our print statement also emits a newline by default.')
print('#' * 52 + '  So we will have to strip those out.')
print('#' * 52 + '  * read the first line to get the column headers and create a named tuple class')
print('#' * 52 + '  read data types from second line and store this so we can cast the strings'
                 '  we are reading to the correct data type')
print('#' * 52 + '  read the data rows and parse them into a named tuples')

with open('cars.csv') as file:
    row_index = 0
    for line in file:
        if row_index == 0:
            # header row
            headers = line.strip('\n').split(';')
            print(headers)
        elif row_index == 1:
            # data type row
            data_types = line.strip('\n').split(';')
            print(data_types)
        else:
            # data rows
            data = line.strip('\n').split(';')
            print(data)
        row_index += 1

print('#' * 52 + '  ')

from collections import namedtuple
cars = []

with open('cars.csv') as file:
    row_index = 0
    for line in file:
        if row_index == 0:
            # header row
            headers = line.strip('\n').split(';')
            Car = namedtuple('Car', headers)
        elif row_index == 1:
            # data type row
            data_types = line.strip('\n').split(';')
            print(data_types)
        else:
            # data rows
            data = line.strip('\n').split(';')
            car = Car(*data)
            cars.append(car)
        row_index += 1

print(cars[0])
print('#' * 52 + '  We still need to parse the data into strings, integers, floats...')
print('#' * 52 + '  Lets break this problem down into smaller chunks:')
print('#' * 52 + '  First we need to figure cast to a data type based on the data type string:')
print('#' * 52 + '  STRING --> `str`')
print('#' * 52 + '  DOUBLE --> `float`')
print('#' * 52 + '  INT --> `int`')
print('#' * 52 + '   CAT --> `str`')

def cast(data_type, value):
    if data_type == 'DOUBLE':
        return float(value)
    elif data_type == 'INT':
        return int(value)
    else:
        return str(value)

data_types = ['STRING', 'DOUBLE', 'INT', 'DOUBLE', 'DOUBLE', 'DOUBLE', 'DOUBLE', 'INT', 'CAT']
data_row = ['Chevrolet Chevelle Malibu', '18.0', '8', '307.0', '130.0', '3504.', '12.0', '70', 'US']

print(list(zip(data_types, data_row)))

print('#' * 52 + '  And we can either use a `map()` or a list comprehension to apply the cast function to each one:')

print([cast(data_type, value) for data_type, value in zip(data_types, data_row)])

print('#' * 52 + '  So now we can write this in a function:')

def cast_row(data_types, data_row):
    return [cast(data_type, value)
            for data_type, value in zip(data_types, data_row)]

print('#' * 52 + '  Lets go back and fix up our original code now:')

from collections import namedtuple
cars = []

with open('cars.csv') as file:
    row_index = 0
    for line in file:
        if row_index == 0:
            # header row
            headers = line.strip('\n').split(';')
            Car = namedtuple('Car', headers)
        elif row_index == 1:
            # data type row
            data_types = line.strip('\n').split(';')
        else:
            # data rows
            data = line.strip('\n').split(';')
            data = cast_row(data_types, data)
            car = Car(*data)
            cars.append(car)
        row_index += 1

print(cars[0])

print('#' * 52 + '  Now lets see if we can clean up this code by using iterators directly:')

from collections import namedtuple
cars = []

with open('cars.csv') as file:
    file_iter = iter(file)
    headers = next(file_iter).strip('\n').split(';')
    Car = namedtuple('Car', headers)
    data_types = next(file_iter).strip('\n').split(';')
    for line in file_iter:
        data = line.strip('\n').split(';')
        data = cast_row(data_types, data)
        car = Car(*data)
        cars.append(car)

print(cars[0])

print('#' * 52 + '  That is already quite a bit cleaner... But why stop there!')

from collections import namedtuple

with open('cars.csv') as file:
    file_iter = iter(file)
    headers = next(file_iter).strip('\n').split(';')
    data_types = next(file_iter).strip('\n').split(';')
    cars_data = [cast_row(data_types,
                          line.strip('\n').split(';'))
                   for line in file_iter]
    cars = [Car(*item) for item in cars_data]

print(cars_data[0])
print(cars[0])

print('#' * 52 + '  I chose to split creating the parsed cars_data and the named tuple list'
                 '  into two steps for readability - but we could combine them into a single step:')

from collections import namedtuple

with open('cars.csv') as file:
    file_iter = iter(file)
    headers = next(file_iter).strip('\n').split(';')
    data_types = next(file_iter).strip('\n').split(';')
    cars = [Car(*cast_row(data_types,
                          line.strip('\n').split(';')))
            for line in file_iter]


print(cars[0])

