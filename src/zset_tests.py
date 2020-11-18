from sets import ZSet
import os
from ctypes import *

# print(os.environ)

""" Expected output when running zset_tests.py
initializing zset
initializing zset
Testing persistance between two shared object of same library
Called zset_delete with persist 1
Checking persistance:initial_string
Checking persistanmce:persist 1
Called zset_delete with persist 2
Checking persistance:initial_string
Checking persistanmce:persist 2
Called zset_delete with test_remove1
Checking persistance:persist 1
Checking persistanmce:test_remove1
Called zset_add with 0.000000, test_add, 0.000000
Called zset_add with 0.000000, test_add2, 1.000000
Called zset_range with 0.000000, 1.000000, true, false
Created rangespec successfully
Called zset_length

Testing two zsets
Called zset_delete with test_remove2
Checking persistance:persist 2
Checking persistanmce:test_remove2
-1
Called zset_add with 0.000000, test_add, 0.000000
-1
Called zset_add with 0.000000, test_add2, 1.000000
-1
Called zset_range with 0.000000, 1.000000, true, false
Created rangespec successfully
['temp', 'testing', 'strings']
temp
testing
strings
Called zset_length
1
"""

zset = ZSet("zsetpy_test.so")
zset2 = ZSet("zsetpy_test2.so")

print("Testing persistance between two shared object of same library")


#----------------------------- Should print these values if running properly.
zset.remove("persist 1")    # original -> persist 1
zset2.remove("persist 2")   # original -> persist 1

zset.remove("test_remove1") # persist 1 -> test_remove1
zset.add("test_add", 0)     # test_add
zset.add("test_add2", 0, 1) # test_add2
zset.subset(0, 1, True, False)
zset.size()


print("\nTesting two zsets")
print(zset2.remove("test_remove2"))    # persist 2 -> test_remove2
print(zset2.add("test_add", 0))        # test_add
print(zset2.add("test_add2", 0, 1))    # test_add2
ret = zset2.subset(0, 1, True, False)
print(ret)
for w in ret:
    print(w)
print(zset2.size())


