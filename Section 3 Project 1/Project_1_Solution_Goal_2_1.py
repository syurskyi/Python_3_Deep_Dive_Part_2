class Polygons:
    def __init__(self, m, R):
        if m < 3:
            raise ValueError('m must be greater than 3')
        self._m = m
        self._R = R

    def __len__(self):
        return self._m - 2

    def __repr__(self):
        return f'Polygons(m={self._m}, R={self._R})'


# polygons = Polygons(2, 10)  # ValueError: m must be greater than 3

polygons = Polygons(3, 1)
print(len(polygons))

polygons = Polygons(6, 1)
print(len(polygons))

print('#' * 52 + '  Lets also test the representation:')

print(polygons)