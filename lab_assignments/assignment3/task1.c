#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
// header files for shared memory
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/types.h>
#include <sys/shm.h>
#include <sys/msg.h>
#include <string.h>

struct shared {
    char sel[100]; 
    int b;
};

int main() {
    int shmid;
    struct shared *shm;
    int pipefd[2]; 
    pid_t pid;

    // allocating shared memory
    shmid = shmget(IPC_PRIVATE, sizeof(struct shared), IPC_CREAT | 0666);
    if (shmid == -1) {
        perror("shmget failed");
        exit(1);
    } 

    // attech shared memory (shm is a pointer for each prceess looking at shared memory to access the stuct resource)
    shm = (struct shared *)shmat(shmid, NULL, 0);
    if (shm == (void *) -1) {
        perror("shmat failed");
        exit(1); 
    }

    // set initial balance
    shm->b = 1000;

    // check pipefd worked
    if (pipe(pipefd) == -1) {
        perror("pipe failed");
        exit(1);
    }

    printf("Provide Your INput From Given Options:\n");
    printf("1. Type a to Add Money\n");
    printf("2. Type w to Withdraw Money\n");
    printf("3. Type c to check Balance\n");

    scanf("%s", shm->sel);
    printf("\n");
    printf("Your selection:%s\n", shm->sel);

    pid = fork();

    //  parent work (home)
    if (pid > 0) {
        close(pipefd[1]); // to close the write end of the pipe
        wait(NULL);

        char buffer[100];
        read(pipefd[0], buffer, sizeof(buffer));
        printf("\n%s\n", buffer);

        close(pipefd[0]);// closing the read end of the pipe
        shmdt(shm); // disconnects the process from the shared memory
        shmctl(shmid, IPC_RMID, NULL); // removes the shared memory after deteching all processes
    } else { // opr work starts 
        close(pipefd[0]); 

        if (strcmp(shm->sel, "a") == 0) {
            printf("Enter amount to be added:\n");
            int amount;
            scanf("%d", &amount);
            if (amount > 0) {
                shm->b += amount;
                printf("\nBalance added successfully\n");
                printf("Updated balance after addition; \n%d\n", shm->b);
            } else {
                printf("\nAdding failed, Invalid amount\n");
            }
        } else if (strcmp(shm->sel, "w") == 0) {
            printf("Enter amount to be withdrawn:\n");
            int amount;
            scanf("%d", &amount);

            if (amount > 0 && amount <= shm->b) {
                shm->b -= amount;
                printf("\nBalance withdrawn successfully\n");
                printf("Updated balance after withdrawal:\n%d\n", shm->b);
            } else {
                printf("\nWithdrawal failed, Invalid amount\n");
            }
        } else if (strcmp(shm->sel, "c") == 0) {
            printf("\nYour current balance is:\n%d\n", shm->b);
        } else {
            printf("\nInvalid selection\n");
        }

        // sending message to buffer from opr to write
        char *msg = "Thank you for using";
        write(pipefd[1], msg, strlen(msg) + 1); // +1  add byte storage for null terminator

        // Clean up
        close(pipefd[1]);
        shmdt(shm);
        exit(0);
    }   
    return 0;
}