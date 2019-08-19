print('#' * 52 + '  ### Pipelines - Pulling Data')

import csv

def parse_data(f_name):
    f = open(f_name)
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)  # skip header row
        yield from csv.reader(f, dialect=dialect)
    finally:
        f.close()

import itertools

for row in itertools.islice(parse_data('cars.csv'), 5):
    print(row)

print('#' * 52 + '  Now lets filter out rows based on the car make:')

def filter_data(rows, contains):
    for row in rows:
        if contains in row[0]:
            yield row

print('#' * 52 + '  We can now start building a (pull) pipeline by pulling data from the data source, '
                 '  through the filter:')
print('#' * 52 + '  caller <-- filter <-- data')

data = parse_data('cars.csv')
filtered_data = filter_data(data, 'Chevrolet')

# pipeline: caller <-- filtered_data <-- data

for row in itertools.islice(filtered_data, 5):
    print(row)

print('#' * 52 + '  As you can see, using iteration we are pulling data all the way from the file, '
                 '  through the csv reader, through the filter and back to us (the caller).')
print('#' * 52 + '  Lets further filter out rows that contain the word Carlo as well:')

data = parse_data('cars.csv')
filter_1 = filter_data(data, 'Chevrolet')
filter_2 = filter_data(filter_1, 'Carlo')

# pipeline: caller <-- filter_2 <-- filtered_1 <-- data

for row in itertools.islice(filter_2, 5):
    print(row)

print('#' * 52 + '  We can package all this up into a single delegator generator:')

def output(f_name):
    data = parse_data(f_name)
    filter_1 = filter_data(data,'Chevrolet')
    filter_2 = filter_data(filter_1, 'Carlo')
    yield from filter_2

results = output('cars.csv')
for row in results:
    print(row)

print('#' * 52 + '  We can actually make this a little more generic while we are at it:')

def output(f_name, *filter_words):
    data = parse_data(f_name)
    for filter_word in filter_words:
        data = filter_data(data, filter_word)
    yield from data

results = output('cars.csv', 'Chevrolet')
for row in itertools.islice(results, 5):
    print(row)

print('#' * 52 + '  ')

results = output('cars.csv', 'Chevrolet', 'Carlo', 'Landau')
for row in itertools.islice(results, 5):
    print(row)