# 02 — Network Configuration

## Objective

Establish reliable local network connectivity between the GMKtec Ubuntu Server and the administration workstation.

This document describes the initial network configuration and the concepts behind it.

## 1. Network architecture

```text
                     Internet
                        |
                  Home router
                        |
              Local network (LAN)
                 192.168.1.0/24
                        |
            +-----------+-----------+
            |                       |
       MacBook Air               GMKtec
       SSH client                homelab-01
                                 Ubuntu Server
                                 192.168.1.12
                                 enp2s0
```

The MacBook Air connects to the home network using Wi-Fi, while the Ubuntu Server uses Ethernet.

Both devices communicate through the local network.

## 2. Network interfaces

The server contains multiple network interfaces.

| Interface | Role | Initial state |
|---|---|---|
| `lo` | Loopback | UP |
| `enp1s0` | Ethernet | DOWN |
| `enp2s0` | Ethernet | UP |
| `wlp4s0` | Wi-Fi | DOWN |

Inspect the interfaces using:

```bash
ip -br addr
```

The `-br` option displays a brief summary of the interface addresses and operational states.

The active interface is `enp2s0`.

## 3. DHCP configuration

During Ubuntu Server installation, the Ethernet interface was configured using DHCP.

DHCP stands for Dynamic Host Configuration Protocol.

It allows a DHCP server, usually the home router, to assign network parameters automatically.

Typical parameters include:

- IPv4 address
- Subnet mask
- Default gateway
- DNS servers
- Lease duration

The server received:

```text
IPv4 address: 192.168.1.12
Subnet:      192.168.1.0/24
Interface:   enp2s0
```

The `/24` prefix corresponds to the subnet mask `255.255.255.0`.

The default gateway and DNS configuration have not yet been independently verified.

## 4. Private IP addressing

The address `192.168.1.12` belongs to the RFC 1918 private IPv4 address space.

Private IP addresses are used within local networks and are not directly routed over the public Internet.

This explains why the following command works from the Mac when both devices are on the same home network:

```bash
ssh mouhamadou@192.168.1.12
```

However, the same command will not normally reach the home server from another network.

## 5. Ethernet connectivity

The GMKtec is connected to the home router using a Cat 6 Ethernet cable.

The active Ethernet interface is `enp2s0`.

Ethernet provides a stable wired connection suitable for a server that will remain powered on for extended periods.

## 6. Useful diagnostic commands

Display network interfaces:

```bash
ip -br addr
```

Display the routing table:

```bash
ip route
```

Display DNS configuration:

```bash
resolvectl status
```

Test connectivity to the local router:

```bash
ping -c 4 <GATEWAY_IP>
```

Test connectivity to an external IP address:

```bash
ping -c 4 1.1.1.1
```

Test DNS resolution:

```bash
getent hosts ubuntu.com
```

These commands help distinguish physical connectivity, IP routing and DNS problems.

## 7. Planned improvements

### Stable LAN addressing

The server currently receives its IP address through DHCP.

A DHCP reservation on the home router is preferred to keep the address stable while retaining centralized network configuration.

### Remote access

Remote administration outside the home network will be implemented using a secure VPN solution, such as Tailscale or WireGuard.

Direct exposure of SSH to the public Internet is not planned.

### Network security

Future tasks include:

- Configure a firewall
- Restrict unnecessary inbound connections
- Configure SSH key authentication
- Document network services and ports
- Monitor network availability

## 8. Validation

Completed:

- [x] Ethernet cable connected
- [x] Ethernet link active
- [x] DHCP address assigned
- [x] Local SSH connection successful
- [x] Ubuntu package mirror reachable during installation

Pending:

- [ ] Verify default gateway
- [ ] Verify DNS servers
- [ ] Configure DHCP reservation
- [ ] Configure VPN access
- [ ] Configure firewall rules

## Lessons learned

This milestone introduced:

- LAN and WAN
- Network interfaces
- Ethernet connectivity
- DHCP
- IPv4 addressing
- Subnet masks and CIDR notation
- Private versus public IP addresses
- Basic network diagnostics