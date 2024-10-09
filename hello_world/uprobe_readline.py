#!/usr/bin/python3

from __future__ import print_function
from bcc import BPF
from time import strftime

# load BPF program
bpf_text = """
#include <uapi/linux/ptrace.h>
int printret(struct pt_regs *ctx) {
    if (!ctx->ax)
        return 0;

    char str[80] = {};
    bpf_probe_read(&str, sizeof(str), (void *)ctx->ax);
    bpf_trace_printk("%s\\n", &str);

    return 0;
};
"""
b = BPF(text=bpf_text)
b.attach_uretprobe(name="/bin/bash", sym="readline", fn_name="printret")

# header
print("%-9s %-6s %s" % ("TIME", "PID", "COMMAND"))

# format output
while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    except ValueError:
        continue
    print("%-9s %-6d %s" % (strftime("%H:%M:%S"), pid, msg))