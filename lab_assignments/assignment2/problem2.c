#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <time.h>

int bread = 0;
int cheese = 1;
int lettuce = 2;

// supplier given items track -1 =item not given on table.
int item1 = -1;
int item2 = -1;
int N; //N user input veriable

pthread_mutex_t table_mutex;

sem_t sem_A, sem_B, sem_C; /*sem_A for maker A
                            sem_B for maker B
                            sem_C for maker C*/
sem_t tablefree; //for supplier to wait

void* supplier(void* arg);
void* makerA(void* arg);
void* makerB(void* arg);
void* makerC(void* arg);

int main()
{
    pthread_t t_supplier, tA, tB, tC;
    
    printf("Enter number of rounds: \n");
    scanf("%d", &N);

    pthread_mutex_init(&table_mutex, NULL);

    sem_init(&sem_A,0,0);
    sem_init(&sem_B,0,0);
    sem_init(&sem_C,0,0);
    sem_init(&tablefree,0,1); // initial value 1 means table free

    srand(time(NULL));

    pthread_create(&t_supplier, NULL, supplier, NULL);
    pthread_create(&tA,NULL,makerA,NULL);
    pthread_create(&tB,NULL,makerB,NULL);
    pthread_create(&tC,NULL,makerC,NULL);

    pthread_join(t_supplier, NULL);
    pthread_join(tA, NULL);
    pthread_join(tB, NULL);
    pthread_join(tC, NULL);
    return 0;
}

void* supplier(void* arg)
{
    for(int i=0; i<N; i++)
    {
        sem_wait(&tablefree); // wait for table to free
        pthread_mutex_lock(&table_mutex);

        item1 = rand() % 3;
        item2 =rand() % 3;

        while (item1 == item2)
        {
            item2 = rand() % 3;
        } 

        printf("\nSupplier places: ");
        
        if (item1 == bread){printf("Bread ");}
        if (item1 == cheese){printf("Cheese ");}
        if (item1 == lettuce){printf("Lettuce ");}

        if (item2 == bread){printf("and Bread\n");}
        if (item2 == cheese){printf("and Cheese\n");}
        if (item2 == lettuce){printf("and Lettuce\n");}

        if((item1 == bread && item2 == cheese) ||
           (item1 == cheese && item2 == bread))
        {
            sem_post(&sem_C); // missing lettuce -> Maker C
        }
        
        else if((item1 == cheese && item2 == lettuce) ||
        (item1 == lettuce && item2 == cheese))
        {
            sem_post(&sem_A);
        }
        
        else
        {
            sem_post(&sem_B); //missing cheese
        }
        pthread_mutex_unlock(&table_mutex);
    }
    return NULL;
}
void* makerA(void* arg) 
{
    for(int i = 0; i < N; i++)
    {
        sem_wait(&sem_A); // wait till supplier signal
        printf("Maker A picks up ingredients\n");
        printf("Maker A is making the sandwich...\n");
        printf("Maker A finished and eats the sandwich\n");
        printf("Maker A signals Supplier\n");
        sem_post(&tablefree); // signal to supplier table is free
    }
}

void* makerB(void* arg) {
    for(int i = 0; i < N; i++) 
    {
        sem_wait(&sem_B);
        printf("Maker B picks up ingredients\n");
        printf("Maker B is making the sandwich...\n");
        printf("Maker B finished and eats the sandwich\n");
        printf("Maker B signals Supplier\n");
        sem_post(&tablefree);
    }
}

void* makerC(void* arg)
{
    for(int i = 0; i < N; i++)
    {
        sem_wait(&sem_C);
        printf("Maker C picks up ingredients\n");
        printf("Maker C is making the sandwich...\n");
        printf("Maker C finished and eats the sandwich\n");
        printf("Maker C signals Supplier\n");
        sem_post(&tablefree);
    }
}