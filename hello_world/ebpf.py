#!/usr/bin/python3

from bcc import BPF
from time import sleep

program = """
int hello_world(void *ctx) {
    bpf_trace_printk("Hello, World!\\n");
    return 0;
}
"""

program_uid = """
int hello_world(void *ctx) {
    u64 uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;

    bpf_trace_printk("id: %d\\n", uid);
    return 0;
}
"""

b = BPF(text=program)
clone = b.get_syscall_fnname("clone")
b.attach_kprobe(event=clone, fn_name="hello_world")
b.trace_print()

program_map = """
BPF_HASH(clones);

int hello_world(void *ctx) {
    u64 uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
    u64 counter = 0;
    u64 *p;

    p = clones.lookup(&uid);
    if (p != 0) {
        counter = *p;
    }

    counter++;
    clones.update(&uid, &counter);

    return 0;
}
"""

# b = BPF(text=program_map)
# clone = b.get_syscall_fnname("clone")
# b.attach_kprobe(event=clone, fn_name="hello_world")
# 
# while True:
#     sleep(1)
#     s = ""
#     if b["clones"]:
#         for k, v in b["clones"].items():
#             s += f"ID: {k.value}, Clones: {v.value}\t"
#         print(s)
#     else:
#         print("No clones found")
