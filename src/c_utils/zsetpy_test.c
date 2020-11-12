// #include "zset.h"

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

// static ZSet * zset;

// TODO remove this definition
typedef struct {
    double min, max;
    bool minex, maxex; /* are min or max exclusive? */
} rangespec;

void zsetpy_init(void)
{
    puts("initializing zset");
    // zset = zset_new();
}

int zsetpy_score(char *uid, double score) 
{
    printf("Called zset_score with %s, %f\n", uid, score);
    return -1;
    // return zset_score(zset, uid, &score);
}

int zsetpy_add(double score, char *uid, double newscore)
{
    printf("Called zset_add with %f, %s, %f\n", score, uid, newscore);
    return -1;
    // return zset_add(zset, score, uid, &newscore);
}

unsigned long zsetpy_length()
{
    puts("Called zset_length");
    return -1;
    // return zset_length(zset);
}

int zsetpy_rank(char * uid, bool reverse){
    printf("Called zset_rank with %s, %s\n", uid, reverse ? "true" : "false");
    return -1;
    // return zset_rank(zset, uid, reverse);
}


char * persist = "original";
int zsetpy_delete(char* uid) {
    printf("Called zset_delete with %s\n", uid);
    
    printf("Checking persistance:%s\n", persist);
    persist = uid;
    printf("Checking persistanmce:%s\n", persist);
    return -1;
    // return zset_delete(zset, uid);
}

// TODO remove temp testing char array
char * temp[] = {
    "temp",
    "testing",
    "strings"
};

char ** zsetpy_range(double min, double max, bool minex, bool maxex)
{
    printf("Called zset_range with %f, %f, %s, %s\n", min, max, minex ? "true":"false", maxex ? "true":"false");
    rangespec *range = malloc(sizeof(rangespec));
    range->min = min;
    range->max = max;
    range->minex = minex;
    range->maxex = maxex;
    if (range != NULL)
        puts("Created rangespec successfully");
    else
        puts("Could not create rangespec");


    // char ** uids = zset_range(zset, &range);
    free(range);

    return temp;
    // return uids;
}



