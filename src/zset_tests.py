from sets import ZSet
import os
# from ctypes import *

zset = ZSet("zsetpy.so")

print(1)
zset.add("first", 0)
print(2)
zset.add("second", 1)

print(zset.size())