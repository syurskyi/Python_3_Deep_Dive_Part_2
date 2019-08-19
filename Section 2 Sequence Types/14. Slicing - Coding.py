s = slice(0, 2)

print(type(s))

print(s.start)

print(s.stop)

l = [1, 2, 3, 4, 5]
print(l[s])

data = []  # a collection of rows, read from a file maybe
for row in data:
    first_name = row[0:51]
    last_name = row[51:101]
    ssn = row[101:111]
    # etc

range_first_name = slice(0, 51)
range_last_name = slice(51, 101)
range_ssn = slice(101, 111)

for row in data:
    first_name = row[range_first_name]
    last_name = row[range_last_name]
    ssn = row[range_ssn]


print('#' * 52 + ' Additionally, extended slicing allows specifying a step value:')
l = 'python'
print(l[0:6:2], l[0:6:3])

print('#' * 52 + ' And extended slices can also be defined using `slice`:')
s1 = slice(0, 6, 2)
s2 = slice(0, 6, 3)
print(l[s1], l[s2])

print('#' * 52 + ' Unlike regular indexing (e.g. `l[n]`), its OK for slice indexes to be "out of bounds":')
l = [1, 2, 3, 4, 5, 6]
print(l[0:100])
print(l[-10:100])

print('#' * 52 + ' But regular indexing will raise exceptions for out of bound errors:')
# l = [1, 2, 3, 4, 5, 6]
# l[100]
# IndexError                                Traceback (most recent call last)
# <ipython-input-14-17c89fd6f29e> in <module>()
#       1 l = [1, 2, 3, 4, 5, 6]
# ----> 2 l[100]
#
# IndexError: list index out of range


print('#' * 52 + 'In slicing, if we do not specify the start/end index, Python will automatically use the start/end '
                 'of the sequence we are slicing: ')
l = [1, 2, 3, 4, 5, 6]
print(l[:4])
print(l[4:])

print('#' * 52 + ' In fact, we can omit both:')
print(l[:])

print('#' * 52 + 'In addition to the start/stop values allowing for negative values, the step value can also be '
                 'negative. This simply means the sequence will traversed in the opposite direction: ')
l = [0, 1, 2, 3, 4, 5]
print(l[3:0:-1])

print('#' * 52 + 'If we wanted to include the `0` index element, we could do it by ommitting the end value: ')
print(l[3::-1])

print('#' * 52 + ' We could also do the following:')
print(l[3:-100:-1])

print('#' * 52 + ' But this would not work as expected: ')
print(l[3:-1:-1])

# Remember from the lecture that this range equivalence would be:
# `3 --> 3`
# `-1 < 0 --> max(-1, 6-1) --> max(-1, 5) --> 5`
# so equivalent range would be given by:

print(list(range(3, 5, -1)))

print('#' * 52 + ' Easily Converting a Slice to a Range')
print(slice(1, 5).indices(10))
print(list(range(1, 5, 1)))

l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(l[1:5])

print('#' * 52 + ' The `slice` object can also handle extended slicing: ')
print(slice(0, 100, 2).indices(10))
print(list(range(0, 10, 2)))
print(l[0:100:2])

print('#' * 52 + 'We can easily retrieve a list of indices from a slice by passing the unpacked tuple returned by the'
                 ' `indices` method to the range functions arguments and converting to a list: ')
print(list(range(*slice(None, None, -1).indices(10))))

print('#' * 52 + ' As we can see from this example, using a slice such as `[::-1]` returns the a sequence that is '
                 'in reverse order from the original one. ')

print(l)
print(l[::])
print(l[::-1])
