from collections import deque

dq = deque([1, 2, 3, 4, 5])
print(dq)

dq.append(100)
print(dq)
print(dq)

dq.appendleft(-10)
print(dq)
print(dq.pop())

print(dq)
print(dq.popleft())
print(dq)

print('#' * 52 + '  We can create a capped queue')

dq = deque([1, 2, 3, 4], maxlen=5)

dq.append(100)
print(dq)

dq.append(200)
print(dq)

dq.append(300)
print(dq)

print('#' * 52 + '  As you can see the first item (`2`) was automatically discarded from the left of the queue'
                 '  when we added `300` to the right.')

print('#' * 52 + '  We can also find the number of elements in the queue by using the `len()` function:')

print(len(dq))

print('#' * 52 + '  as well as query the `maxlen`:')
print(dq.maxlen)

print('#' * 52 + '  Now lets create an empty queue, and write two functions - one that will add elements to the queue,'
                 '  and one that will consume elements from the queue:')

def produce_elements(dq):
    for i in range(1, 36):
        dq.appendleft(i)

def consume_elements(dq):
    while len(dq) > 0:
        item = dq.pop()
        print('processing item', item)

def coordinator():
    dq = deque()
    producer = produce_elements(dq)
    consume_elements(dq)

coordinator()

print('#' * 52 + '  We will use a capped `deque`, and change our producer and consumers slightly, ')
print('#' * 52 + '  so that each one does its work, the yields control back to the caller once its done with its work')
print('#' * 52 + '  - the producer adding elements to the queue,'
                 '  and the consumer removing and processing elements from the queue:')


def produce_elements(dq, n):
    for i in range(1, n):
        dq.appendleft(i)
        if len(dq) == dq.maxlen:
            print('queue full - yielding control')
            yield


def consume_elements(dq):
    while True:
        while len(dq) > 0:
            print('processing ', dq.pop())
        print('queue empty - yielding control')
        yield


def coordinator():
    dq = deque(maxlen=10)
    producer = produce_elements(dq, 36)
    consumer = consume_elements(dq)
    while True:
        try:
            print('producing...')
            next(producer)
        except StopIteration:
            # producer finished
            break
        finally:
            print('consuming...')
            next(consumer)

coordinator()

print('#' * 52 + '  ### Timings using Lists and Deques for Queues')

from timeit import timeit

list_size = 10_000


def append_to_list(n=list_size):
    lst = []
    for i in range(n):
        lst.append(i)


def insert_front_of_list(n=list_size):
    lst = []
    for i in range(n):
        lst.insert(0, i)


lst = [i for i in range(list_size)]


def pop_from_list(lst=lst):
    for _ in range(len(lst)):
        lst.pop()


lst = [i for i in range(list_size)]


def pop_from_front_of_list(lst=lst):
    for _ in range(len(lst)):
        lst.pop(0)

print(timeit('append_to_list()', globals=globals(), number=1_000))
print(timeit('insert_front_of_list()', globals=globals(), number=1_000))
print(timeit('pop_from_list()', globals=globals(), number=1_000))
print(timeit('pop_from_front_of_list()', globals=globals(), number=1_000))

print('#' * 52 + '  As you can see, '
                 '  insert elements at the front of the list is not very efficient compared to the end of the list.')
print('#' * 52 + '  So lists are OK to use as stacks, but not as queues.')
print('#' * 52 + '  The standard library is `deque` is efficient at adding/removing items from both'
                 '  the start and end of the collection:')

from collections import deque

list_size = 10_000


def append_to_deque(n=list_size):
    dq = deque()
    for i in range(n):
        dq.append(i)


def insert_front_of_deque(n=list_size):
    dq = deque()
    for i in range(n):
        dq.appendleft(i)


dq = deque(i for i in range(list_size))


def pop_from_deque(dq=dq):
    for _ in range(len(lst)):
        dq.pop()


dq = deque(i for i in range(list_size))


def pop_from_front_of_deque(dq=dq):
    for _ in range(len(lst)):
        dq.popleft()

print(timeit('append_to_deque()', globals=globals(), number=1_000))
print(timeit('insert_front_of_deque()', globals=globals(), number=1_000))
print(timeit('pop_from_deque()', globals=globals(), number=1_000))
print(timeit('pop_from_front_of_deque()', globals=globals(), number=1_000))