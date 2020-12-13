/*-----------------------------------------------------------------------------
 * Sorted set API
 *----------------------------------------------------------------------------*/
/* ZSETs are ordered sets using two data structures to hold the same elements
 * in order to get O(log(N)) INSERT and REMOVE operations into a sorted
 * data structure.
 *
 * The elements are added to a hash table mapping Redis objects to scores.
 * At the same time the elements are added to a skip list mapping scores
 * to Redis objects (so objects are sorted by scores in this "view").
 *
 * Note that the SDS string representing the element is the same in both
 * the hash table and skiplist in order to save memory. What we do in order
 * to manage the shared SDS string more easily is to free the SDS string
 * only in zslFreeNode(). The dictionary has no value free method set.
 * So we should always remove an element from the dictionary, and later from
 * the skiplist.
 *
 * This skiplist implementation is almost a C translation of the original
 * algorithm described by William Pugh in "Skip Lists: A Probabilistic
 * Alternative to Balanced Trees", modified in three ways:
 * a) this implementation allows for repeated scores.
 * b) the comparison is not just by key (our 'score') but by satellite data.
 * c) there is a back pointer, so it's a doubly linked list with the back
 * pointers being only at "level 1". This allows to traverse the list
 * from tail to head, useful for ZREVRANGE. */


/* For our case, we do not need to do c) and for a) we can point to list
 * for duplicate scores */

#include "zset.h"

ZSet * zset_new(void) {
    ZSet * zs = malloc(sizeof(*zs));
    zs->sl = skip_list_new();
    enum cc_stat status = hashtable_new(zs->map);
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
    enum cc_stat status = hashtable_remove(zs->map, uid, &score);
    if (status == CC_OK) {
        bool slretval = skip_list_delete(zs->sl, score, uid, NULL);
        // Possible error: found in hashmap but not in skiplist.
        // TODO Log this?
        return true;
    }
    return false;
}

bool zset_add(ZSet *zs, double score, char *uid) {
    if(hashtable_contains_key(uid))
        // uid are unique.
        return false;
    
    // map uid -> score
    enum cc_stat status = hashtable_add(zs->map, uid, score);
    if (status != CC_OK)
        // could not add to hashmap
        return false;
    
    return skip_list_insert(zs->sl, score, uid);
}

char ** zset_range(ZSet *zs, rangespec *range) {

}