#!/usr/bin/python3

from bcc import BPF
from time import sleep

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

b = BPF(text=program_map)
clone = b.get_syscall_fnname("clone")
b.attach_kprobe(event=clone, fn_name="hello_world")

while True:
    sleep(1)
    s = ""
    if b["clones"]:
        for k, v in b["clones"].items():
            s += f"ID: {k.value}, Clones: {v.value}\t"
        print(s)
    else:
        print("No clones found")
