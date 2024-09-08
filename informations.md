
---

# Install source

On ubuntu 24.04
```bash
sudo apt-get install bpfcc-tools linux-headers-$(uname -r)

# opensnoop
sudo apt install libbpf-tools
```

check install:
```
sudo opensnoop-bpfcc

sudo opensnoop --name cat
```

[source](https://github.com/iovisor/bcc/blob/master/INSTALL.md)

---

# BCC tools

[source](https://github.com/iovisor/bcc?tab=readme-ov-file)

---
