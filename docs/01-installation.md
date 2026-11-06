# 01 — Ubuntu Server Installation

## Objective

Install Ubuntu Server on a physical GMKtec mini-PC to establish the first node of a personal infrastructure and data engineering homelab.

The node will initially be administered remotely using SSH and will later support automation, container orchestration and distributed workloads.

## 1. Hardware inventory

| Component | Configuration |
|---|---|
| Device | GMKtec M8 mini-PC |
| Processor | AMD Ryzen 5 PRO 6650H |
| CPU | 6 cores / 12 threads |
| Memory | 16 GB LPDDR5-6400 |
| Storage | 512 GB NVMe SSD |
| Networking | 2 × Realtek 2.5 GbE |
| Wireless | MediaTek MT7922 |
| Virtualization | AMD hardware virtualization enabled |
| Graphics | Integrated AMD Radeon GPU |

The installed memory is likely soldered and should not be assumed to be upgradeable.

## 2. Prepare the installation USB

The mini-PC was initially running Windows 11.

Required tools:

- Ubuntu Server 26.04.1 LTS AMD64 ISO
- Rufus for Windows
- 8 GB USB flash drive

Procedure:

1. Download the Ubuntu Server AMD64 ISO from the official Ubuntu website.
2. Download Rufus from its official website.
3. Insert the USB flash drive.
4. Open Rufus and select the correct USB device.
5. Select the Ubuntu Server ISO.
6. Use the compatible boot settings detected by Rufus.
7. Write the ISO to the USB device.
8. Wait until Rufus displays `READY`.

**Warning:** Writing the ISO destroys existing data on the selected USB device.

## 3. Boot from USB

1. Keep the installation USB connected.
2. Restart the GMKtec.
3. Repeatedly press `F7` during startup to open the firmware boot menu.
4. Select the UEFI USB entry.
5. Start the Ubuntu Server installer.

The boot menu also displayed the internal Windows Boot Manager, confirming that the installer USB and internal SSD were separate boot devices.

## 4. Installer configuration

Selected options:

| Setting | Choice |
|---|---|
| Language | English |
| Keyboard layout | French |
| Installation type | Ubuntu Server |
| Minimized installation | Disabled |
| Proxy | None |
| Package mirror | Official Ubuntu mirror |
| Ubuntu Pro | Skipped |
| OpenSSH server | Installed |
| SSH password authentication | Enabled temporarily |
| Featured snaps | None |

The standard Ubuntu Server installation was selected to provide a convenient foundation for learning Linux administration.

## 5. Network configuration

The installer detected two Realtek Ethernet interfaces and a MediaTek Wi-Fi interface.

Initially, the network interfaces were not connected.

A Cat 6 Ethernet cable was connected between a LAN port on the home router and the GMKtec.

The active Ethernet interface was configured using automatic IPv4 addressing (DHCP).

The router assigned an address in the `192.168.1.0/24` network.

The Ubuntu package mirror connectivity test succeeded, confirming access to the package repositories.

## 6. Storage configuration

The internal 512 GB NVMe SSD was selected for installation.

Guided partitioning with LVM was enabled.

Approximate layout:

| Mount point / volume | Size | Purpose |
|---|---:|---|
| `/boot/efi` | 1 GB | UEFI boot files |
| `/boot` | 2 GB | Linux kernel and boot files |
| `/` | 100 GB | Root filesystem |
| LVM free extents | 374 GB | Available for future allocation |

The LVM volume group was named `ubuntu-vg`.

This layout preserves capacity for future logical volumes dedicated to application data, containers or other workloads.

**Important:** The installation erased the previous Windows installation on the selected internal SSD.

## 7. Host identity

The system was configured with:

- Hostname: `homelab-01`
- Local administrator: `mouhamadou`

The administrator password is not stored in this repository.

## 8. SSH installation

OpenSSH Server was enabled during installation.

Password authentication was temporarily permitted for initial remote access.

SSH key-based authentication and further hardening are planned for the next infrastructure milestone.

## 9. First boot

After installation:

1. Restart the machine.
2. Remove the installation USB when prompted.
3. Boot Ubuntu from the internal NVMe SSD.
4. Log in using the local administrator account.
5. Verify the network interfaces.

Commands:

```bash
hostname
whoami
ip -br addr
```

Expected hostname:

```text
homelab-01
```

Expected user:

```text
mouhamadou
```

The active Ethernet interface is `enp2s0`.

## 10. Initial remote administration

From the macOS Terminal:

```bash
ssh mouhamadou@<SERVER_LAN_IP>
```

On the first connection, verify and accept the server's SSH host key fingerprint.

Authenticate using the Ubuntu administrator password.

The remote shell prompt should resemble:

```text
mouhamadou@homelab-01:~$
```

This confirms that the server can be administered remotely from the workstation.

## 11. Validation checklist

- [x] Physical hardware detected
- [x] Ubuntu Server installed
- [x] UEFI boot successful
- [x] LVM storage configured
- [x] Ethernet connection established
- [x] DHCP address assigned
- [x] Ubuntu package mirror reachable
- [x] OpenSSH installed
- [x] Local login successful
- [x] Remote SSH login successful
- [ ] Operating system updated
- [ ] SSH key authentication configured
- [ ] Firewall configured
- [ ] Stable LAN address configured

## 12. Lessons learned

This installation introduced several infrastructure concepts:

- UEFI boot management
- Bootable installation media
- Linux network interface naming
- Ethernet link establishment
- DHCP addressing
- Package repositories
- LVM storage management
- SSH remote administration
- Local versus remote shell execution

## Next steps

Continue with system updates, SSH key authentication, network configuration, basic firewall rules and server hardening.