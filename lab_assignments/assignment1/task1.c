#include <stdio.h> // provides fgets()
#include <fcntl.h> // for open()
#include <unistd.h> // Read() write()
#include <stdbool.h> // for boolean veriables
#include <string.h> 
int main(){
    int fd;
    char buffer[100];
    fd = open("inputfile.txt",O_RDWR|O_CREAT,0644);
    if(fd!=-1){
        printf("file open success\n");
        bool running = true;
       
        while (running){
            
            printf("Enter a string: \n");
            /*fgets(pointer to the array to hold read string --- max # char to read --- keyboard input stream)
            fgets()adds a '\n''\0' at the end*/
            fgets(buffer,sizeof(buffer),stdin);        
            buffer[strcspn(buffer, "\n")] = '\0';// fgets adds \n at the end. need to remove it with "\0" to compare -1 or will read -1\n.
            
            if (strcmp(buffer,"-1") == 0){
                running =false;
            }
            else{
                
                write(fd,buffer,strlen(buffer));// strlen() only counts char till first '\0'("\0" is not included in len)
                write(fd,"\n",1); // for starting a newline after each input entry
                printf("write successful\n");
                printf("enter -1 to stop\n");
            }
        }

    } 
    close(fd);
    return 0;
}