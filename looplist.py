#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__credits__ = ["Robin Weiland", ]
__copyright__ = "Copyright 2019, Robin Weiland"

__date__ = "2019-01-22"
__version__ = "0.1.0"
__license__ = "MIT"

__status__ = "In Development"
__maintainer__ = "Robin Weiland"


__doc__ = """Provides a simple class, which inherits from built-in 'list' and allowing the use of indeces
that are greater than the length of the list.
Let's say you have a list 'l' of length 4. Normally, l[5] would raise an IndexError. Using a LoopList gets
you l[0], since the list would wrap around and start again at index 0 until the given index is reached."""

__all__ = ["LoopList"]

from collections.abc import Iterator


class LoopList(list):
    __doc__ = __doc__

    def __init__(self, item=None, iterationLooped=False):
        """
        :param item: object(s) for the list; lists and tuples get extended, anything else appended
        :var _iterationLooped: determines wether iterating over the list stops at the end or
                               wraps around and continously repeat (more on that at LoppedList.__iter__())
        """
        super(LoopList, self).__init__()
        self._iterationLooped = iterationLooped
        if item is not None:
            if isinstance(item, (list, tuple, LoopList,)): self.extend(item)
            else: self.append(item)

    def __getitem__(self, index):
        """
        The 'looping' is based on calculating the modulo of index and the length of the list
        Same behaviour(except looping) as list.__getitem__() builtin method. Consult its docs for details
        :param index: index of the item to get
        :type index: int
        :return: item at index
        """
        return super().__getitem__(index % len(self))

    def __setitem__(self, index, value):
        """
        Basicly the same looping system as LoopList.__getitem__()
        Same behaviour(except looping) as list.__setitem__() builtin method. Consult its docs for details
        :param index: index of the item to change
        :var index: int
        :param value: the value the index is changed into
        :type value: anything a builtin list can take
        """
        super().__setitem__(index % len(self), value)

    def __delitem__(self, index):
        """
        Same behaviour(except looping) as list.__delitem__() builtin method. Consult its docs for details
        :param index: index to delete
        :type index: int
        """
        super().__delitem__(index % len(self))

    def __iter__(self):
        """
        defines '_ for _ in LoopList()' - behaviour
        Example:
            'iterationLooped' was set False in the constructor [default]:
                ll = LoopList([0, 1, 2, ])
                for item in ll: print(item)

                -->
                0
                1
                2


            'iterationLooped' was set True in the constructor:
                ll = LoopList([0, 1, 2, ])
                for item in ll: print(item)

                -->
                0
                1
                2
                0
                1
                2
                0
                ...

        Keep in mind to set up 'iterationLooped' according to your intended use
        :return: Iterator
        """
        if not self._iterationLooped: return super().__iter__()
        else: return LoopListIterator(self)

    def pop(self, index=None):
        """
        Gets the item at the given index and also deletes it from the list
        Example:
            ll = LoopList([0, 1, 2, 3, 4, 5, ])
            ll.pop(2)  --> returns 2 and alters ll to [0, 1, 3, 4, 5, ]
            ll.pop(22)  --> returns 3 and alters ll to [0, 1, 4, 5, ]
        Same behaviour(except wrapping) as list.pop() builtin method. Consult its docs for details
        :param index: index of the item to return
        :type index: int
        :return: item at index
        """
        return super().pop(index % len(self))

    def insert(self, index, item):
        """
        Probably simillar to LoopList.__setitem__()
        Same behaviour(except wrapping) as list.insert() builtin method. Consult its docs for details
        :param index: index on which 'item' gets inserted
        :type index: int
        :param item: the object to insert
        :type item: anything a builtin list can take
        """
        super().insert(index % len(self), item)


    def index(self, item, iteration=0, start=None, end=None):
        """
        Seeks the index of 'item' in the list and simulates a given number of iterations on it
        Example:
            ll = LoopList([1, 2, 3, ])
            ll.index(2)  --> returns 1
            ll.index(2, 5)
        Same behaviour(except iteration) as list.index() builtin method. Consult its docs for details
        :param item: item within the list
        :param iteration:
        :type iteration: int
        :type start: int
        :type end: int
        :return: index of 'item' in the list
        """
        # FIXME: currently doesn't work [TypeError: slice indices must be integers or None or have an __index__ method]
        raise NotImplementedError('This method behaves unexpectedly and is currently under rework')
        # noinspection PyUnreachableCode
        # return super().index(item, start % len(self), end % len(self)) + (len(self) * iteration)
        return super().index(item, start, end) + (len(self) * iteration)

    def copy(self, returnType=list):
        """
        Creates a shallow copy of the object and converts it in the given datatype
        Same behaviour(except conversion) as list.copy() builtin method. Consult its docs for details
        :param returnType: datatype of the returned copy
        :type returnType: LoopList, list, tuple
        :return: copy of the current LoopList converted into the selected datatype
        """
        return returnType(super().copy())


class LoopListIterator(Iterator):
    """Iterator class for LoopedList. Used in LoopedList.__iter__()"""
    def __init__(self, source):
        """
        :param source: object to iterate through
        :type source: LoopList
        :var: _counter: used to infinitly loop by adding to it in each iteration
        """
        self._source = source
        self._counter = -1

    def __next__(self):
        """:return: next item of the LoopedList"""
        self._counter += 1
        return self._source[self._counter]


if __name__ == '__main__': pass
