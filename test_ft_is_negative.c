#include "ex04/ft_is_negative.c"
// #include <stdio.h>

void ft_is_negative(int n);

int main(void) {
    // expected NPP
    int i = -1;

    while (i <= 1){
        // printf("%d\n", i);
        ft_is_negative(i);
        // printf("\n");
        i++;
    }
    
    return 0;
}