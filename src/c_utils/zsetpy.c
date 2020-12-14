#include "zset.h"

#include <string.h>
#include <stdio.h>

static ZSet * zset;

void zsetpy_init(void)
{
    zset = zset_new();
}

// int zsetpy_score(char *puid, double score) 
// {
//     char * uid = malloc(sizeof(char) * strlen(puid));
//     uid = strcpy(uid, puid);
//     return zset_score(zset, uid, &score);
// }

int zsetpy_add(double score, char *puid)
{
    char * uid = malloc(sizeof(char) * strlen(puid));
    uid = strcpy(uid, puid);
    
    return zset_add(zset, score, uid);
}

unsigned long zsetpy_length()
{
    return zset_length(zset);
}

// int zsetpy_rank(char * puid, bool reverse){
//     char * uid = malloc(sizeof(char) * strlen(puid));
//     uid = strcpy(uid, puid);
//     return zset_rank(zset, uid, reverse);
// }

int zsetpy_delete(char* puid) {
    char * uid = malloc(sizeof(char) * strlen(puid));
    uid = strcpy(uid, puid);
    return zset_delete(zset, uid);
}

char ** zsetpy_range(double min, double max, bool minex, bool maxex)
{
    rangespec *range = malloc(sizeof(rangespec));
    range->min = min;
    range->max = max;
    range->minex = minex;
    range->maxex = maxex;

    Array * results = zset_range(zset, range);
    free(range);

    char ** buffer = (char **)array_get_buffer(results);
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
