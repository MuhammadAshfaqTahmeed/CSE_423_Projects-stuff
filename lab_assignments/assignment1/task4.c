#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    char *arr[] = { NULL, "11", "12", "30", "40", NULL}; // end NULL used for execvp() first NULL used for initally using no program
    pid_t pid = fork();
    
    if (pid == 0) {
        printf("Inside child and executing sort:\n");
        arr[0] = "./sort.out"; // dont forget to use ./ or wont work
        execvp(arr[0], arr);  // Executes sort program
    }
    else {
        wait(NULL);
        printf("Inside parent and executing oddeven:\n");
        arr[0] = "./oddeven.out";
        execvp(arr[0], arr);  // Executes oddeven program
    }
    
    return 0;
}