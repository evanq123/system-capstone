from sets import ZSet
import os

# print(os.environ)

zset = ZSet("zsetpy_test.so")
zset2 = ZSet("zsetpy_test2.so")

print("Testing persistance between two shared object of same library")
zset.remove("persist 1")
zset2.remove("persist 2")

print("\nTesting 1 zset")

zset.remove("test_remove")
zset.add("test_add", 0)
zset.add("test_add2", 0, 1)
zset.subset(0, 1, True, False)
zset.size()


print("\nTesting two zsets")
zset2.remove("test_remove")
zset2.add("test_add", 0)
zset2.add("test_add2", 0, 1)
zset2.subset(0, 1, True, False)
zset2.size()
