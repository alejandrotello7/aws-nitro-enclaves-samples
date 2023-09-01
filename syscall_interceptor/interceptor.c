#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/unistd.h>
#include <linux/fdtable.h>
#include <linux/syscalls.h>
#include <asm/paravirt.h>

MODULE_LICENSE("GPL");

// The sys_call_table address obtained from the kernel
unsigned long *sys_call_table;

// Original write syscall function pointer
asmlinkage long (*original_write)(unsigned int, const char __user *, size_t);

// Custom write syscall
asmlinkage long custom_write(unsigned int fd, const char __user *buf, size_t count) {
    // Intercept the write syscall
    printk(KERN_INFO "Intercepted write syscall: fd=%u, count=%zu\n", fd, count);

    // Call the original write syscall
    return original_write(fd, buf, count);
}

static int __init interceptor_init(void) {
    // Replace this value with the actual sys_call_table address
    sys_call_table = (unsigned long *)0xffffffffb9a001c0;

    // Store the original write syscall function
    original_write = (void *)sys_call_table[__NR_write];

    // Disable write protection
    write_cr0(read_cr0() & (~0x10000));

    // Replace the write syscall with our custom_write
    sys_call_table[__NR_write] = (unsigned long *)&custom_write;

    // Enable write protection
    write_cr0(read_cr0() | 0x10000);

    printk(KERN_INFO "Interceptor module loaded\n");
    return 0;
}

static void __exit interceptor_exit(void) {
    // Disable write protection
    write_cr0(read_cr0() & (~0x10000));

    // Restore the original write syscall
    sys_call_table[__NR_write] = (unsigned long *)original_write;

    // Enable write protection
    write_cr0(read_cr0() | 0x10000);

    printk(KERN_INFO "Interceptor module unloaded\n");
}

module_init(interceptor_init);
module_exit(interceptor_exit);
