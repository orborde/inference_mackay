import random

class FwdBackSampler:
    def __init__(self, chooser):
        self._chooser = chooser
        self._items = {0: self._chooser.choice()}

    def _extent(self):
        amin = min(self._items.keys())
        amax = max(self._items.keys())
        return amin, amax

    def _radius(self):
        return min(map(abs, self._extent()))

    def _extend(self):
        amin, amax = map(abs, self._extent())

        choice = self._chooser.choice()
        print(self._radius(), self._extent(), 'extending with', choice)
        if amax > amin:
            assert amax == amin+1
            self._items[-amin-1] = choice
        else:
            assert amax == amin
            self._items[amax+1] = choice

    def sample(self, t):
        while self._radius() < abs(t):
            self._extend()

        return self._items[t]

class ListChooser:
    def __init__(self, items):
        self._queue = list(reversed(items))

    def choice(self):
        return self._queue.pop()

f=FwdBackSampler(ListChooser('abcdefghijklmnopqrstuvwxyz'))
data = [f.sample(t) for t in range(-10, 10)]
assert ''.join(data) == 'usqomkigecabdfhjlnpr', data
print(data)
