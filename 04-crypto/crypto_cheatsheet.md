# Cryptography Cheatsheet

## 1. Online Ciphers and Automated Solvers

Use [dcode.fr](https://www.dcode.fr/) for classic ciphers and frequency analysis:
- Cipher identification: [dcode.fr/cipher-identifier](https://www.dcode.fr/cipher-identifier)
- Caesar cipher and Rot13
- Vigenere cipher (analyzes key length automatically)
- Affine and substitution ciphers
- Transposition and rail fence ciphers

---

## 2. XOR Operations in Python

### Single-Byte XOR Brute Force
```python
def single_byte_xor(ciphertext_bytes):
    for key in range(256):
        decrypted = bytes([b ^ key for b in ciphertext_bytes])
        if b"flag{" in decrypted.lower() or b"ctf{" in decrypted.lower():
            print(f"[+] Key {key} ({chr(key)}): {decrypted}")
```

### Repeating-Key XOR (Known Plaintext Attack)
When the flag format is known (example: starts with `flag{`):
```python
ciphertext = bytes.fromhex("<HEX_STRING>")
known_plaintext = b"flag{"

# Deriving initial key bytes
derived_key = bytes([c ^ p for c, p in zip(ciphertext[:len(known_plaintext)], known_plaintext)])
print(f"Key prefix: {derived_key}")
```

---

## 3. Hash Identification and Cracking

### Length Reference Table
| Algorithm | Hash Length (Hex Characters) | Hashcat Mode |
| :--- | :--- | :--- |
| **MD5** | 32 | `-m 0` |
| **SHA-1** | 40 | `-m 100` |
| **SHA-256** | 64 | `-m 1400` |
| **SHA-512** | 128 | `-m 1700` |
| **SHA-512 Crypt** | Starts with `$6$` | `-m 1800` |
| **Bcrypt** | Starts with `$2y$` or `$2a$` | `-m 3200` |

### Hash Lookup and Cracking
1. Check online database: [crackstation.net](https://crackstation.net/)
2. Run Hashcat with a wordlist:
   ```bash
   hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt
   ```
3. Run John the Ripper:
   ```bash
   john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
   ```

---

## 4. CyberChef Multi-Step Decoding

When analyzing nested or unknown encoding formats:
1. Open [CyberChef](https://gchq.github.io/CyberChef/).
2. Add the `Magic` operation to the recipe pipeline.
3. Enable `Intensive mode` and set depth to 3.
4. CyberChef tests combinations of Base64, Hex, URL-encoding, Gzip, and character shifts to extract readable text.
