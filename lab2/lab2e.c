#include "panopticon.h"
#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

typedef int64_t data_t;
typedef int64_t prio_t;

typedef struct Node {
    data_t floor;
    prio_t p;
    const char *guest;
    struct Node *l, *r;
} Node;

typedef struct tower_spy {
    Node *root;
    int64_t n_floors;
    int64_t size;
} tower_spy;


Node *n_make(data_t f, const char *g);
void n_split(Node *n, data_t v, Node **l, Node **x, Node **r);
Node *n_merge(Node *l, Node *r);
Node *n_add(Node *n, data_t f, const char *g);
bool n_contains(Node *n, data_t f);
Node *pred(Node *n, data_t f);
Node *succ(Node *n, data_t f);



Node *n_make(data_t f, const char *g) {
    Node *n = malloc(sizeof(Node));
    n->floor = f;
    n->guest = g;
    n->p = oj_rand();
    n->l = n->r = NULL;
    return n;
}

void n_split(Node *n, data_t v, Node **l, Node **x, Node **r) {
    if (!n) {
        *l = *x = *r = NULL;
        return;
    }
    if (v < n->floor) {
        *r = n;
        n_split(n->l, v, l, x, &n->l);
    } else if (v > n->floor) {
        *l = n;
        n_split(n->r, v, &n->r, x, r);
    } else {
        *l = n->l;
        *x = n;
        *r = n->r;
        n->l = n->r = NULL;
    }
}


Node *n_merge(Node *l, Node *r) {
    if (!l) {
        return r;
    } 
    if (!r) {
        return l;
    } 
    if (l->p >= r->p) {
        l->r = n_merge(l->r, r);
        return l;
    } else {
        r->l = n_merge(l, r->l);
        return r;
    }
}

Node *n_add(Node *n, data_t f, const char *g) {
    Node *l, *x, *r;
    n_split(n, f, &l, &x, &r);
    assert(!x);
    x = n_make(f, g);
    return n_merge(n_merge(l, x), r);
}

bool n_contains(Node *n, data_t f) {
    if (!n) {
        return false;
    }
    if (f < n->floor) {
        return n_contains(n->l, f);
    } 
    if (f > n->floor) {
        return n_contains(n->r, f);
    }
    return true;
}

tower_spy *t_init(int64_t n) {
    tower_spy *t = malloc(sizeof(tower_spy));
    t->root = NULL;
    t->n_floors = n;
    t->size = 0;
    return t;
}

void purchase(tower_spy *t, const char *g, int64_t f) {
    if (!n_contains(t->root, f)) {
        t->root = n_add(t->root, f, g);
        t->size++;
    }
}

Node *pred(Node *n, data_t f) {
    Node *res = NULL;
    while (n) {
        if (n->floor < f) {
            res = n;
            n = n->r;
        } else {
            n = n->l;
        }
    }
    return res;
}

Node *succ(Node *n, data_t f) {
    Node *res = NULL;
    while (n) {
        if (n->floor > f) {
            res = n;
            n = n->l;
        } else {
            n = n->r;
        }
    }
    return res;
}

two_names two_nearest(tower_spy *t, int64_t f) {
    two_names res;
    res.nearest = NULL;
    res.snd_nearest = NULL;

    if (t->size <= 2) {
        return res;
    }

    Node *left1 = pred(t->root, f);
    Node *left2 = NULL;
    if (left1) {
        left2 = pred(t->root, left1->floor);
    }

    Node *right1 = succ(t->root, f);
    Node *right2 = NULL;
    if (right1) {
        right2 = succ(t->root, right1->floor);
    }

    Node *cand[4];
    int cnt = 0;
    if (left1) {
        cand[cnt++] = left1;
    }
    if (left2) {
        cand[cnt++] = left2;
    }
    if (right1) {
        cand[cnt++] = right1;
    }
    if (right2) {
        cand[cnt++] = right2;
    }

    if (cnt < 2) {
        return res;
    }

    int best = -1, snd = -1;
    for (int i = 0; i < cnt; i++) {
        if (best == -1) {
            best = i;
        } else {
            int64_t da = llabs(cand[i]->floor - f);
            int64_t db = llabs(cand[best]->floor - f);
            if (da < db || (da == db && cand[i]->floor < cand[best]->floor)) {
                best = i;
            }
        }
    }

    for (int i = 0; i < cnt; i++) {
        if (i == best) {
            continue;
        }
        if (snd == -1) {
            snd = i;
        } else {
            int64_t da = llabs(cand[i]->floor - f);
            int64_t db = llabs(cand[snd]->floor - f);
            if (da < db || (da == db && cand[i]->floor < cand[snd]->floor)) {
                snd = i;
            }
        }
    }

    if (best != -1) {
        res.nearest = cand[best]->guest;
    }
    if (snd != -1) {
        res.snd_nearest = cand[snd]->guest;
    }

    return res;
}
