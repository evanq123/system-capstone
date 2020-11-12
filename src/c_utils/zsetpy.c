#include "zset.h"

static ZSet * zset;

void zsetpy_init(void)
{
    zset = zset_new();
}

int zsetpy_score(char *uid, double score) 
{
    return zset_score(zset, uid, &score);
}

int zsetpy_add(double score, char *uid, double newscore)
{
    return zset_add(zset, score, uid, &newscore);
}

unsigned long zsetpy_length()
{
    return zset_length(zset);
}

int zsetpy_rank(char * uid, bool reverse){
    return zset_rank(zset, uid, reverse);
}

int zsetpy_delete(char* uid) {
    return zset_delete(zset, uid);
}

char ** zsetpy_range(double min, double max, bool minex, bool maxex)
{
    rangespec *range = malloc(sizeof(rangespec));
    range->min = min;
    range->max = max;
    range->minex = minex;
    range->maxex = maxex;

    char ** uids = zset_range(zset, &range);
    free(range);

    return uids;
}
