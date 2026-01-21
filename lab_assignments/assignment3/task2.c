#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/types.h>
#include <sys/shm.h>
#include <sys/msg.h>
#include <string.h>

struct msg{
    long int type;
    char txt[6];
};

int main(){
    int msgid;
    struct msg message;
    pid_t p1, p2;

    msgid = msgget(IPC_PRIVATE, IPC_CREAT|0666);
    if (msgid == -1){
        printf("msgget failed");
        exit(1);
    }
    printf("Please enter the workspace name:\n");
    char workspace[7];  // Increased to 7 to properly hold "cse321" + null terminator
    scanf("%6s", workspace);  // Read max 6 characters

    if(strcmp(workspace, "cse321") != 0){
        printf("Invalid workspace name\n");
        msgctl(msgid, IPC_RMID, NULL);
        return 0;
    }
    message.type = 1;
    strcpy(message.txt, workspace);
    if(msgsnd(msgid, &message, sizeof(message.txt), 0) == -1){
        perror("msgsnd failed");
        exit(1);
    }
    printf("Workspace name sent to otp generator from log in: %s\n", message.txt);

    /* Rest of your existing code remains exactly the same */
    p1 = fork();
    if(p1 == -1){
        perror("fork failed");
        exit(1);
    }
    if(p1 == 0){
        if(msgrcv(msgid, &message, sizeof(message.txt), 1, 0) == -1){
            perror("msgrcv failed");
            exit(1);
        }
        printf("OTP generator recieved workspace name from log in: %s\n", message.txt);

        message.type = 2;
        sprintf(message.txt, "%d", getpid());
        if(msgsnd(msgid, &message, sizeof(message.txt), 0) == -1){
            perror("msgsnd failed");
            exit(1);
        }
        printf("OTP sent to log in from OTP generator: %s\n", message.txt);

        message.type = 3;
        if(msgsnd(msgid, &message, sizeof(message.txt), 0) == -1){
            perror("msgsnd failed");
            exit(1);
        }

        p2 = fork();
        if(p2 == -1){
            perror("fork failed");
            exit(1);
        }

        if(p2 == 0){
            if(msgrcv(msgid, &message, sizeof(message.txt), 3, 0) == -1){
                perror("msgrcv failed");
                exit(1);
            }
            printf("Mail received OTP from OTP generator: %s\n", message.txt);

            message.type = 4;
            if(msgsnd(msgid, &message, sizeof(message.txt), 0) == -1){
                perror("msgsnd failed");
                exit(1);
            }
            printf("OTP sent to log in from mail: %s\n", message.txt);
            exit(0);
        }
        wait(NULL);
        exit(0);
    }

    wait(NULL);

    if(msgrcv(msgid, &message, sizeof(message.txt), 2, 0) == -1){
        perror("msgrcv failed");
        exit(1);
    }
    printf("Log in received OTP from OTP generator: %s\n", message.txt);
    char otp1[6];
    strcpy(otp1, message.txt);

    if(msgrcv(msgid, &message, sizeof(message.txt), 4, 0) == -1){
        perror("msgrcv failed");
        exit(1);
    }
    printf("Log in received OTP from mail: %s\n", message.txt);
    char otp2[6];
    strcpy(otp2, message.txt);

    if(strcmp(otp1, otp2) == 0){
        printf("OTP Verified\n");
    } else {
        printf("OTP Incorrect\n");
    }

    msgctl(msgid, IPC_RMID, NULL);
    return 0;
}