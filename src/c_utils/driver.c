#include <stdio.h>
#include "zset.h"

int main() {
    ZSet * n = zset_new();
    zset_add(n, 0, "test");
    return 0;
}