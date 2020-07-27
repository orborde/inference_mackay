import random

class FwdBackSampler:
    def __init__(self, seed, choices):
        self._choices = choices
        self._rand = random.Random(seed)
        self._items = {0: self._choice()}

    def _choice(self):
        return self._rand.choice(self._choices)

    def _extent(self):
        amin = min(self._items.keys())
        amax = max(self._items.keys())
        return amin, amax

    def _radius(self):
        return min(map(abs, self._extent()))

    def _extend(self):
        amin, amax = map(abs, self._extent())

        if amax > amin:
            assert amax == amin+1
            self._items[-amin-1] = self._choice()
        else:
            assert amax == amin
            self._items[amax+1] = self._choice()

    def sample(self, t):
        while self._radius() < abs(t):
            print(self._radius(), self._extent(), 'extending to', t)
            self._extend()

        return self._items[t]

f=FwdBackSampler(1337, 'abc')
data = [f.sample(t) for t in range(-10, 10)]
print(data)
