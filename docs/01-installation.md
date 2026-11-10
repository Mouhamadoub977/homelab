# Host Provisioning & Storage Baseline

## Scope

This document records the initial provisioning of `homelab-01`, a physical GMKtec M8 host running Ubuntu Server 26.04.1 LTS. It captures the hardware baseline, installation decisions, storage layout and post-installation checks.

The host is the first and currently only compute node. High availability, automated rebuilds and disaster recovery are not yet implemented.

## 1. Hardware baseline

| Component | Recorded configuration |
|---|---|
| Platform | GMKtec M8 mini-PC |
| Processor | AMD Ryzen 5 PRO 6650H |
| CPU topology | 6 cores / 12 threads |
| Memory | 16 GB LPDDR5-6400 |
| Primary storage | 512 GB NVMe SSD |
| Wired networking | 2 × Realtek 2.5 GbE |
| Wireless | MediaTek MT7922 |
| Graphics | Integrated AMD Radeon GPU |
| Virtualization | AMD hardware virtualization enabled during setup |

Firmware inventory reports four 4 GB LPDDR5-6400 memory devices (16 GB total). Ubuntu currently exposes approximately 11.9 GiB of usable RAM. The AMD Radeon 680M driver reports 3072 MiB of VRAM, consistent with a substantial integrated GPU memory reservation. Additional firmware and kernel reservations may apply. Hardware values should be reconfirmed before they are used as sizing guarantees.

Recommended inventory capture:

```bash
lscpu
free -h
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
ip -br link
sudo dmidecode -t system -t memory
```

## 2. Installation method

The system was migrated from its original Windows 11 installation to Ubuntu Server using an Ubuntu Server 26.04.1 LTS AMD64 installation image written to a USB drive with Rufus.

- Boot mode: UEFI.
- Firmware boot menu: `F7` on the GMKtec.
- Installation profile: standard Ubuntu Server, not minimized.
- Locale: English; keyboard: French.
- Package source: official Ubuntu mirror; no proxy configured.
- Ubuntu Pro: skipped.
- OpenSSH Server: selected during installation.
- Additional featured snaps: none selected.

The installer booted from the USB device and targeted the internal NVMe SSD. The installation replaced the previous Windows system.

**Provisioning constraint:** this was an interactive installation, not an unattended or reproducible image-based deployment. Automated provisioning is a future milestone.

## 3. Storage design

Guided partitioning with LVM was selected. The recorded approximate layout is:

| Partition / logical volume | Approximate size | Function |
|---|---:|---|
| `/boot/efi` | 1 GB | UEFI boot files |
| `/boot` | 2 GB | Kernel and boot artifacts |
| `/` | 100 GB | Root filesystem |
| Unallocated extents within `ubuntu-vg` | 374 GB | Capacity reserved for future logical volumes |

The volume group is named `ubuntu-vg`.

### Design rationale

Keeping the initial root filesystem smaller than the physical SSD leaves room for later separation of container data, database storage and other workloads into dedicated logical volumes. LVM enables flexible logical-volume allocation and resizing, subject to filesystem and available-capacity constraints.

**Current limit:** the available extents are not yet assigned to application volumes. The storage layout was verified on 2026-11-10 using `lsblk`, `df`, `pvs`, `vgs` and `lvs`: the NVMe disk reports 476.9 GiB, the `ubuntu-vg` volume group approximately 473.89 GiB, the root logical volume 100 GiB, and approximately 373.89 GiB of unallocated LVM extents. A fresh inventory is required before allocating storage to application workloads.

Validation commands:

```bash
lsblk -f
df -hT
sudo pvs
sudo vgs
sudo lvs -a -o +devices
```

LVM is a volume-management mechanism, not a substitute for backups or recovery testing.

## 4. Network and host identity

During installation, the host was connected to the home router through a Cat 6 Ethernet cable. DHCP was used for IPv4 configuration, and the Ubuntu package mirror was reachable.

| Setting | Recorded value |
|---|---|
| Hostname | `homelab-01` |
| Administrative account | `mouhamadou` |
| Active Ethernet interface | `enp2s0` |
| Observed LAN IPv4 | `192.168.1.12` |
| Address assignment | DHCP |

The LAN address is observational, not a verified permanent reservation. Network interface inventory, Netplan behavior and the subsequent remote access deployment are documented separately in [Network Architecture & Connectivity](02-networking.md).

## 5. Initial access and subsequent hardening

OpenSSH Server was installed during provisioning. Password-based SSH access was temporarily enabled for initial administration.

After successful public-key authentication was established, the server was hardened using a dedicated OpenSSH drop-in. The validated baseline now includes:

- Ed25519 public-key login from macOS.
- Password and keyboard-interactive SSH authentication disabled.
- Direct root SSH login disabled.
- Private remote administration through Tailscale.

These controls were applied **after** the original OS installation and should not be mistaken for installer defaults. Implementation and validation are documented in [SSH Administration & Access Hardening](03-ssh.md).

## 6. Post-installation validation

The initial boot completed successfully from the internal NVMe SSD after removal of the installation media. The host was reachable over Ethernet and could be administered remotely.

Observed checks across subsequent provisioning work:

| Area | Validation | Result |
|---|---|---|
| Host identity | `hostname`, `whoami` | Expected host and administrator |
| Network | `ip -br addr` | Active Ethernet and assigned IPv4 |
| Package access | Installer mirror connectivity test | Successful |
| SSH | Remote interactive login | Successful |
| System packages | OS updates applied | Completed during baseline work |
| Boot / network readiness | Reboot and `systemctl --failed` | No failed units after Netplan remediation |
| Remote administration | SSH through Tailscale from an external network | Successful |

A later login banner reported Ubuntu Server 26.04.1 LTS and kernel `7.0.0-43-generic`. It also reported three devices with available firmware upgrades. The firmware update status has not been investigated or remediated in this documentation.

For a fresh verification snapshot:

```bash
hostnamectl
uname -r
uptime
systemctl --failed
sudo apt update
apt list --upgradable
sudo fwupdmgr get-upgrades
```

The last two commands inspect available updates; they do not install them.

## 7. Operational gaps and next milestones

- Capture and version a sanitized hardware/storage inventory.
- Define logical-volume allocation and filesystem strategy for data services.
- Document backup scope, recovery objectives and a tested restore procedure.
- Assess available firmware upgrades before scheduling maintenance.
- Review firewall and network exposure.
- Automate baseline configuration with Ansible.
- Define a reproducible provisioning or rebuild process.

## Related documentation

- [Network Architecture & Connectivity](02-networking.md)
- [SSH Administration & Access Hardening](03-ssh.md)
- [Infrastructure Architecture](../diagrams/architecture.md)
