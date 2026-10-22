# Reverse Engineering Cheatsheet

## 1. Fast Command-Line Recon (Try this before opening Ghidra!)

```bash
file ./binary
strings -n 8 ./binary | grep -iE 'flag|pass|key|correct|wrong'
```

### The `ltrace` Superpower
If the binary uses standard library functions to check flags (like `strcmp`, `strncmp`, `memcmp`), `ltrace` intercepts and prints the comparison in plaintext!
```bash
ltrace ./binary
# Enter dummy password: "AAAA"
# ltrace prints: strcmp("AAAA", "SUPER_SECRET_FLAG_12345") = -1
```

### The `strace` Check
If the binary reads a file or opens a socket:
```bash
strace ./binary 2>&1 | grep -iE 'open|read|flag'
```

---

## 2. Ghidra Quick Guide

1. **Import & Analyze**:
   - `File` $\rightarrow$ `Import File` $\rightarrow$ Select binary.
   - Double-click to open in CodeBrowser.
   - Click **Yes** when prompted to analyze (leave default options checked).
2. **Finding the Main Logic**:
   - In **Symbol Tree** (left pane) $\rightarrow$ Expand **Functions** $\rightarrow$ Click `main`.
   - Inspect the **Decompile** window on the right.
3. **Clean Up Code for Readability**:
   - Press **`L`** on any confusing variable (e.g. `uVar1`) to rename it (e.g. `user_input`, `flag_buffer`).
   - Press **`Ctrl + L`** to retype a variable (e.g. change `undefined4` to `char *`).
4. **Search for Strings**:
   - `Search` $\rightarrow$ `Program Text` or `Search` $\rightarrow$ `For Strings...`
   - Double-click string $\rightarrow$ Right-click in Listing $\rightarrow$ `References` $\rightarrow$ `Show References to Address` to find where the string is used!

---

## 3. Unpacking & Decompilation by File Type

### UPX Packed Binaries
Check if binary says `UPX!` in strings or file header:
```bash
upx -d packed_binary -o unpacked_binary
```

### Python Bytecode (`.pyc` files)
If given a compiled Python file:
```bash
# Using decompyle++ / pycdc:
pycdc challenge.pyc > challenge_decompiled.py

# Using uncompyle6 (for Python 2.7 - 3.8):
uncompyle6 challenge.pyc > challenge_decompiled.py
```

### .NET / C# Executables (Windows PE)
If `file` says: `PE32/PE64 executable ... Mono/.Net assembly`:
- Open directly in **dnSpy** or **ILSpy** (Windows).
- It will decompile back into nearly 100% original C# source code!

### Java (`.jar` or `.class`)
- Open in **JD-GUI** or **CFR**:
```bash
java -jar cfr.jar target.class --outputdir ./decompiled/
```
