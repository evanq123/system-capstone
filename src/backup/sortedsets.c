#include <collectc/treeset.h>
#include <collectc/hashtable.h>
#include <collectc/array.h>

#include <stdio.h>
#include <stdlib.h>

static HashTable * table; // i.e.: {"date": treeset<date_score, uid>}

int cmp(const void *a, const void *b) {
    // a and b will be determined from our application.
    return *((int*) a) - *((int*) b);
}

void treeset_get_range(TreeSet *set, void *k1, void *k2, Array *out) {
    void *a = k1;
    void *curr = a;
    if (curr != NULL) {
        array_add(out, curr);
    }
    while(cmp(a, k2) < 0) {
        enum cc_stat status = treeset_get_greater_than(set, a, &curr);
        if(status != CC_OK || curr == NULL) {
            return;
        }
        array_add(out, curr);
        a = curr;
    }
}

// void treeset_get_range_iter(TreeSet *set, void *k1, void *k2, Array *out) {
//     void *a = k1;
//     void *curr = a;
//     TreeSetIter *iter;
//     treeset_iter_init(iter, set);
//     if (curr != NULL) {
//         array_add(out, curr);
//     }
//     while(cmp(a, k2) < 0) {
//         enum cc_stat status = treeset_iter_next(set, a, &curr);
//         if(status != CC_OK || curr == NULL) {
//             return;
//         }
//         array_add(out, curr);
//         a = curr;
//     }
// }

void treeset_get_all_greater_than_equal(TreeSet *set, void *element, Array *out) {
    void * last;
    treeset_get_last(set, &last);

    treeset_get_range(set, element, last, out);
}

void treeset_get_all_lesser_than_equal(TreeSet *set, void *element, Array *out){
    void * first;
    treeset_get_first(set, &first);

    treeset_get_range(set, first, element, out);
}

void test2() {
    TreeSet * dates;
    treeset_new(cmp, &dates);
    Array * result;
    int a = 1;
    int b = 2;
    int c = 3;
    int d = 4;
    int e = 5;
    int f = 6;
    int g = 7;
    treeset_add(dates, &a);
    treeset_add(dates, &g);
    treeset_add(dates, &b);
    treeset_add(dates, &c);
    treeset_add(dates, &d);
    treeset_add(dates, &e);
    treeset_add(dates, &f);

    array_new(&result);
    treeset_get_range(dates, &a, &d, result);
    
    for(int i = 0; i < array_size(result); i++) {
        int *g;
        array_get_at(result, i, (void *) &g);
        printf("%d\n", *g);
    }

    Array * result2;
    Array * result3;
    array_new(&result2);
    array_new(&result3);
    treeset_get_all_greater_than_equal(dates, &c, result2);
    treeset_get_all_lesser_than_equal(dates, &d, result3);
    printf("-\n");
    for(int i = 0; i < array_size(result2); i++) {
        int *g;
        array_get_at(result2, i, (void *) &g);
        printf("%d\n", *g);
    }
    printf("-\n");
    for(int i = 0; i < array_size(result3); i++) {
        int *g;
        array_get_at(result3, i, (void *) &g);
        printf("%d\n", *g);
    }


}



/** Temporary test methods **/
void test() {
    TreeSet * test;
    treeset_new(cmp, &test);
    int a = 1;
    int b = 2;
    int c = 3;
    int d = 4;
    treeset_add(test, &a);
    treeset_add(test, &b);
    treeset_add(test, &c);

    int *g;

    treeset_get_lesser_than(test, &d, (void *) &g);
    
    printf("%d\n", *g);
}

int main () {
    // test();
    test2();
}

