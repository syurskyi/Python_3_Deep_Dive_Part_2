import csv


def data_reader(f_name):
    f = open(f_name)
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        reader = csv.reader(f, dialect=dialect)
        yield from reader
    finally:
        f.close()


for row in data_reader('car_data.csv'):
    print(row)

print('#' * 52 + '  Lets create our indices, output headers and data converters for this file -'
                 '  basically these are our configuration parameters for this data file.')

input_file = 'car_data.csv'

idx_make = 0
idx_model = 1
idx_year = 2
idx_vin = 3
idx_color = 4

headers = ('make', 'model', 'year', 'vin', 'color')

converters = (str, str, int, str, str)

print('#' * 52 + '  Now lets create a generator that will return the parsed data:')

def data_parser():
    data = data_reader(input_file)
    next(data)  # skip header row
    for row in data:
        parsed_row = [converter(item)
                      for converter, item in zip(converters, row)]
        yield parsed_row


data = data_parser()
for _ in range(5):
    print(next(data))

print('#' * 52 + '  Lets also write our coroutine decorator that will auto prime coroutines:')

def coroutine(fn):
    def inner(*args, **kwargs):
        g = fn(*args, **kwargs)
        next(g)
        return g
    return inner

print('#' * 52 + '  Next we are going to write a coroutine that will create and write data to a file.')
print('#' * 52 + '  We will need to pass the output file name to the coroutine, '
                 '  and the coroutine will assume that the data is being passed in as a list '
                 '  (basically whatever is coming back from `data_parser`).')
print('#' * 52 + '  To make it easier, '
                 '  we will also pass it the column headers so we can include that in the output file.')

@coroutine
def save_data(f_name, headers):
    with open(f_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        while True:
            data_row = yield
            writer.writerow(data_row)

print('#' * 52 + '  Now we re going to create a filter coroutine that will have the following parameters:')

@coroutine
def filter_data(filter_predicate, target):
    while True:
        data_row = yield
        if filter_predicate(data_row):
            target.send(data_row)

print('#' * 52 + '  Next, lets write our broadcaster. '
                 '  It just sends received data to all the generators specified in the `targets` argument:')

@coroutine
def broadcast(targets):
    while True:
        data_row = yield
        for target in targets:
            target.send(data_row)


def process_data():
    data = data_parser()

    out_pink_cars = save_data('pink_cars.csv', headers)
    out_ford_green = save_data('ford_green.csv', headers)
    out_older = save_data('older.csv', headers)

    filter_pink_cars = filter_data(lambda d: d[idx_color].lower() == 'pink',
                                   out_pink_cars)

    def pred_ford_green(data_row):
        return (data_row[idx_make].lower() == 'ford'
                and data_row[idx_color].lower() == 'green')

    filter_ford_green = filter_data(pred_ford_green, out_ford_green)
    filter_older = filter_data(lambda d: d[idx_year] <= 2010, out_older)
    filters = (filter_pink_cars, filter_ford_green, filter_older)
    broadcaster = broadcast(filters)

    for row in data:
        broadcaster.send(row)

    print('Finished processing.')

process_data()

print('#' * 52 + '  Lets see what those files contain:')

def print_file_data():
    for file_name in ('pink_cars.csv', 'ford_green.csv', 'older.csv'):
        print(f'***** {file_name} *****')
        for row in data_reader(file_name):
            print(row)
        print('\n\n\n')

print_file_data()

print('#' * 52 + '  Theres one more bit of cleanup I want to do though.')
print('#' * 52 + '  I would prefer to have the definition of my pipeline not also be the consumer of the data. '
                 '  Just trying to keep functionality more separated.')
print('#' * 52 + '  So lets rewrite change `process_data` to just be another step in the pipeline.')


@coroutine
def pipeline_coro():
    out_pink_cars = save_data('pink_cars.csv', headers)
    out_ford_green = save_data('ford_green.csv', headers)
    out_older = save_data('older.csv', headers)

    filter_pink_cars = filter_data(lambda d: d[idx_color].lower() == 'pink',
                                   out_pink_cars)

    def pred_ford_green(data_row):
        return (data_row[idx_make].lower() == 'ford'
                and data_row[idx_color].lower() == 'green')

    filter_ford_green = filter_data(pred_ford_green, out_ford_green)
    filter_older = filter_data(lambda d: d[idx_year] <= 2010, out_older)

    filters = (filter_pink_cars, filter_ford_green, filter_older)

    broadcaster = broadcast(filters)

    while True:
        data_row = yield
        broadcaster.send(data_row)

pipe = pipeline_coro()
data = data_parser()
for row in data:
    pipe.send(row)

# print_file_data()  # Error: Could not determine delimiter
print('#' * 52 + '  ')
print('#' * 52 + '  Uh-oh, we get an exception. Why did the parser fail to figure out the dialect of the file?')

with open('pink_cars.csv') as f:
    for row in f:
        print('row', row)

print('#' * 52 + '  ')

print('#' * 52 + '  The file is empty!!')
print('#' * 52 + '  The issue is that our files have not been closed yet!')
print('#' * 52 + '  The pipeline coroutine is still active, so nothing go released or closed -'
                 '  including the endpoints of our pipeline.')
print('#' * 52 + '  Fortunately this is easy to do - we just need to close the pipeline.')

pipe.close()

print('#' * 52 + '  ')
print('#' * 52 + '  And now we should be able to read those files:')

print_file_data()

print('#' * 52 + '  Perfect, so just to recap, here is how we would use our pipeline:')

pipe = pipeline_coro()
data = data_parser()
for row in data:
    pipe.send(row)
pipe.close()

print('#' * 52 + '  Notice how we open the pipeline, and then close it? Does this remind you of a context manager?')
print('#' * 52 + '  Lets write a context manager for our pipeline - that way we will never forget to close it!')

from contextlib import contextmanager

@contextmanager
def pipeline():
    p = pipeline_coro()
    try:
        yield p
    finally:
        p.close()

with pipeline() as pipe:
    data = data_parser()
    for row in data:
        pipe.send(row)

print_file_data()