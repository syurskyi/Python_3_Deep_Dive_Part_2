def gen():
    try:
        while True:
            received = yield
            print(received)
    finally:
        print('exception must have happened...')


g = gen()

next(g)

g.send('hello')
# g.throw(ValueError, 'custom message')  #  ValueError: custom message

print('#' * 52 + '  As you can see, the exception occurred **inside** the generator,'
                 '  and then propagated up to the caller (we did not intercept and silence the exception).')


def gen():
    try:
        while True:
            received = yield
            print(received)
    except ValueError:
        print('received the value error...')
    finally:
        print('generator exiting and closing')


g = gen()

next(g)
g.send('hello')
# g.throw(ValueError, 'stop it!')  #

print('#' * 52 + '  ##### if the generator catches the exception and yields a value,'
                 '  that is the return value of the throw() method')

from inspect import getgeneratorstate


def gen():
    while True:
        try:
            received = yield
            print(received)
        except ValueError as ex:
            print('ValueError received...', ex)


g = gen()
next(g)

g.send('hello')
g.throw(ValueError, 'custom message')

g.send('hello')

print('#' * 52 + '  And the generator is now in a suspended state, waiting for our next call:')

print(getgeneratorstate(g))

print(
    '#' * 52 + '  ##### if the generator does not catch the exception, the exception is propagated back to the caller')


def gen():
    while True:
        received = yield
        print(received)


g = gen()
next(g)
g.send('hello')

# g.throw(ValueError, 'custom message') # ValueError: custom message

print('#' * 52 + '  And the generator is now in a closed state:')

print(getgeneratorstate(g))

print('#' * 52 + '  ##### if the generator catches the exception, and exits (returns), '
                 '  the StopIteration exception is propagated to the caller')


def gen():
    try:
        while True:
            received = yield
            print(received)
    except ValueError as ex:
        print('ValueError received', ex)
        return None


g = gen()
next(g)
g.send('hello')

# g.throw(ValueError, 'custom message')

print(getgeneratorstate(g))  # must be GEN_CLOSED

print('#' * 52 + '  ##### if the generator catches the exception, and raises another exception,'
                 '  that exception is propagated to the caller')


def gen():
    try:
        while True:
            received = yield
            print(received)
    except ValueError as ex:
        print('ValueError received...', ex)
        raise ZeroDivisionError('not really...')


g = gen()
next(g)
g.send('hello')

# g.throw(ValueError, 'custom message')  # ZeroDivisionError: not really...

print('#' * 52 + '  And out generator is, once again, in a closed state:')

print(getgeneratorstate(g))  # must be GEN_CLOSED

print('#' * 52 + ' As you can see our traceback includes both the `ZeroDivisionError` '
                 ' and the `ValueError` that caused the `ZeroDivisionError` to happen in the first place.')
print('#' * 52 + ' If you dont want to have that  traceback you can easily remove it and only display '
                 ' the `ZeroDivisionError` (I will cover this and exceptions in detail in a later part of this series):')


def gen():
    try:
        while True:
            received = yield
            print(received)
    except ValueError as ex:
        print('ValueError received...', ex)
        raise ZeroDivisionError('not really...') from None


g = gen()
next(g)
g.send('hello')

# g.throw(ValueError, 'custom message') # ZeroDivisionError: not really...

print('#' * 52 + '  #### Example of where this can be useful')


class CommitException(Exception):
    pass


class RollbackException(Exception):
    pass


def write_to_db():
    print('opening database connection...')
    print('start transaction...')
    try:
        while True:
            try:
                data = yield
                print('writing data to database...', data)
                print()
            except CommitException:
                print('committing transaction...')
                print('opening next transaction...')
                print()
            except RollbackException:
                print('aborting transaction...')
                print('opening next transaction...')
                print()
    finally:
        print('generator closing...')
        print('aborting transaction...')
        print('closing database connection...')
        print()


sql = write_to_db()

next(sql)

print('#' * 52 + '  ')

sql.send(100)

print('#' * 52 + '  ')

sql.throw(CommitException)

sql.send(200)
sql.throw(RollbackException)
sql.send(200)
sql.throw(CommitException)
sql.close()

print('#' * 52 + '  #### throw() and close()')


def gen():
    try:
        while True:
            received = yield
            print(received)
    finally:
        print('closing down...')


g = gen()
next(g)
g.send('hello')
g.close()

g = gen()
next(g)
g.send('hello')
# g.throw(GeneratorExit) # GeneratorExit:

print('#' * 52 + '  Even if we catch the exception, we are still exiting the generator, so using `throw` will result in'
                 '  the caller receiving a `StopIteration` exception.')

def gen():
    try:
        while True:
            received = yield
            print(received)
    except GeneratorExit:
        print('received generator exit...')
    finally:
        print('closing down...')

g = gen()
next(g)
g.close()

g = gen()
next(g)
# g.throw(GeneratorExit) # StopIteration:

print('#' * 52 + '  So, we can use `throw` to close the generator, but as the caller we now have to handle'
                 '  the exception that propagates up to us:')

g = gen()
next(g)
try:
    g.throw(GeneratorExit)
except StopIteration:
    print('silencing GeneratorExit...')
    pass
