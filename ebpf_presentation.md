---
marp: true
title: Introduction to eBPF 
theme: default
style: |
  section.title  h1 {
    font-size: 250%;
    text-align: center;
  }
  section.title  p {
    font-size: 250%;
    text-align: center;
  }
  section.plan h1 {
    font-size: 250%;
  }
  section.plan li:nth-child(1) {
    font-size: 200%;
    font-weight: bold
  }
  section.plan li {
    font-size: 150%;
  }
  section.image p:has(img) {
    text-align: center;
  }
  section.code pre {
    font-size: 2rem;
  }
  
paginate: true
---

<!-- _class: title -->

# Dynamically programming the kernel using

![50%](images/EBPF_logo.png)

---

<!-- _class: plan -->
<!-- _backgroundColor: orange -->
<!-- _color: white -->

# Plan

- Introduction
- Usage example with bcc
- Limitation

---

# Introduction - What is eBPF?

## Definition

eBPF est une technologie révolutionnaire issue du noyau Linux qui peut exécuter des programmes dans un environnement confiné, mais avec les privilèges du noyau du système d'exploitation. eBPF est utilisé pour étendre de façon sûre et efficace les capacités du noyau, sans qu'il soit nécessaire de modifier le code source du noyau ou de charger des modules.

---

# Introduction - What is eBPF?

## Naming

BPF signifiait à l'origine Berkeley Packet Filter, mais maintenant qu’eBPF (« extended BPF ») peut faire bien plus que filtrer des paquets, l'acronyme n'a plus de sens. eBPF est désormais considéré comme un terme autonome qui ne signifie plus vraiment quelque chose. Dans le code source de Linux, le terme BPF persiste, et dans les outils et la documentation, les termes BPF et eBPF sont généralement utilisés de manière interchangeable. Le BPF d'origine est parfois appelé cBPF (classic BPF) pour le distinguer d’eBPF.

![w:256](images/EBPF_logo.png) Le logo se nomme eBee. Il a été choisi lors du premier sommet d'eBPF

---

![bg auto](images/state_of_ebpf.png)

---

# Introduction - Why eBPF?

## Philosophie

Depuis toujours, le système d'exploitation est l’endroit idéal pour implémenter des solutions d'observabilité, de sécurité et de mise en réseau, en raison de la situation privilégiée du noyau pour superviser et contrôler l'ensemble du système. Évidemment, le noyau d’un système d'exploitation est difficile à faire évoluer en raison de son rôle central et de ses exigences élevées en matière de stabilité et de sécurité. L’innovation au cœur du système d’exploitation suit donc un rythme plus lent que celui des applications utilisateurs.

---

# Introduction - Why eBPF?

## Fonctionnement des applications

<!-- _class: image -->

![w:800 h:400](images/Kernel_Layout.png)

---

# Introduction - Why eBPF?

## Concrètement

eBPF change complètement la donne. Cette technologie permet aux développeurs d’exécuter des programmes confinés dans le noyau, et ainsi d’ajouter de nouvelles fonctionnalités au système d’exploitation qui tourne sur une machine. Le système d'exploitation garantit alors la sûreté des programmes grâce à un vérificateur, et assure une vitesse d'exécution égale au code natif à l'aide d'un compilateur Just-In-Time (JIT). En conséquence, une vague de projets basés sur eBPF a vu le jour, couvrant un large éventail d’applications, notamment pour des fonctionnalités de réseau, d'observabilité et de sécurité nouvelle génération.

---

# Introduction - How it works?

## Les points d'attaches

Les programmes eBPF sont pilotés par des événements et sont exécutés lorsque le noyau ou une application passe un certain hook (point d’attache). Les hooks prédéfinis incluent les appels système, l'entrée/sortie de fonctions, les points de trace du noyau, les événements réseau, et d’autres encore.

![bg right h:300](images/syscall-hook.png)

---

# Introduction - How it works?

## L'évolutivité

Si un hook prédéfini n'existe pas pour un besoin particulier, il est possible de créer une sonde noyau (kprobe) ou une sonde utilisateur (uprobe) pour attacher des programmes eBPF presque n'importe où dans le noyau ou les applications utilisateur.

<!-- _class: image -->

![h:300](images/hook-overview.png)

---

# Introduction - Main Applications

- BCC
- Cilium
- Falco
- Pixie
- Tetragon


reference: [Official site - Applications](https://ebpf.io/fr-fr/applications/)

---

# Example using bcc

## Install bcc

<!-- _class: code -->

On ubuntu 24.04

```bash
sudo apt-get install bpfcc-tools linux-headers-$(uname -r)
```

---

# Example using bcc

## Principe

- Write a python script using the bcc library
- This python script will contain a C program to be loaded by the kernel
- Then the C program is attached to a probe that will execute the program
- At the end run the script

---

# Example using bcc

## Principe

- Write a python script using the bcc library

<!-- _class: code -->

```py
#!/usr/bin/python3

from bcc import BPF
```

---

# Example using bcc

## Principe

- Write a C program to be executed in the kernel

<!-- _class: code -->

```py
program = """
int hello_world(void *ctx) {
    bpf_trace_printk("Hello, World!\\n");
    return 0;
}
"""
```

---

# Example using bcc

## Principe

- Attach the C program to a probe that will execute it

<!-- _class: code -->

```py
b = BPF(text=program)
clone = b.get_syscall_fnname("clone")
b.attach_kprobe(event=clone, fn_name="hello_world")
b.trace_print()
```

---

# Example using bcc

## Helper functions

Helper functions are functions defined by the kernel which can be invoked from eBPF programs. These helper functions allow eBPF programs to interact with the kernel as if calling a function.

<!-- _class: code -->

```py
program = """
int hello_world(void *ctx) {
    u64 uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;

    bpf_trace_printk("id: %d\\n", uid);
    return 0;
}
"""
```

---

# Example using bcc

## BPF hash maps

BPF ‘maps’ provide generic storage of different types for sharing data between kernel and user space. There are several storage types available, including hash, array. Several of the map types exist to support specific BPF helpers that perform actions based on the map contents. The maps are accessed from BPF programs via BPF helpers which are documented in the man-pages for bpf-helpers(7).

---

# Example using bcc

## Hash map example - Kernel Space

<!-- _class: code -->

```py
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
```

---

# Example using bcc

## Hash map example - User Space

<!-- _class: code -->

```py
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
```

---

# BPF Tools

BPF tools provides scripts help you to profile your system.

You can install those tools on Ubuntu 22.04 using:

``` 
sudo apt install libbpf-tools
```

and check the install:

``` 
sudo opensnoop-bpfcc
```

```
sudo opensnoop --name cat
```
