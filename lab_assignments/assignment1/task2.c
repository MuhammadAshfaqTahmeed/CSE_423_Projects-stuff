#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

void main(){
    pid_t pid;
    pid_t x;
    
    pid = fork(); // first fork child create
    if(pid > 0){
        //parent process enter
        wait(NULL);
        printf("I am parent\n");
    }
    else if(pid == 0){
        // child process enter
        x = fork(); // 2nd fork grandchild create

        if(x>0){
            wait(NULL);
            printf("I am child\n");
        }
        else if(x==0){
            // granchild entered
            printf("I am grandchild\n");
        }
    }
}