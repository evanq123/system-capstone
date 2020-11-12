from sets import ZSet
import os
from ctypes import *

# print(os.environ)

zset = ZSet("zsetpy_test.so")
zset2 = ZSet("zsetpy_test2.so")

print("Testing persistance between two shared object of same library")


#----------------------------- Should print these values if running properly.
zset.remove("persist 1")    # original -> persist 1
zset2.remove("persist 2")   # original -> persist 1

# TODO incorrect resutls; I believe ctypes.create_string_buffer() is only creating
# 1 dynamically allocated memory. Thus, everytime create_string_buffer is called,
# the new value is placed into the old buffer, and thus the string does not persist.
zset.remove("test_remove1") # persist 1 -> test_remove1
zset.add("test_add", 0)     # test_add
zset.add("test_add2", 0, 1) # test_add2
zset.subset(0, 1, True, False)
zset.size()


print("\nTesting two zsets")
zset2.remove("test_remove2")    # persist 2 -> test_remove2
zset2.add("test_add", 0)        # test_add
zset2.add("test_add2", 0, 1)    # test_add2
zset2.subset(0, 1, True, False)
zset2.size()
