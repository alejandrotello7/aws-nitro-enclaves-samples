cmd_/home/atello/Downloads/aws-nitro-enclaves-samples/syscall_interceptor/interceptor.mod := printf '%s\n'   interceptor.o | awk '!x[$$0]++ { print("/home/atello/Downloads/aws-nitro-enclaves-samples/syscall_interceptor/"$$0) }' > /home/atello/Downloads/aws-nitro-enclaves-samples/syscall_interceptor/interceptor.mod
