
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

test map

```
sudo adduser

sudo su

su - forfun -c "ls -l /tmp"
```


---

Profiling

or example you can refer to:
https://netflixtechblog.com/linux-performance-analysis-in-60-000-milliseconds-accc10403c55
 to investigate a perfomance issue on a Linux Machine.

