#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int fibonacci_size, search_num;
int *fibarray;
int *search_idx;
int *result;

void* gen_fibbonacci(void *args);
void* search_fib(void *args);

int main()
{
    pthread_t t1;
    pthread_t t2;

    printf("Enter the term of fibonacci sequence:\n");
    scanf("%d", &fibonacci_size);

    printf("How many numbers you are willing to search?:\n");
    scanf("%d",&search_num);
    
    search_idx = malloc(search_num * sizeof(int));
    result = malloc(search_num * sizeof(int));

    for (int i = 0; i < search_num; i++) 
    {
        printf("Enter search %d: ", i+1);
        scanf("%d", &search_idx[i]);
    }

    pthread_create(&t1, NULL, gen_fibbonacci, NULL);
    pthread_join(t1,NULL);

    for(int i=0; i<=fibonacci_size; i++)
    {
        printf("a[%d] = %d\n", i, fibarray[i]);
    }

    pthread_create(&t2, NULL, search_fib, NULL);
    pthread_join(t2, NULL);

    for (int i= 0; i < search_num; i++)
    {
        printf("result of search #%d = %d\n", i+1, result[i]);
    }

    return 0;
}

void* gen_fibbonacci(void *args)
{
    fibarray = (int*) malloc((fibonacci_size+1) * sizeof(int));
    if (fibonacci_size >= 0) 
    {
        fibarray[0] = 0;
    }
    if (fibonacci_size >= 1) 
    {
        fibarray[1] = 1;
    }

    for (int i = 2; i<=fibonacci_size; i++)
    {
        fibarray[i] = fibarray[i-1] + fibarray[i-2];
    }

    pthread_exit(NULL);
}

void* search_fib(void *arg)
{
    for (int i =0; i<search_num; i++)
    {
        int idx =search_idx[i];
        if (idx >= 0 && idx <= fibonacci_size)
        {
            result[i] = fibarray[idx];
        }
        else
        {
            result[i] = -1;
        }
    }
    pthread_exit(NULL);
}