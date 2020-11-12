from ctypes import *
from abc import ABC, abstractmethod

import bisect

class SortedSet(ABC):
    @abstractmethod
    def remove(self, item):
        pass
    
    @abstractmethod
    def add(self, item):
        pass
    
    @abstractmethod
    def subset(self, start, end):
        pass

    def __iter__(self):
        pass

    def __str__(self):
        return self._set.__str__()

    def __repr__(self):
        return self._set.__repr__()

class SListItem():
    def __init__(self, item, score):
        self.item = item
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

class SList(SortedSet):
    # Simple list Used for prototype.
    def __init__(self):
        self._set = list()

    def remove(self, item):
        for elem in self._set:
            uid, score = elem
            if uid == item:
                self._set.remove(elem)
                return True
        return False

    def add(self, item, score):
        # print(item, score)
        # self._set.append((int(score), item))
        # O(n) insertion because python's list is slow:
        # https://wiki.python.org/moin/TimeComplexity
        bisect.insort(self._set, SListItem(item, score))

    def subset(self, start, end):
        res = list()
        # O(n)
        # for elem in self._set:
        #     if elem.score >= start and elem.score <= end:
        #         res.append(elem.item)

        #O(2log(n) + M), M = # of matches
        left_index = bisect.bisect_left(self._set, SListItem('temp_min', start))
        right_index = bisect.bisect_right(self._set, SListItem('temp_max', end))
        for i in range(left_index, right_index):
            res.append(self._set[i].item)
        return res

    def __iter__(self):
        return self._set.__iter__()

    def __str__(self):
        return self._set.__str__()
    
    def __repr__(self):
        return self._set.__repr__()

class ZSet(SortedSet):
    # TODO shared object should be able to load multiple times.
    # We can temporarily instantiate as many zsets as we need
    # by compiling the .so under different names.
    # https://bit.ly/2JnVxaQ
    def __init__(self, zset_so_filename="zsetpy.so"):
        # TODO compile zsetpy.c -> zset_so_filename.so
        cdll.LoadLibrary(zset_so_filename)
        self._zset = CDLL(zset_so_filename)
        self._so_filename = zset_so_filename
        self._init_zset_functions()
        self._zset.zsetpy_init()

    def _init_zset_functions(self):
        #zset_init
        self._zset.zsetpy_init.restypes = None
        self._zset.zsetpy_init.argtypes = None

        #zset_score
        self._zset.zsetpy_score.restype = c_int
        self._zset.zsetpy_score.argtypes = [c_char_p, c_double]

        #zset_add
        self._zset.zsetpy_add.restype = c_int
        self._zset.zsetpy_add.argtypes = [c_double, c_char_p, c_double]

        #zset_length
        self._zset.zsetpy_length.restype = c_ulong
        self._zset.zsetpy_length.argtypes = None

        #zset_rank
        self._zset.zsetpy_rank.restype = c_int
        self._zset.zsetpy_rank.argtypes = [c_char_p, c_bool]

        #zset_length
        self._zset.zsetpy_delete.restype = c_int
        self._zset.zsetpy_delete.argtypes = [c_char_p]

        #zset_range
        self._zset.zsetpy_range.restype = POINTER(c_char_p)
        self._zset.zsetpy_range.argtypes = [c_double, c_double, c_bool, c_bool]

    def remove(self, item):
        return self._zset.zsetpy_delete(item)

    def add(self, item, score, newscore=None):
        if newscore is not None:
            return self._zset.zsetpy_add(score, item, newscore)
        return self._zset.zsetpy_add(score, item, score)

    def subset(self, start, end, include_start=True, include_end=True):
        return self._zset.zsetpy_range(start, end, include_start, include_end)
    
    def size(self):
        return self._zset.zsetpy_length()

    class ZSetIterator:
        def __init__(self, zset):
            self._zset = zset

        def __next__(self):
            # TODO generate next elem.
            pass

    def __iter__(self):
        return ZSetIterator(self._zset)

    def __str__(self):
        return "Set:'{}' has {} elements".format(self._so_filename, self.self.size())

    def __repr__(self):
        return self.__str__()