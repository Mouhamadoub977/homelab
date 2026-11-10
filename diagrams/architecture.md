# Homelab Architecture

## Current architecture — Phase 1

```mermaid

flowchart TB
    subgraph UNDERLAY["LAYER 1 - Physical and IP underlay"]
        direction LR
        MAC["MacBook Air<br/>macOS / SSH client"]
        ACCESS["Remote Wi-Fi / LAN<br/>External gateway"]
        INTERNET(("Internet / IP routing"))
        ROUTER["Home router<br/>Gateway: 192.168.1.254<br/>NAT / DHCP"]
        SERVER["GMKtec M8<br/>homelab-01<br/>Ubuntu Server 26.04.1"]

        MAC -->|"Wi-Fi"| ACCESS
        ACCESS -->|"IP connectivity"| INTERNET
        INTERNET -->|"Public network path"| ROUTER
        ROUTER -->|"Ethernet / enp2s0<br/>192.168.1.12/24"| SERVER
    end

    subgraph OVERLAY["LAYER 2 - Tailscale overlay"]
        direction LR
        TS_MAC["Tailscale on macOS<br/>100.104.23.26"]
        CONTROL["Tailscale coordination<br/>Identity / peer discovery"]
        DERP["DERP relay<br/>Fallback only"]
        TS_SERVER["Tailscale on Ubuntu<br/>tailscale0: 100.80.166.89/32<br/>Policy routing: table 52"]

        TS_MAC -.->|"Control plane"| CONTROL
        CONTROL -.->|"Control plane"| TS_SERVER
        TS_MAC <-->|"WireGuard encrypted traffic<br/>Direct path observed during test"| TS_SERVER
        TS_MAC <-.->|"Relay path if required"| DERP
        DERP <-.->|"Encrypted traffic relay"| TS_SERVER
    end

    subgraph ADMIN["LAYER 3 - SSH administration"]
        direction LR
        CLIENT["OpenSSH client<br/>Ed25519 private key on Mac"]
        SSHD["OpenSSH server<br/>TCP 22 / public-key auth"]
        CLIENT -->|"SSH over Tailscale<br/>100.80.166.89:22"| SSHD
    end

    MAC -.->|"Runs"| TS_MAC
    SERVER -.->|"Runs"| TS_SERVER
    MAC -.->|"Runs"| CLIENT
    SERVER -.->|"Runs"| SSHD

    MAC -.->|"Alternative: SSH over LAN<br/>192.168.1.12:22<br/>when on same LAN"| SERVER

    classDef physical fill:#e8f1ff,stroke:#2563eb,color:#1e3a8a
    classDef overlay fill:#dcfce7,stroke:#16a34a,color:#166534
    classDef admin fill:#f3e8ff,stroke:#9333ea,color:#581c87

    class MAC,ACCESS,INTERNET,ROUTER,SERVER physical
    class TS_MAC,CONTROL,DERP,TS_SERVER overlay
    class CLIENT,SSHD admin

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
- Default gateway observed: `192.168.1.254`
- Tailscale interface: `tailscale0`
- Tailscale policy-routing table: `52`
- Tailscale peer route: `100.104.23.26/32` via `tailscale0`
- Tailscale peer connectivity: direct during the observed test
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
