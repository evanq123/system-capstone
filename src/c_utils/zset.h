#ifndef __ZSET_H
#define __ZSET_H

#include <collectc/hashtable.h>

#include <stdbool.h>

#include "skiplist.h"

/* ZSet */
typedef struct ZSet {
    HashTable * map;
    SkipList * sl;
} ZSet;

ZSet * zset_new(void);
unsigned long zset_length(ZSet *zs);
int zset_score(ZSet *sz, char *uid, double *score);
int zset_add(ZSet *zs, double score, char *uid, double *newscore);
long zset_rank(ZSet *zs, char *uid, bool reverse);
int zset_delete(ZSet *zs, char *uid);
char ** zset_range(ZSet *zs, rangespec *range);

#endif
