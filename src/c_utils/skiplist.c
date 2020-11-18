#include "skiplist.h"

// TODO: safer malloc and free to avoid errors on runtime.
// TODO: possibly use list to store duplicate scores making this 2-d.

/**
 * Creates a new skip list node and returns that node.
 * 
 * @param[in] level the specified number of levels
 * @param[in] score the score for the associated uid
 * @param[in] uid the unique identifier(primary key) of the element
 * 
 * @return SkipListNode* on success, else NULL
 */
SkipListNode * skip_list_node_new(int level, double score, char * uid) 
{
    SkipListNode * sn = 
        malloc(sizeof(*sn) + level * sizeof(struct SkipListLevel));
    if (sn == NULL)
        return NULL;
    sn->score = score;
    // List * uids;
    // enum cc_stat status = list_new(&uids);
    // if (status != CC_OK)
    //     return NULL;
    // sn->uids = uids;
    sn->uid = uid;
    return sn;
}

/**
 * Frees the specified skip list node.
 * 
 * @note 
 * Frees the uid if node->uid != NULL
 * @param[in] node the skip list node to free
 */
void skip_list_node_free(SkipListNode * node)
{
    // list_destroy(node->uids);
    if (node->uid != NULL)
        free(node->uid);
    free(node);
}

/**
 * Creates a new skip list and returns that list.
 * 
 * @return SkipList* on success, else NULL
 */
SkipList * skip_list_new(void) 
{
    SkipList * sl = 
        malloc(sizeof(*sl));
    sl->level = 1;
    sl->size = 0;
    if ( (sl->head = skip_list_node_new(SKIPLIST_MAXLEVEL, 0, NULL)) == NULL) {
        return NULL;
    } 
    for (int i = 0; i < SKIPLIST_MAXLEVEL; i++) {
        sl->head->level[i].forward = NULL;
        sl->head->level[i].span = 0; 
    }
    sl->head->backward = NULL;
    sl->tail = NULL;
    return sl;
}

/**
 * Frees the specified skip list.
 * 
 * @param[in] sl the skip list to be freed
 */
void skip_list_free(SkipList * sl)
{
    SkipListNode * node = sl->head->level[0].forward, *next;

    free(sl->head);
    while(node) {
        next = node->level[0].forward;
        skip_list_node_free(node);
        node = next;
    }
    free(sl);
}

/**
 * Generate a random level for skip list node.
 * 
 * @return int between [1...MAXLEVEL] where higher levels are less
 * likely to be returned, using powerlaw distribution.
 */
int skip_list_random_level(void) 
{
    int level = 1;
    while ((random() & 0xFFFF) < (SKIPLIST_P * 0xFFFF))
        level++;
    return (level < SKIPLIST_MAXLEVEL) ? level : SKIPLIST_MAXLEVEL;
}

/**
 * Insert uid into skiplist.
 * 
 * @note
 * This skiplist implementation allows duplicate scores, so the caller,
 * (sortedset) must make sure that the uid is not already in this skip
 * list.
 */
SkipListNode * skip_list_insert(SkipList *sl, double score, char* uid)
{
    // move n to insertion location.
    SkipListNode * n = sl->head;
    unsigned int rank[SKIPLIST_MAXLEVEL];
    for (int i = sl->level - 1; i >= 0; i--)
    {
        rank[i] = (i == (sl->level - 1)) ? 0 : rank[i + 1];
        while (n->level[i].forward && 
            (n->level[i].forward->score < score ||
                (n->level[i].forward->score == score &&
                strcmp(n->level[i].forward->uid, uid) < 0)))
        {
            rank[i] += n->level[i].span;
            n = n->level[i].forward;
        }
    }
    
    // preparing to add n.
    SkipListNode * update[SKIPLIST_MAXLEVEL];
    int level = skip_list_random_level();
    n = skip_list_node_new(level, score, uid);
    if(level > sl->level) {
        for (int i = sl->level; i < level; i++) {
            rank[i] = 0; 
            update[i] = sl->head;
            update[i]->level[i].span = sl->size;
        }
    }
    
    // update skip list inserting n
    for(int i = 0; i < level; i++) {
        // update forward references.
        n->level[i].forward = update[i]->level[i].forward;
        update[i]->level[i].forward = n;

        // update span
        n->level[i].span = update[i]->level[i].span - (rank[0] - rank[i]);
        update[i]->level[i].span = (rank[0] - rank[i]) + 1;
    }

    // update untouched levels' span
    for (int i = level; i < sl->level; i++) {
        update[i]->level[i].span++;
    }

    // update backward pointers for doubly linked skip list
    n->backward = (update[0] == sl->head) ? NULL : update[0];
    if (n->level[0].forward) {
        n->level[0].forward->backward = n;
    } else {
        sl->tail = n;
    }

    sl->size++;
    return n;
}