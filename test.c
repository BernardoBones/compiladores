// test.c
#include <stdio.h>
extern long long medianof3(long long a, long long b, long long c);

int main(void) {
    long long r;
    r = medianof3(10LL, 5LL, 8LL);
    printf("%lld\n", r); // deve imprimir 8
    // testar outros casos
    printf("%lld\n", medianof3(-5LL, 0LL, 5LL)); // 0
    printf("%lld\n", medianof3(7LL, 7LL, 3LL)); // 7
    printf("%lld\n", medianof3(1,1,1));   // 1
    printf("%lld\n", medianof3(-10,-20,-30)); // -20

    printf("%lld\n", medianof3(1000L, 666LL, -52LL)); // 666
    printf("%lld\n", medianof3(999999999LL, 999999999LL, 999999999LL)); // 999999999
    printf("%lld\n", medianof3(-3,-1,-2));   // 

    return 0;
}
