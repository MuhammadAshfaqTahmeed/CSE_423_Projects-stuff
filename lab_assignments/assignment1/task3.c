#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
void main(){
    pid_t a,b,c;
    int flag = 1; // parent also counted
    
    a = fork();   

    if( a == 0 ){ 
        // count child
        flag++;
        printf("Child process created: PID = %d\n", getpid());
        
        int var  = getpid();
        if(var % 2 != 0){ // if pid is odd then fork a granchild
            pid_t gc = fork();
            if(gc == 0){ //  at gc now
                flag++; // grandchild counted
                printf("Grandchild process created: PID = %d\n", getpid());
            }  
            else{
                wait(NULL);// child waits for granchild to execute
            } 
        } 
       
    }
    else{
        wait(NULL);
    }
    
    b = fork();
    
    if (b == 0){
        flag++;
        printf("Child process created: PID = %d\n", getpid());
        
        int var = getpid();
        if (var % 2 == 0){
           pid_t gc = fork();
           if(gc == 0){
            flag++;
            printf("Grandchild process created: PID = %d\n", getpid());
           }
           else{
            wait(NULL);
           }
        }
    }
    else{
        wait(NULL);
    }
    
    c = fork();
    
    if (c == 0){
         // count child
        flag++;
        printf("Child process created: PID = %d\n", getpid());
        
        int var = getpid();
        if (var % 2 != 0){ //  chlid pid odd create a gc
            pid_t gc = fork();
            if (gc == 0){ // at gc now 
                flag++; // count gc
                printf("Grandchild process created: PID = %d\n", getpid());
            }
            else{
                wait(NULL);
            }
        } 
    }
    else{
        wait(NULL);   
    }
    if (a > 0 && b > 0  && c > 0){
        printf("Parent created %d\n",flag);
    } 
}  