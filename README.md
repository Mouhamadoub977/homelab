# Personal Homelab

A hands-on infrastructure engineering project built on physical hardware to explore Linux, networking, automation, container orchestration, observability and modern data platforms.

## Overview

The goal of this project is to design, deploy, automate and operate a self-hosted infrastructure, progressing from a single Ubuntu Server node to a distributed homelab environment.

This repository documents the architecture, technical decisions, configurations, experiments and lessons learned.

## Current Infrastructure

| Component | Description |
|---|---|
| Server | GMKtec Mini PC |
| Operating system | Ubuntu Server 26.04 LTS |
| Hostname | homelab-01 |
| Networking | Ethernet, DHCP |
| Remote administration | OpenSSH |
| Administration workstation | MacBook Air |
| Storage | NVMe SSD, LVM |

## Project Roadmap

### Phase 1 — Infrastructure Foundation

- [x] Install Ubuntu Server on physical hardware
- [x] Configure Ethernet connectivity
- [x] Configure initial storage using LVM
- [x] Install OpenSSH Server
- [x] Establish remote SSH access
- [x] Verify hostname, user and network interfaces
- [ ] Update operating system packages
- [ ] Configure SSH key authentication
- [ ] Harden SSH and firewall configuration
- [ ] Configure stable LAN addressing
- [ ] Configure secure remote access through VPN

### Phase 2 — Automation

- [ ] Learn and implement Ansible
- [ ] Automate server provisioning
- [ ] Introduce Infrastructure as Code

### Phase 3 — Containerization and Orchestration

- [ ] Deploy Docker and Docker Compose
- [ ] Build containerized applications
- [ ] Deploy Kubernetes (k3s)
- [ ] Explore multi-node orchestration

### Phase 4 — Observability

- [ ] Deploy Prometheus
- [ ] Deploy Grafana
- [ ] Implement centralized logging
- [ ] Configure monitoring and alerting

### Phase 5 — Data Engineering Platform

- [ ] Deploy PostgreSQL
- [ ] Deploy MinIO
- [ ] Deploy Apache Airflow
- [ ] Experiment with Spark and dbt
- [ ] Build an end-to-end data pipeline

## Documentation

- [Ubuntu Server Installation](docs/01-installation.md)
- [Networking Configuration](docs/02-networking.md)
- [SSH Configuration](docs/03-ssh.md)
- [Infrastructure Architecture](diagrams/architecture.md)

## Engineering Principles

- Infrastructure as Code
- Reproducibility
- Security by design
- Version control
- Observability
- Documentation-driven learning

## Project Status

**Phase 1 — Infrastructure Foundation: In progress**

The first physical node is operational and accessible through SSH on the local network.

## Security

No passwords, private SSH keys, access tokens or other sensitive credentials are stored in this repository.