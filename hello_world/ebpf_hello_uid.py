#!/usr/bin/python3

from bcc import BPF

program_uid = """
int hello_world(void *ctx) {
    u64 uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;

    bpf_trace_printk("id: %d\\n", uid);
    return 0;
}
"""

b = BPF(text=program_uid)
clone = b.get_syscall_fnname("clone")
b.attach_kprobe(event=clone, fn_name="hello_world")
b.trace_print()
