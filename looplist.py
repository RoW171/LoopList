__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-01-22"
__version__ = "0.1.0"


"""
simple class, which inherits from built-in 'list' and provides the use of indeces that are greater than the length of
the list.
Let's say you have a list 'l' of length 4. Normally, l[5] would raise an IndexError. If you use an EternalList you
would get l[0], since the list would start again at index 0 until the given index is reached.
"""

from collections.abc import Iterator


class LoopList(list):
    def __init__(self, item=None, iterationLooped=False):
        """
        constructor
        :param item: object(s) for the list; lists and tuples get extended, anything else appended
        """
        super(list, self).__init__()
        self._iterationLooped = iterationLooped
        if item is not None:
            if isinstance(item, (list, tuple, LoopList,)): self.extend(item)
            else: self.append(item)

    def __getitem__(self, index):
        return super().__getitem__(index % len(self))

    def __setitem__(self, index, value):
        super().__setitem__(index % len(self), value)

    def __delitem__(self, index):
        super().__delitem__(index % len(self))

    def __iter__(self):
        if not self._iterationLooped: return super().__iter__()
        else: return LoopListIterator(self)

    def pop(self, index=None):
        return super().pop(index % len(self))

    def insert(self, index, item):
        print(index, index % len(self), item)
        super().insert(index % len(self), item)


    def index(self, item, iteration=0, start=None, end=None):
        """
        :param item: item within the list
        :param iteration:
        :type iteration: int
        :type start: int
        :type end: int
        """
        return super().index(item, start, end) + (len(self) * iteration)

    def copy(self, returnType=list):
        return returnType(super().copy())


class LoopListIterator(Iterator):
    def __init__(self, source):
        self._source = source
        self._counter = -1

    def __next__(self):
        self._counter += 1
        return self._source[self._counter]


if __name__ == '__main__':
    from string import ascii_lowercase
    ll = LoopList()
    ll.extend([_ for _ in ascii_lowercase])
    print(ll)
    print(ll[4])
    print(ll[26])
    # print(ll.index('a'))
    ll.insert(255, 'ß')
    print(ll)
    ll[255] = 'hello world!"'
    print(ll)
    print(ll.pop(255))
    print(ll)
    for i in ll: print(i)
