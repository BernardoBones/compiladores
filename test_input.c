// test_input.c
#include <stdio.h>
extern long long medianof3(long long a, long long b, long long c);

int main(void) {
    long long x, y, z;

    printf("Digite tres numeros inteiros: ");
    if (scanf("%lld %lld %lld", &x, &y, &z) != 3) {
        printf("Entrada invalida!\n");
        return 1;
    }

    long long r = medianof3(x, y, z);
    printf("A mediana de (%lld, %lld, %lld) = %lld\n", x, y, z, r);

    return 0;
}
