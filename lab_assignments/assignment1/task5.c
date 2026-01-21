#include <stdio.h>
#include <unistd.h> // for all forks() getpid() getppid()
#include <sys/types.h>
#include <sys/wait.h> // for all wait calls
#include <stdlib.h> // needed to recognise exit()

int main(){
    pid_t chi , grchi ;
    printf("Parent process ID:%d \n", getpid());

    chi = fork();

    if (chi == 0){ // context now child
        printf("Child process ID:%d \n",getpid()); 
        for(int i = 0; i < 3; i++){
            grchi = fork();
            
            if (grchi == 0){ // context now granchild
                printf("Grand child ID:%d \n",getpid());
                exit(0); // exit granchild
            }
            else{
                wait(NULL);
            }       
        }
        exit(0); // exit child  
    }
    else{
        wait(NULL); // wait for child to finish
    }
    return 0;
}