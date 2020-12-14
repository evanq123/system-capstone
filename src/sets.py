from ctypes import *
from abc import ABC, abstractmethod

import os
import bisect
#--------------------------------------------------------------------------------------------------
# SORTED SET Interface
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
        pass

    def __repr__(self):
        pass

class SListItem():
    def __init__(self, item, score):
        self.item = item
        self.score = score

    def __lt__(self, other):
        return self.score < other.score


#--------------------------------------------------------------------------------------------------
# SORTED LIST
class SList(SortedSet):
    # Simple multiset datastructure used for prototype.
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


#--------------------------------------------------------------------------------------------------
# ZSET 
class ZSetIterator:
    def __init__(self, zset):
        self._zset = zset

    def __next__(self):
        # TODO generate next elem.
        pass

class ZSet(SortedSet):
    # TODO shared object should be able to load multiple times.
    # We can temporarily instantiate as many zsets as we need
    # by compiling the .so under different names.
    # https://bit.ly/2JnVxaQ
    def __init__(self, zset_so_filename="zsetpy.so"):
        # For now, assume zsetpy.so and copy filename
        os.system("cp zsetpy.so {}".format(zset_so_filename))
        
        self._zset = CDLL(os.path.abspath(zset_so_filename))
        self._so_filename = zset_so_filename
        self._init_zset_functions()
        self._zset.zsetpy_init()

    def _init_zset_functions(self):
        #zset_init
        self._zset.zsetpy_init.restypes = None
        self._zset.zsetpy_init.argtypes = None

        #zset_score
        # self._zset.zsetpy_score.restype = c_int
        # self._zset.zsetpy_score.argtypes = [c_char_p, c_double]

        #zset_add
        self._zset.zsetpy_add.restype = c_bool
        self._zset.zsetpy_add.argtypes = [c_double, c_char_p]

        #zset_length
        self._zset.zsetpy_length.restype = c_ulong
        self._zset.zsetpy_length.argtypes = None

        #zset_rank
        # self._zset.zsetpy_rank.restype = c_int
        # self._zset.zsetpy_rank.argtypes = [c_char_p, c_bool]

        #zset_delete
        self._zset.zsetpy_delete.restype = c_bool
        self._zset.zsetpy_delete.argtypes = [c_char_p]

        #zset_range
        self._zset.zsetpy_range.restype = POINTER(c_char_p)
        self._zset.zsetpy_range.argtypes = [c_double, c_double, c_bool, c_bool]

    def remove(self, item):
        # TODO Needed to create buffer for item, possible issue may arise?
        # esp. with non null characters in string buffer.
        item_arr = create_string_buffer(item.encode(), len(item))
        # print(repr(item_arr.raw))
        return self._zset.zsetpy_delete(item_arr)

    def add(self, item, score):
        item_arr = create_string_buffer(item.encode(), len(item))
        return self._zset.zsetpy_add(score, item_arr)

    def subset(self, start, end, exclude_start=False, exclude_end=False):
        # pointer of bytes
        ptrs = self._zset.zsetpy_range(start, end, exclude_start, exclude_end)
        res = []
        for b in ptrs:
            if b is None:
                break
            res.append(b.decode())

        return res
    
    def size(self):
        return self._zset.zsetpy_length()

    def __iter__(self):
        return ZSetIterator(self._zset)

    def __str__(self):
        return "Set:'{}' has {} elements".format(self._so_filename, self.self.size())

    def __repr__(self):
        return self.__str__()