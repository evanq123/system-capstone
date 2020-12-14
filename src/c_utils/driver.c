#include <stdio.h>
#include "zset.h"

char ** zsetpy_range2(ZSet *zset, double min, double max, double *replylen, bool minex, bool maxex)
{
    rangespec *range = malloc(sizeof(rangespec));
    range->min = min;
    range->max = max;
    range->minex = minex;
    range->maxex = maxex;

    Array * results = zset_range(zset, range);
    free(range);

    char ** buffer = (char **)array_get_buffer(results);
    replylen[0] = array_size(results);
    printf("reply 1: %f\n", replylen[0]);
    char ** uids = malloc(sizeof(char *) * array_size(results));
    // Trim length of retval and copy
    for (int i = 0; i < array_size(results); i++) {
        uids[i] = buffer[i];
    }
    array_destroy(results); // Frees Array struct but not data.

    // TODO, uids are not free'd since it is sent to python.
    // might cause memory leak, but we'll see.
    return uids; 
}

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
    double * replylen = malloc(sizeof(double));
    char ** results = zsetpy_range2(n, 0, 4, replylen, false, false);
    printf("reply 2: %f\n", replylen[0]);
    for (int i = 0; i < replylen[0]; i++) {
        printf("uid %s\n", results[i]);
    }
    return 0;
}


