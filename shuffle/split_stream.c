#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Code that takes every other character and writes it to the standard output stream from 
// the file shuffle.txt
// Run with gcc -o split split_stream.c and ./split
int main( ) {
	FILE *file; 
    file = fopen("shuffle.txt", "r");
    if (file) {
        int chr;
        int i = 0; 

        while ((chr = fgetc(file)) != EOF){
        	if (i == 0) {
        		fputc(chr, stdout); 
        		i = 1;
        	} else {
                // skip every other output
    			i = 0;
        	}
            
        }
        fclose(file);
    } else {
    	printf("Shuffle.txt could not be found.");
    }
   
   return 0;
}