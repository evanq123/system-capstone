/*-----------------------------------------------------------------------------
 * Sorted set API
 *----------------------------------------------------------------------------*/
/* ZSETs are ordered sets using two data structures to hold the same elements
 * in order to get O(log(N)) INSERT and REMOVE operations into a sorted
 * data structure.
 *
 * The elements are added to a hash table mapping uids to scores.
 * At the same time the elements are added to a skip list mapping scores
 * to uids (so uids are sorted by scores in this "view").
 *
 * This skiplist implementation is almost a C translation of the original
 * algorithm described by William Pugh in "Skip Lists: A Probabilistic
 * Alternative to Balanced Trees", modified in three ways:
 * a) this implementation allows for repeated scores.
 * b) the comparison is not just by key (our 'score') but by satellite data.
 * c) there is a back pointer, so it's a doubly linked list with the back
 * pointers being only at "level 1". This allows to traverse the list
 * from tail to head, useful for reverse ranges in the future. */

#include "zset.h"
#include <stdio.h> // Should be logger instead.

ZSet * zset_new(void) {
    ZSet * zs = malloc(sizeof(*zs));
    zs->sl = skip_list_new();
    enum cc_stat status = hashtable_new(&zs->map);
    if (status != CC_OK) {
        skip_list_free(zs->sl);
        free(zs);
        return NULL;
    }
    
    return zs;
}

unsigned long zset_length(ZSet *zs) {
    return zs->sl->size;
} 

bool zset_delete(ZSet *zs, char *uid) {
    double score;
    enum cc_stat status = hashtable_remove(zs->map, uid, (void *)&score);
    if (status == CC_OK) {
        bool slretval = skip_list_delete(zs->sl, score, uid, NULL);
        // Possible error: found in hashmap but not in skiplist.
        // TODO Log this?
        if (slretval) {
            fprintf(stderr, "Found %s in hashmap but not in skiplist.\n", uid);
        } 
        return true;
    }
    return false;
}

bool zset_add(ZSet *zs, double score, char *uid) {
    if(hashtable_contains_key(zs->map, (void *)uid))
        // uid are unique.
        return false;
    
    // map uid -> score
    enum cc_stat status = hashtable_add(zs->map, uid, (void *)&score);
    if (status != CC_OK)
        // could not add to hashmap
        return false;
    
    return skip_list_insert(zs->sl, score, uid);
}

char ** zset_range(ZSet *zs, rangespec *range) {
    Array * results;
    enum cc_stat status = array_new(&results);
    if (status != CC_OK) {
        // result array could not be created.
        // TODO log this.
        return NULL;
    }
    // Get the node thats first in range.
    SkipListNode * ln = skip_list_first_in_range(zs->sl, range);
    if (ln == NULL) {
        // empty array
        array_destroy(results);
        return calloc(sizeof(char *), 1);
    }

    while(ln) {
        // If this node is not lte max, it is out of range.
        if (!skip_list_value_lte_max(ln->score, range)) break;
        array_add(results, ln->uid);
        ln = ln->level[0].forward; // forward == null if no more elems.
    }

    char ** buffer = (char **)array_get_buffer(results);
    char ** retval = malloc(sizeof(char *) * array_size(results));
    // Trim length of retval and copy
    for (int i = 0; i < array_size(results); i++) {
        retval[i] = buffer[i];
    }
    array_destroy(results); // Frees Array struct but not data.
    return retval;
}