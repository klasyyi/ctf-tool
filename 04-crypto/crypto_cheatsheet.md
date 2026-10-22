# Cryptography Cheatsheet & Quick Solver

## 1. The Best Online Solver: [dcode.fr](https://www.dcode.fr/)
If you encounter any of these classic ciphers, do not write code manually—paste into dcode.fr:
- **Cipher Identifier**: [dcode.fr/cipher-identifier](https://www.dcode.fr/cipher-identifier) (Detects ~200 cipher types automatically!)
- **Caesar / Rot13 / Rot47**
- **Vigenere Cipher** (Solves even without the key!)
- **Affine / Substitution Cipher**
- **Rail Fence / Baconian / Polybius**

---

## 2. XOR Operations (Python Snippets)

### Single-Byte XOR Brute Force
```python
def single_byte_xor(ciphertext_bytes):
    for key in range(256):
        decrypted = bytes([b ^ key for b in ciphertext_bytes])
        # Check for standard flag formats
        if b"flag{" in decrypted.lower() or b"ctf{" in decrypted.lower():
            print(f"[+] Key {key} ({chr(key)}): {decrypted}")

# Example:
# single_byte_xor(bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"))
```

### Repeating-Key XOR (Known Plaintext Attack)
If you know the flag begins with `flag{`:
```python
cipher = bytes.fromhex("...")
known_plain = b"flag{"
# key[i] = cipher[i] ^ known_plain[i]
key = bytes([c ^ p for c, p in zip(cipher[:len(known_plain)], known_plain)])
print(f"Probable Key start: {key}")
```

---

## 3. Hash Cracking Quick Checklist

1. **Identify Hash**:
   - Length 32 hex chars $\rightarrow$ MD5 (`hashcat -m 0`)
   - Length 40 hex chars $\rightarrow$ SHA-1 (`hashcat -m 100`)
   - Length 64 hex chars $\rightarrow$ SHA-256 (`hashcat -m 1400`)
   - Starts with `$6$` $\rightarrow$ SHA-512 crypt (`hashcat -m 1800`)
   - Starts with `$2y$` $\rightarrow$ Bcrypt (`hashcat -m 3200`)
2. **Instant Online Lookup**:
   - [crackstation.net](https://crackstation.net/) (Fastest, billions of pre-computed hashes)
3. **John the Ripper / Hashcat**:
   ```bash
   hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt
   john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
   ```

---

## 4. CyberChef Magic Recipes
When you have an unknown encoded string (e.g. `H4sIA...` or `PD9wa...`):
1. Paste string into [CyberChef](https://gchq.github.io/CyberChef/).
2. Drag the **Magic** operation into the Recipe box.
3. Turn on **Intensive mode** and set Depth to 3.
4. CyberChef will automatically chain Base64, Gzip, Hex, URL-decoding, and Rot13 to reveal plaintext!
