# Reverse Engineering Cheatsheet

## 1. Command-Line Analysis

Inspect basic file metadata and strings:
```bash
file ./binary
strings -n 8 ./binary | grep -iE 'flag|pass|key|correct|wrong'
```

### Dynamic Tracing with ltrace
If the binary uses standard C library comparison functions (`strcmp`, `strncmp`, `memcmp`), `ltrace` displays arguments in cleartext during execution:
```bash
ltrace ./binary
```

### System Call Tracing with strace
Inspect file system calls, network connections, and input/output operations:
```bash
strace ./binary 2>&1 | grep -iE 'open|read|flag'
```

---

## 2. Ghidra Analysis Workflow

1. Import and analyze:
   - Go to `File` > `Import File` and select target binary.
   - Open file in CodeBrowser and run default automatic analysis.
2. Locate entry point:
   - In `Symbol Tree` > `Functions`, locate and select `main`.
   - Inspect the generated C code in the `Decompile` pane.
3. Variable refactoring:
   - Select variable and press `L` to rename.
   - Press `Ctrl + L` to reassign data types (such as `char *` or `int`).
4. Cross references:
   - Search strings using `Search` > `For Strings...`.
   - Right-click selected string in Listing, then select `References` > `Show References to Address`.

---

## 3. Unpacking and Decompilation

### UPX Packed Binaries
Check for UPX headers in strings:
```bash
upx -d packed_binary -o unpacked_binary
```

### Python Bytecode (.pyc)
Decompile compiled Python bytecode:
```bash
# Using decompyle++ / pycdc:
pycdc challenge.pyc > decompiled.py

# Using uncompyle6 (for Python 2.7 to 3.8):
uncompyle6 challenge.pyc > decompiled.py
```

### .NET / C# Executables (Windows PE)
If the binary is a .NET assembly, decompile with:
- dnSpy
- ILSpy

These tools decompile assemblies directly into C# source code.

### Java Bytecode (.class / .jar)
Decompile Java archives using CFR or JD-GUI:
```bash
java -jar cfr.jar target.class --outputdir ./decompiled/
```
