#ifndef __SKIPLIST_H
#define __SKIPLIST_H

// #include <collectc/list.h>

#include <stdbool.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

/* Skip List */
#define SKIPLIST_MAXLEVEL 32    /* will be enough for 2^64 elements */
#define SKIPLIST_P 0.25         /* probability = 1/4 */

typedef struct SkipListNode {
    // List * uids;
    char * uid;
    double score;

    struct SkipListNode *backward;
    struct SkipListLevel {
        struct SkipListNode *forward;
        unsigned long span;
    } level[];

} SkipListNode;

typedef struct SkipList {
    SkipListNode * head, * tail;
    unsigned long size;
    int level;
} SkipList;

typedef struct rangespec{
    double min, max;
    bool minex, maxex; /* are min or max exclusive? */
} rangespec;

SkipList * skip_list_new(void);
void skip_list_free(SkipList * sl);

SkipListNode * skip_list_insert(SkipList *sl, double score, char *uid);
bool skip_list_delete(SkipList *sl, double score, char *uid, SkipListNode **node);

SkipListNode * skip_list_first_in_range(SkipList *sl, rangespec *range);
// SkipListNode * skip_list_last_in_range(SkipList *sl, rangespec *range);

// unsigned long skip_list_get_rank(SkipList *sl, double score, char *o);

bool skip_list_value_gte_min(double value, rangespec *spec);
bool skip_list_value_lte_max(double value, rangespec *spec);

#endif
