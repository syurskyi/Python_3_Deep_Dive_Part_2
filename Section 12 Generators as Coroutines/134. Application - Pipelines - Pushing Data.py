print('#' * 52 + '  ### Pipelines - Pushing Data')

print('#' * 52 + '  We can also create pipelines where we **push** data through multiple stages of this pipeline,'
                 '  using `send`, so, essentially, using coroutines.')


def coroutine(coro):
    def inner(*args, **kwargs):
        gen = coro(*args, **kwargs)
        next(gen)
        return gen

    return inner


@coroutine
def handle_data():
    while True:
        received = yield
        print(received)


import math


@coroutine
def power_up(n, next_gen):
    while True:
        received = yield
        output = math.pow(received, n)
        next_gen.send(output)

print_data = handle_data()
gen = power_up(2, print_data)
# pipeline: gen --> print_data
for i in range(1, 6):
    gen.send(i)

print('#' * 52 + '  Ok, as you can see we are now **pushing** data through this pipeline.')
print('#' * 52 + '  But why stop there? Lets add another `power_up` in the pipeline:')

print_data = handle_data()
gen2 = power_up(3, print_data)
gen1 = power_up(2, gen2)
# pipeline: gen1 --> gen2 --> print_data
for i in range(1, 6):
    gen1.send(i)

print('#' * 52 + '  Now lets add a filter to our pipeline that will only retain even values:')

@coroutine
def filter_even(next_gen):
    while True:
        received = yield
        if received %2 == 0:
            next_gen.send(received)

print_data = handle_data()
filtered = filter_even(print_data)
gen2 = power_up(3, filtered)
gen1 = power_up(2, gen2)

# pipeline: gen1 --> gen2 --> filtered --> print_data

for i in range(1, 6):
    gen1.send(i)