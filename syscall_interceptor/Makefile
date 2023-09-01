obj-m += interceptor.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules NO_BTF=1

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
