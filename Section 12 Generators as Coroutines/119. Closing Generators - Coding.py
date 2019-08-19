print('#' * 52 + '  We can actually close a generator by sending it a special message, calling its `close()` method.')
print('#' * 52 + '  When that happens, an exception is raised **inside** the generator,'
                 '  and we may or may not want to do something - maybe cleaning up a resource,'
                 '  commiting a transaction to a database, etc')

from inspect import getgeneratorstate

import csv

def parse_file(f_name):
    print('opening file...')
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            yield row
    finally:
        print('closing file...')
        f.close()

import itertools

parser = parse_file('cars.csv')
for row in itertools.islice(parser, 10):
    print(row)

print('#' * 52 + '  ')

parser.close()

print('#' * 52 + '  And the state of the generator is now closed:')

from inspect import getgeneratorstate


print(getgeneratorstate(parser))

print('#' * 52 + '  Which means we can no longer call `next()` on it - we will just get a `StopIteration` exception:')

# next(parser) # StopIteration:

print('#' * 52 + '  Lets look at an example of this:')

def parse_file(f_name):
    print('opening file...')
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)  # skip header row
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            yield row
    except Exception as ex:
        print('some exception occurred', str(ex))
    except GeneratorExit:
        print('Generator was closed!')
    finally:
        print('cleaning up...')
        f.close()

parser = parse_file('cars.csv')
for row in itertools.islice(parser, 5):
    print(row)

print(parser.close())

print('#' * 52 + '  You will notice that the exception occurred, and then the generator ran'
                 '  the `finally` block and had a clean exit - in other words, '
                 '  the `GeneratorExit` exception was silenced, but the generator terminated (returned),'
                 '  so that is perfectly fine.')
print('#' * 52 + '  But what happens if we catch that exception inside a loop maybe,'
                 '  and simply ignore it and try to keep going?')

def parse_file(f_name):
    print('opening file...')
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)  # skip header row
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            try:
                yield row
            except GeneratorExit:
                print('ignoring call to close generator...')
    finally:
        print('cleaning up...')
        f.close()

parser = parse_file('cars.csv')
for row in itertools.islice(parser, 5):
    print(row)

# print(parser.close())  # RuntimeError: generator ignored GeneratorExit

print('#' * 52 + '  Generators should be cooperative, '
                 '  and ignore a request to close down is not exactly being cooperative.')
print('#' * 52 + '  If we really want to catch the exception inside our loop, '
                 '  we have to either re-raise it or return from the generator:')

def parse_file(f_name):
    print('opening file...')
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)  # skip header row
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            try:
                yield row
            except GeneratorExit:
                print('got a close...')
                raise
    finally:
        print('cleaning up...')
        f.close()

parser = parse_file('cars.csv')
for row in itertools.islice(parser, 5):
    print(row)

print('#' * 52 + '  ')

print(parser.close())

print('#' * 52 + '  As will this:')

def parse_file(f_name):
    print('opening file...')
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)  # skip header row
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            try:
                yield row
            except GeneratorExit:
                print('got a close...')
                return
    finally:
        print('cleaning up...')
        f.close()

parser = parse_file('cars.csv')
for row in itertools.islice(parser, 5):
    print(row)

print(parser.close())

print('#' * 52 + '  And of course, our `finally` block still ran.')
print('#' * 52 + '  If we want to we can also raise an exception, but this will then be received by the caller,'
                 '  who either has to handle it, or let it bubble up:')

def parse_file(f_name):
    print('opening file...')
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)  # skip header row
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            try:
                yield row
            except GeneratorExit:
                print('got a close...')
                raise Exception('why, oh why, did you do this?') from None
    finally:
        print('cleaning up...')
        f.close()

parser = parse_file('cars.csv')
# for row in itertools.islice(parser, 5):
#     print(row)

print('#' * 52 + '  We can certainly do it using a context manager - but we can also do it using a coroutine.')

def save_to_db():
    print('starting new transaction')
    while True:
        try:
            data = yield
            print('sending data to database:', data)
        except GeneratorExit:
            print('committing transaction')
            raise

trans = save_to_db()
# print(next(trans))
next(trans)

print('#' * 52 + '  ')

trans.send('data 1')

print('#' * 52 + '  ')

trans.send('data 2')

print('#' * 52 + '  ')

trans.close()

print('#' * 52 + '  But of course, something could go wrong while writing the data to the database,'
                 '  in which case we would want to abort the transaction instead:')

def save_to_db():
    print('starting new transaction')
    while True:
        try:
            data = yield
            print('sending data to database:', eval(data))
        except Exception:
            print('aborting transaction')
        except GeneratorExit:
            print('committing transaction')
            raise

trans = save_to_db()
next(trans)

trans.send('1 + 10')
trans.send('1/0')

print('#' * 52 + '  But we have a slight problem:')

trans.send('2 + 2')

print('#' * 52 + '  But we can still commit the transaction when things do not go wrong:')

trans = save_to_db()
next(trans)
trans.send('1+10')
trans.send('2+10')
trans.close()

print('#' * 52 + '  ')
print('#' * 52 + '  ')
print('#' * 52 + '  ')

def save_to_db():
    print('starting new transaction')
    is_abort = False
    try:
        while True:
            data = yield
            print('sending data to database:', eval(data))
    except Exception:
        is_abort = True
        raise
    finally:
        if is_abort:
            print('aborting transaction')
        else:
            print('committing transaction')

trans = save_to_db()
next(trans)
trans.send('1 + 1')
trans.close()

trans = save_to_db()
next(trans)
trans.send('1 / 0')