print('#' * 52 + '  ### Yield From')


def matrix(n):
    gen = ((i * j for j in range(1, n + 1))
           for i in range(1, n + 1)
           )
    return gen


m = list(matrix(5))

print(m)

print('#' * 52 + '  Suppose we want an iterator to iterate over all the values of the matrix, element by element.')


def matrix_iterator(n):
    for row in matrix(n):
        for item in row:
            yield item


for i in matrix_iterator(3):
    print(i)

print('#' * 52 + '  But we can avoid using that nested for loop by using a special form of `yield`: `yield from`')


def matrix_iterator(n):
    for row in matrix(n):
        yield from row


for i in matrix_iterator(3):
    print(i)

print('#' * 52 + '  Here is an example where using `yield from` can be quite effective.')
print('#' * 52 + '  In this example we need to read car brands from multiple files to get it as a single collection.')

brands = []

with open('car-brands-1.txt') as f:
    for brand in f:
        brands.append(brand.strip('\n'))

with open('car-brands-2.txt') as f:
    for brand in f:
        brands.append(brand.strip('\n'))

with open('car-brands-3.txt') as f:
    for brand in f:
        brands.append(brand.strip('\n'))

for brand in brands:
    print(brand, end=', ')

print('#' * 52 + '  ')

print('#' * 52 + '  But notice that we had to load up the entire data set in memory.')
print('#' * 52 + '  As we have discussed before this is not very efficient.')
print('#' * 52 + '  Instead we could use a generator approach as follows:')


def brands(*files):
    for f_name in files:
        with open(f_name) as f:
            for line in f:
                yield line.strip('\n')


files = 'car-brands-1.txt', 'car-brands-2.txt', 'car-brands-3.txt'
for brand in brands(*files):
    print(brand, end=', ')

print('#' * 52 + '  ')

print('#' * 52 + '  We can simplify our function by using `yield from`:')


def brands(*files):
    for f_name in files:
        with open(f_name) as f:
            yield from f


for brand in brands(*files):
    print(brand, end=', ')

print('#' * 52 + '  ')
print('#' * 52 + '  ')

print('#' * 52 + '  Now we still have to clean up that trailing n character...')
print(
    '#' * 52 + '  So, we are going to create generators that can read each line of the file, and yield a clean result,'
               '  and we will `yield from` that generator:')


def gen_clean_read(file):
    with open(file) as f:
        for line in f:
            yield line.strip('\n')


f1 = gen_clean_read('car-brands-1.txt')
for line in f1:
    print(line, end=', ')

print('#' * 52 + '  ')


print('#' * 52 + '  So now, we can proceed with our overarching generator function as before,'
                 '  except we will `yield from` our generators, instead of directly from the file iterator:')

files = 'car-brands-1.txt', 'car-brands-2.txt', 'car-brands-3.txt'

def brands(*files):
    for file in files:
        yield from gen_clean_read(file)

for brand in brands(*files):
    print(brand, end=', ')
    print()

print('#' * 52 + '  ')
print('#' * 52 + '  Using `yield from`:')

def brands(*files):
    for file in files:
        yield from gen_clean_read(file)

print('#' * 52 + '  Without using `yield from`:')

def brands(*files):
    for file in files:
        for line in gen_clean_read(file):
            yield line

for brand in brands(*files):
    print(brand, end=', ')


