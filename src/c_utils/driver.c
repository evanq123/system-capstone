#include <stdio.h>
#include "zset.h"

int main() {
    ZSet * n = zset_new();
    zset_add(n, 0, "1");
    zset_add(n, 0, "2");
    printf("%ld\n", zset_length(n));
    printf("%s\n", zset_delete(n, "1") ? "True" : "False");
    printf("%s\n", zset_delete(n, "2") ? "True" : "False");
    printf("%ld\n", zset_length(n));

    zset_add(n, 0, "1");
    zset_add(n, 4, "3");
    zset_add(n, 2, "2");
    
    rangespec *range = malloc(sizeof(rangespec));
    range->min = 0;
    range->max = 4;
    range->minex = false;
    range->maxex = false;
    Array * results = zset_range(n, range);
    char ** buffer = (char **)array_get_buffer(results);
    char ** retval = malloc(sizeof(char *) * array_size(results));
    // Trim length of retval and copy
    for (int i = 0; i < array_size(results); i++) {
        retval[i] = buffer[i];
        printf("uid : %s\n", retval[i]);
    }
    array_destroy(results); // Frees Array struct but not data.

    return 0;
}