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

# Introduction - What is eBPF? To know

Le portail d'eBPF se trouve sur http://eBPF.io.

Membres du consortium eBPF: Microsoft, Google, Netflix, Facebook...

---

# Introduction - Why eBPF?

## Philosophie

Depuis toujours, le système d'exploitation est l’endroit idéal pour implémenter des solutions d'observabilité, de sécurité et de mise en réseau, en raison de la situation privilégiée du noyau pour superviser et contrôler l'ensemble du système. Évidemment, le noyau d’un système d'exploitation est difficile à faire évoluer en raison de son rôle central et de ses exigences élevées en matière de stabilité et de sécurité. L’innovation au cœur du système d’exploitation suit donc un rythme plus lent que celui des applications utilisateurs.

---

# Introduction - Why eBPF?

## Concrètement

eBPF change complètement la donne. Cette technologie permet aux développeurs d’exécuter des programmes confinés dans le noyau, et ainsi d’ajouter de nouvelles fonctionnalités au système d’exploitation qui tourne sur une machine. Le système d'exploitation garantit alors la sûreté des programmes grâce à un vérificateur, et assure une vitesse d'exécution égale au code natif à l'aide d'un compilateur Just-In-Time (JIT). En conséquence, une vague de projets basés sur eBPF a vu le jour, couvrant un large éventail d’applications, notamment pour des fonctionnalités de réseau, d'observabilité et de sécurité nouvelle génération.

---

## Introduction - How it works?

---

