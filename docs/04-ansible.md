# 04 — Ansible: inventory, audit and privilege escalation

**Validated 2026-11-18 from terminal output.** The controller is the MacBook Air (Ansible Core 2.18.7); the target is `homelab-01` (Ubuntu 26.04.1). The SSH alias `homelab` and the dedicated Ed25519 private key exist on macOS, not on Ubuntu.

## Tests performed

```bash
ssh homelab "hostname"
ansible all -i 'homelab,' -m ansible.builtin.ping
ansible-inventory -i ansible/inventory/hosts.yml --graph
ansible all -i ansible/inventory/hosts.yml -m ansible.builtin.ping
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/system-audit.yml -K
```

Results: hostname `homelab-01`, Ansible `pong`, audit recap `ok=7 changed=0 unreachable=0 failed=0 skipped=1`. The audit gathered operating system, host, CPU, RAM, NIC names and read UFW status (`inactive`); a conditional "UFW active" message was correctly skipped.

## sudo-rs interaction

Default sudo path was configured by `update-alternatives` to `/usr/lib/cargo/bin/sudo` (sudo-rs). SSH interactive sudo worked, but Ansible `become` timed out waiting for its escalation prompt.

An explicit alternative succeeded:
```bash
ansible homelab -i ansible/inventory/hosts.yml \
  -m ansible.builtin.command -a 'id -un' -b -K \
  -e 'ansible_become_exe=/usr/bin/sudo.ws'
```

Result `root`. Subsequently, adding `ansible_become_exe: /usr/bin/sudo.ws` under the host in the inventory allowed `-b -K` to succeed without `-e`. This avoids changing Ubuntu's system-wide sudo choice.

**Security:** inventory references an SSH key path only; never commit the private key, password, or real secret variables.

## Key concepts

- `hosts` targets hosts/groups; `gather_facts` reads system attributes.
- `become: true` requests privilege escalation to root by default; `-K` prompts locally for the become password.
- `register` captures command output including `stdout` and `rc`.
- `changed_when: false` changes *reporting*, not actual command effects.
- `when` prevents execution when its expression is false; that task is `skipped`.
- Quote a YAML `when` value containing `Status: active`, e.g. `when: 'ufw_result.stdout | trim == "Status: active"'`.

**Follow-up learning:** host/group variables, roles, handlers, Vault, idempotence, testing, CI and automatic deployment. Firewall activation remains deferred until local console access.
