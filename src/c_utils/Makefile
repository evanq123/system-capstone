zsetpy:
	gcc -c -Wall -Werror -fpic *.c *.h
	ld -r *.o -o final.o 
	gcc -shared -o zsetpy.so final.o
	mv zsetpy.so ..

clean:
	rm *.o *.gch *a

