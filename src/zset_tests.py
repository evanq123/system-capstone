from sets import ZSet
import os
# from ctypes import *

zset = ZSet("zsetpy.so")

zset.add("first", 0)
zset.add("second", 1)

print(zset.size())

print(zset.subset(0, 1))