# Homelab Architecture

## Current architecture — Phase 1

```mermaid
flowchart TD
    Internet["Internet"]
    Router["Home Router / DHCP"]
    Mac["MacBook Air<br/>SSH Client + Tailscale"]
    Server["GMKtec M8<br/>homelab-01<br/>Ubuntu Server"]
    Tailnet["Tailscale Private Network"]

    Internet --- Router
    Router ---|"Ethernet / enp2s0"| Server
    Router ---|"Wi-Fi / LAN"| Mac

    Mac -.->|"Private VPN connection"| Tailnet
    Tailnet -.->|"SSH / TCP 22"| Server

    classDef device fill:#e8f1ff,stroke:#2563eb,color:#1e3a8a
    classDef vpn fill:#dcfce7,stroke:#16a34a,color:#166534

    class Mac,Server device
    class Tailnet vpn
```

## Infrastructure inventory

| Component | Role | Status |
|---|---|---|
| MacBook Air | Administration workstation | Active |
| GMKtec M8 | Physical Ubuntu Server host | Active |
| Home router | LAN connectivity and DHCP | Active |
| OpenSSH | Secure remote administration | Active |
| Tailscale | Private remote connectivity | Active |
| Ansible | Configuration management | Planned |
| Docker / Kubernetes | Container infrastructure | Planned |
| Prometheus / Grafana | Monitoring and observability | Planned |

## Network information

- Hostname: `homelab-01`
- Active interface: `enp2s0`
- LAN address observed: `192.168.1.12/24`
- Address assignment: DHCP
- Tailscale address observed: `100.80.166.89`
- Remote administration: SSH on TCP port 22

## Architecture decisions

1. Use dedicated physical hardware for server workloads.
2. Administer the server remotely from macOS.
3. Use SSH public-key authentication with a dedicated Ed25519 key.
4. Disable SSH password authentication and direct root login.
5. Use Tailscale for private remote connectivity.
6. Introduce infrastructure automation incrementally.

## Future evolution

The infrastructure will evolve toward automated provisioning,
container orchestration, observability and a self-hosted data platform.

The current deployment consists of one physical server.
High availability and distributed workloads are not yet implemented.
