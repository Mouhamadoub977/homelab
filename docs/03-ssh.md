# 03 — SSH Remote Administration

## Objective

Enable secure remote administration of the Ubuntu Server from a macOS workstation using SSH.

This milestone establishes the foundation for managing the homelab without requiring a monitor, keyboard or mouse connected to the server.

## 1. What is SSH?

SSH stands for Secure Shell.

It is a network protocol that provides encrypted communication between two machines.

In this homelab:

- SSH client: MacBook Air
- SSH server: GMKtec running Ubuntu Server
- Hostname: `homelab-01`
- SSH port: TCP 22
- Authentication: Password (temporary)

SSH allows the administrator to execute Linux commands remotely.

## 2. Client-server architecture

```text
MacBook Air
SSH Client
     |
     | Encrypted SSH connection
     | TCP port 22
     |
     v
GMKtec Mini PC
Ubuntu Server
OpenSSH Server
homelab-01
192.168.1.12
```

Both machines currently communicate over the same local network.

## 3. Install OpenSSH Server

OpenSSH Server was selected during the Ubuntu Server installation.

Installer options:

- Install OpenSSH Server: Enabled
- Allow password authentication over SSH: Enabled
- Import SSH identity: Not configured

Password authentication was enabled to simplify initial access.

It will later be replaced with SSH key-based authentication.

## 4. Establish the first connection

From the macOS Terminal:

```bash
ssh mouhamadou@192.168.1.12
```

Command breakdown:

- `ssh`: Launch the SSH client.
- `mouhamadou`: Remote Linux username.
- `@`: Separates username and hostname/IP address.
- `192.168.1.12`: Private IPv4 address of the Ubuntu Server.

The SSH client connects to TCP port 22 by default.

## 5. First connection: host authenticity

On the first connection, SSH displayed a message similar to:

```text
The authenticity of host '192.168.1.12' can't be established.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

This is a normal security mechanism.

SSH asks whether the client should trust the server's public host key.

After verifying the server's host key fingerprint through a trusted channel, the administrator can accept it by typing:

```text
yes
```

The key is then recorded in the client's `~/.ssh/known_hosts` file.

For this initial setup, the host key was accepted, but an independent fingerprint comparison was not documented.

For future servers, fingerprint verification should be part of the provisioning procedure.

## 6. Initial connection issue

The first SSH connection attempt failed with:

```text
ssh_dispatch_run_fatal:
Connection to 192.168.1.12 port 22: Broken pipe
```

A broken pipe indicates that the SSH connection was interrupted.

The exact cause was not established.

A subsequent connection attempt succeeded without requiring additional server configuration.

Therefore, the incident is recorded as a transient connection failure rather than an identified configuration issue.

## 7. Successful connection

The second connection attempt succeeded.

The terminal displayed:

```text
mouhamadou@homelab-01:~$
```

This confirms that the shell is running on the remote Ubuntu Server.

Commands entered at this prompt execute on the GMKtec, not on the MacBook.

## 8. Initial validation commands

### Verify hostname

```bash
hostname
```

Observed result:

```text
homelab-01
```

### Verify logged-in user

```bash
whoami
```

Observed result:

```text
mouhamadou
```

### Verify network interfaces

```bash
ip -br addr
```

The active Ethernet interface was:

```text
enp2s0  UP  192.168.1.12/24
```

These checks confirmed that the administrator was connected to the expected machine and that the server had an active network interface.

## 9. Close the SSH session

To end the remote session:

```bash
exit
```

The terminal displayed:

```text
logout
Connection to 192.168.1.12 closed.
```

The shell returned to the local macOS prompt.

Closing an SSH session does not shut down the Ubuntu Server.

The server continues running independently.

## 10. SSH authentication: current state

Current configuration:

- OpenSSH Server installed
- SSH connection established successfully
- Password authentication enabled
- SSH key authentication not yet configured
- Remote access restricted by current network topology

Planned improvements:

1. Generate an SSH key pair on the MacBook.
2. Install the public key on the Ubuntu Server.
3. Verify key-based authentication.
4. Configure appropriate SSH access restrictions.
5. Disable password authentication only after confirming key-based access.
6. Configure the firewall while preserving SSH connectivity.

**Important:** Never disable password authentication before verifying that an alternative administrative login method works.

## 11. Remote access outside the LAN

The address `192.168.1.12` is private and cannot be used to reach the home server directly across the public Internet.

A secure VPN will be introduced later.

Potential solutions:

- WireGuard
- Tailscale

Direct SSH port forwarding from the router to the public Internet is not planned.

## 12. Security considerations

Never commit the following to Git:

- Private SSH keys
- Passwords
- Authentication tokens
- Credentials
- Sensitive configuration files

The private key should remain on the administration workstation.

Only the corresponding public key should be installed on the server.

## 13. Validation checklist

- [x] OpenSSH Server installed
- [x] SSH client available on macOS
- [x] First host key accepted
- [x] Remote login successful
- [x] Hostname verified
- [x] Username verified
- [x] Network interface verified
- [x] Remote session closed successfully
- [ ] SSH public-key authentication configured
- [ ] SSH configuration hardened
- [ ] Firewall configured
- [ ] VPN access configured

## Lessons learned

This milestone introduced:

- SSH client-server architecture
- Encrypted remote administration
- TCP ports
- Host identity and fingerprints
- The `known_hosts` file
- Local versus remote shell sessions
- Password versus public-key authentication
- Basic SSH troubleshooting

## Next steps

Configure SSH key authentication and basic server security before introducing remote VPN access and infrastructure automation.