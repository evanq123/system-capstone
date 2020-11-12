zsetpy_test:
	gcc -c -Wall -Werror -fpic zsetpy_test.c
	gcc -shared -o zsetpy.so zsetpy.o
	mv zsetpy.so ..


zsetpy:
	gcc -c -Wall -Werror -fpic *.c *.h
	gcc -shared -o zsetpy.so zsetpy.o
	mv zsetpy.so ..