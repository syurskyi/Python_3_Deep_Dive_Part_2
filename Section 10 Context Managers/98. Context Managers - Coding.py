print('#' * 52 + '  You should be familiar with `try` and `finally`.')

try:
    10 / 2
except ZeroDivisionError:
    print('Zero division exception occurred')
finally:
    print('finally ran!')

print('#' * 52 + '  ')

try:
    1 / 0
except ZeroDivisionError:
    print('Zero division exception occurred')
finally:
    print('finally ran!')

print('#' * 52 + '  You will see that in both instances, the `finally` block was executed.'
                 '  Even if an exception is raised in the `except` block, the `finally` block will **still** execute!')

print(
    '#' * 52 + 'Even if the finally is in a function and there is a return statement in the `try` or `except` blocks:')


def my_func():
    try:
        1 / 0
    except:
        return
    finally:
        print('finally running...')

my_func()

print('#' * 52 + '  This is very handy to release resources even in cases where an exception occurs. ')
print('#' * 52 + '  For example making sure a file is closed after being opened:')

try:
    f = open('test.txt', 'w')
    a = 1 / 0
except:
    print('an exception occurred...')
finally:
    print('Closing file...')
    f.close()

print('#' * 52 + '  We should **always** do that when dealing with files.')
print('#' * 52 + '  ')
print('#' * 52 + '  When we use context managers in conjunction with the `with` statement,'
                 '  we end up with the "cleanup" phase happening as soon as the `with` statement finishes:')

with open('test.txt', 'w') as file:
    print('inside with: file closed?', file.closed)
print('after with: file closed?', file.closed)

print('#' * 52 + '  This works even in this case:')

def test():
    with open('test.txt', 'w') as file:
        print('inside with: file closed?', file.closed)
        return file

file = test()
print(file.closed)

print('#' * 52 + '  And yet, the file was still closed.')
print('#' * 52 + '  It also works even if we have an exception in the middle of the block')

# with open('test.txt', 'w') as f:
#     print('inside with: file closed?', f.closed)
#     raise ValueError()                              ###### ValueError:

print('after with: file closed?', f.closed)

print('#' * 52 + '  ')
print('#' * 52 + '  ')
print('#' * 52 + '  ')

def my_func():
    return 1.0 / 0.0

# my_func()  # ZeroDivisionError: float division by zero

print('#' * 52 + '  Lets go ahead and create a context manager:')


class MyContext:
    def __init__(self):
        self.obj = None

    def __enter__(self):
        print('entering context...')
        self.obj = 'the Return Object'
        return self.obj

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('exiting context...')
        if exc_type:
            print(f'*** Error occurred: {exc_type}, {exc_value}')
        return False  # do not suppress exceptions

# with MyContext() as obj:
#     raise ValueError    # ValueError:

print('#' * 52 + '  As you can see, the `__exit__` method was still called -'
                 '  which is exactly what we wanted in the first place.')
print('#' * 52 + '   Also, the exception that was raise inside the `with` block is seen.')
print('#' * 52 + '  We can change that by returning `True` from the `__exit__` method:')


class MyContext:
    def __init__(self):
        self.obj = None

    def __enter__(self):
        print('entering context...')
        self.obj = 'the Return Object'
        return self.obj

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('exiting context...')
        if exc_type:
            print(f'*** Error occurred: {exc_type}, {exc_value}')
        return True  # suppress exceptions

with MyContext() as obj:
    raise ValueError
print('reached here without an exception...')

print('#' * 52 + '  Look at the output of this code:')

with MyContext() as obj:
    print('running inside with block...')
    print(obj)
print(obj)

print('#' * 52 + '  Notice that the `obj` we obtained from the context manager,'
                 '  still exists in our scope after the `with` statement.')
print('#' * 52 + '  The `with` statement does **not** have its own local scope - its not a function!')
print('#' * 52 + '  However, the context manager could manipulate the object returned by the context manager:')

class Resource:
    def __init__(self, name):
        self.name = name
        self.state = None


class ResourceManager:
    def __init__(self, name):
        self.name = name
        self.resource = None

    def __enter__(self):
        print('entering context')
        self.resource = Resource(self.name)
        self.resource.state = 'created'
        return self.resource

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('exiting context')
        self.resource.state = 'destroyed'
        if exc_type:
            print('error occurred')
        return False

with ResourceManager('spam') as res:
    print(f'{res.name} = {res.state}')
print(f'{res.name} = {res.state}')

print('#' * 52 + '  We still have access to `res`, but its internal state was changed'
                 '  by the resource managers `__exit__` method.')
print('#' * 52 + '  Although we already have a context manager for files built-in to Python,'
                 '  lets go ahead and write our own anyways - good practice.')


class File:
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode

    def __enter__(self):
        print('opening file...')
        self.file = open(self.name, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('closing file...')
        self.file.close()
        return False

with File('test.txt', 'w') as f:
    f.write('This is a late parrot!')

print('#' * 52 + '  Even if we have an exception inside the `with` statement, our file will still get closed.')
print('#' * 52 + '  Same applies if we return out of the `with` block if we are inside a function:')

def test():
    with File('test.txt', 'w') as f:
        f.write('This is a late parrot')
        if True:
            return f
        print(f.closed)
    print(f.closed)

f = test()

print('#' * 52 + '  Note that the `__enter__` method can return anything, including the context manager itself.')
print('#' * 52 + '  If we wanted to, we could re-write our file context manager this way:')


class File():
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode

    def __enter__(self):
        print('opening file...')
        self.file = open(self.name, self.mode)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('closing file...')
        self.file.close()
        return False

with File('test.txt', 'r') as file_ctx:
    print(next(file_ctx.file))
    print(file_ctx.name)
    print(file_ctx.mode)