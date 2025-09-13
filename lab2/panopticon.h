#ifndef PANOPTICON_H
#define PANOPTICON_H

#include <stdint.h>

typedef struct two_names {
    const char *nearest;
    const char *snd_nearest;
} two_names;

// provided by the judge
int64_t oj_rand(void);

typedef struct tower_spy tower_spy;
tower_spy *t_init(int64_t n);
void purchase(tower_spy *t, const char *g, int64_t f);
two_names two_nearest(tower_spy *t, int64_t f);

#endif
