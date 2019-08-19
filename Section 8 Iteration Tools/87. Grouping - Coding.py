print('#' * 52 + '  ### Grouping')

import itertools

with open('cars_2014.csv') as f:
    for row in itertools.islice(f, 0, 20):
        print(row, end='')

print('#' * 52 + '  Trivial to do with SQL, but a little more work with Python.')

from collections import defaultdict

makes = defaultdict(int)

with open('cars_2014.csv') as f:
    next(f)  # skip header row
    for row in f:
        make, _ = row.strip('\n').split(',')
        makes[make] += 1

for key, value in makes.items():
    print(f'{key}: {value}')

print('#' * 52 + '  Instead of doing all this, we could use the `groupby` function in `itertools`.')
print('#' * 52 + '  Again, it is a lazy iterator, so we will use lists to see whats happening -'
                 '  but lets use a slightly smaller data set as an example first:')

data = (1, 1, 2, 2, 3)
print(list(itertools.groupby(data)))

print('#' * 52 + '  As you can see, we ended up with an iterable of tuples.')
print('#' * 52 + '   The tuple was the groups of numbers in data, so `1`, `2`, and `3`')
print('#' * 52 + '   But what is in the second element of the tuple? Well its an iterator, but what does it contain?')

it = itertools.groupby(data)
for group in it:
    print(group[0], list(group[1]))

print('#' * 52 + '  Basically it just contained the grouped elements themselves.')
print('#' * 52 + '  This might seem a bit confusing at first - so lets look at the second optional'
                 '  argument of group by - it is a key.')
print('#' * 52 + '  Basically the idea behind that key is the same as the sort keys,'
                 '  or filter keys we have worked with in the past.')
print('#' * 52 + '  It is a **function** that returns a grouping key.')

data = (
    (1, 'abc'),
    (1, 'bcd'),

    (2, 'pyt'),
    (2, 'yth'),
    (2, 'tho'),

    (3, 'hon')
)

groups = list(itertools.groupby(data, key=lambda x: x[0]))

print(groups)

print('#' * 52 + '  Once again you will notice that we have the group keys, and some iterable.')
print('#' * 52 + '   Lets see what those contain:')

groups = itertools.groupby(data, key=lambda x: x[0])
for group in groups:
    print(group[0], list(group[1]))

print('#' * 52 + '  So now lets go back to our car make example.')
print('#' * 52 + '  We want to get all the makes and how many models are in each make.')

with open('cars_2014.csv') as f:
    make_groups = itertools.groupby(f, key=lambda x: x.split(',')[0])

# list(itertools.islice(make_groups, 5)) # ValueError: I/O operation on closed file.

print('#' * 52 + '  Whats going on?')

print('#' * 52 + '  Remember that `groupby` is a **lazy** iterator. '
                 ' This means it did not actually do any work when we called it apart from setting up the iterator.')
print('#' * 52 + '  When we called `list()` on that iterator, **then** it went ahead and try to do the iteration.')
print('#' * 52 + '  However, our `with` (context manager) closed the file by then!')
print('#' * 52 + '  So we will need to do our work inside the context manager.')

with open('cars_2014.csv') as f:
    next(f)  # skip header row
    make_groups = itertools.groupby(f, key=lambda x: x.split(',')[0])
    print(list(itertools.islice(make_groups, 5)))

print('#' * 52 + '  Next, we need to know how many items are in each `itertools._grouper` iterators.')
print('#' * 52 + '  How about using the `len()` property of the iterator?')

# with open('cars_2014.csv') as f:
#     next(f)  # skip header row
#     make_groups = itertools.groupby(f, key=lambda x: x.split(',')[0])
#     make_counts = ((key, len(models)) for key, models in make_groups)
#     print(list(make_counts))  # TypeError: object of type 'itertools._grouper' has no len()

print('#' * 52 + '  Aww... Iterators dont necessarily implement a `__len__` method - and this one definitely does not.')
print('#' * 52 + ' Well, if we think about this, we could simply "replace" each element in the models, '
                 ' with 1, and sum that up ')

with open('cars_2014.csv') as f:
    next(f)  # skip header row
    make_groups = itertools.groupby(f, key=lambda x: x.split(',')[0])
    make_counts = ((key, sum(1 for model in models))
                    for key, models in make_groups)
    print(list(make_counts))

print('#' * 52 + '  #### Caveat')

groups = list(itertools.groupby(data, key=lambda x: x[0]))
for group in groups:
    print(group[0], group[1])

print('#' * 52 + '  Ok, so this looks fine - we now have a list containing tuples - the first element is the group key'
                 '  the second is an iterator - we can ceck that easily:')

it = groups[0][1]
print(iter(it) is it)

print('#' * 52 + '  So yes, this is an iterator - what is in it?')

print(list(it))

print('#' * 52 + '  Empty?? But we did not iterate through it - what happened?')

groups = list(itertools.groupby(data, key=lambda x: x[0]))
for group in groups:
    print(group[0], list(group[1]))

print('#' * 52 + '  So, the 3rd element is OK, but looks like the first two got exhausted somehow...')
print('#' * 52 + '  Lets make sure they are indeed exhausted:')

groups = list(itertools.groupby(data, key=lambda x: x[0]))
# next(groups[0][1])   # StopIteration:
# next(groups[1][1])   # StopIteration:
print(next(groups[2][1]))

print('#' * 52 + '  So, yes, the first two were exhausted when we converted the groups to a list.')
print('#' * 52 + '  The solution here is actually in the Python docs')
print('#' * 52 + '  The key thing here is that the elements yielded from the different groups are using'
                 '  the **same** undelying iterable over all the elements.')
print('#' * 52 + '  As the documentation states, when we advance to the next group, the previous ones iterator is'
                 '  automatically exhausted - it basically iterates over all the elements'
                 '  until it hits the next group key.')

groups = itertools.groupby(data, key=lambda x: x[0])
group1 = next(groups)

print(group1)

print('#' * 52 + '  And the iterator in the tuple is not exhausted:')

print(next(group1[1]))

print('#' * 52 + '  Now, lets try again, but this time we will advance to group2,'
                 '  and see what is in `group1`s iterator:')

groups = itertools.groupby(data, key=lambda x: x[0])
group1 = next(groups)
group2 = next(groups)

print('#' * 52 + '  Now `group1`s iterator has been exhausted (because we moved to `group2`):')

# print(next(group1[1]))  # StopIteration:
print('#' * 52 + '  But `group2` s iterator is still OK:')

print(next(group2[1]))

print('#' * 52 + '  We know that there are still two elements in `group2`, so lets advance to `group3`'
                 '  and go back and see whats left in `group2` s iterator:')

group3 = next(groups)

# next(group2[1]) # StopIteration:
print('#' * 52 + '  But `group3` s iterator is just fine:')

print(next(group3[1]))

print('#' * 52 + '  So, just be careful here with the `groupby()` - if you want to save all the data into'
                 '  a list you cannot first convert the groups into a list -'
                 '  you **must** step through the groups iterator,')
print('#' * 52 + '  and retrieve each individual iterators elements into a list,'
                 '  the way we did it in the first example, or simply using a comprehension:')

groups = itertools.groupby(data, key=lambda x: x[0])
groups_list = [(key, list(items)) for key, items in groups]
print(groups_list)







