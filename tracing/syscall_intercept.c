struct open_args {
    const char *filename;
    int flags;
    int mode;
};

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

SEC("tracepoint/syscalls/sys_enter_open")
int trace_enter_open(struct open_args *args) {
    char filename[256];
    bpf_probe_read_str(filename, sizeof(filename), args->filename);
    // Rest of your code
    return 0;
}
