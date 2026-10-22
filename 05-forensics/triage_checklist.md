# Forensics Triage Handbook

A structured, step-by-step triage guide for CTF forensics challenges.

---

## Quick Navigation by Artifact Type
0. [Phase 0: One-Liner Flag Grabbers (Cheatcodes)](#0-one-liner-flag-grabbers-cheatcodes)
1. [Phase 1: Universal 60-Second Initial Triage](#1-universal-60-second-initial-triage)
2. [Phase 2: Images and Steganography](#2-images-and-steganography)
3. [Phase 3: Corrupted Files and Header Repair](#3-corrupted-files-and-header-repair)
4. [Phase 4: Compressed Archives](#4-compressed-archives)
5. [Phase 5: Raw Bitstreams and Encoding (1s, 0s, Base64)](#5-raw-bitstreams-and-encoding)
6. [Phase 6: Network Captures (Wireshark and Tshark)](#6-network-captures-pcap)
7. [Phase 7: Memory Forensics (Volatility 3)](#7-memory-forensics-volatility-3)
8. [Phase 8: Deep Multi-Layer Reconnaissance](#8-deep-multi-layer-reconnaissance)

---

## 0. One-Liner Flag Grabbers (Cheatcodes)

Run these automated one-liners first. If a challenge author left the flag unencrypted inside nested layers or non-standard encodings, these commands extract it immediately:

### 1. Multi-Encoding String Sweep (ASCII, UTF-16LE, UTF-16BE)
Standard `strings` only reads 7-bit ASCII. Windows memory dumps, Office files, and registry entries often store flags in 16-bit Little Endian (`l`). This scans all encodings at once:
```bash
for enc in s S b l B L; do strings -a -e $enc target_file; done | grep -iE 'flag\{|ctf\{'
```

### 2. Recursive Matryoshka Carve and Search
Recursively extracts all nested archives inside images, documents, or binaries, then greps through all unpacked files:
```bash
binwalk -e -M target_file && grep -rnoaEi 'flag\{[^}]+\}' _*extracted/
```

### 3. Automated Stream Base64 Decoder
Extracts every Base64 string from a file, attempts decoding in memory, and searches for flag headers:
```bash
grep -oE '[A-Za-z0-9+/]{20,}={0,2}' target_file | while read -r line; do echo "$line" | base64 -d 2>/dev/null; done | grep -iE 'flag\{|ctf\{'
```

### 4. Direct PCAP Flag Scanner
Scans all packets in a capture file for plain or regex flag patterns without opening Wireshark:
```bash
tshark -r capture.pcap -Y 'frame matches "(?i)flag\{"' -T fields -e frame.number -e data.text -e text
```

### 5. Instant PNG LSB Flag Search
Runs `zsteg` across all color channels and filters directly for flag formats:
```bash
zsteg -a image.png | grep -iE 'flag\{|ctf\{'
```

---

## 1. Universal 60-Second Initial Triage
Run these four commands on any unknown file before attempting complex tools:

```bash
# 1. Determine actual file type (ignores file extension)
file target_file

# 2. Search for plain text flags or passwords
strings -n 8 target_file | grep -iE 'flag|ctf|key|pass'

# 3. Inspect metadata and scan for hidden Base64 strings
exiftool target_file
exiftool target_file | grep -oE '[A-Za-z0-9+/]{20,}={0,2}'

# 4. Check integrity or verify against provided hashes
sha256sum target_file
sha256sum * | grep "<TARGET_HASH>"
```

---

## 2. Images and Steganography

### PNG Images
PNG files often hide data in Least Significant Bits (LSB) or custom metadata chunks:
```bash
# Check all LSB channels (primary PNG stego tool)
zsteg -a image.png

# Check for corrupted chunks or hidden text in IHDR/IDAT
pngcheck -v image.png
```

### JPG / JPEG Images
JPG compression destroys LSB data. Data is usually appended to EOF or embedded with a password:
```bash
# Check for appended files or archives
binwalk -e image.jpg

# Extract steghide payload (press Enter for empty passphrase)
steghide extract -sf image.jpg

# Brute-force steghide password with rockyou wordlist
stegseek image.jpg /usr/share/wordlists/rockyou.txt
```

### Audio Files (.wav, .mp3)
1. Open the file in Audacity.
2. Click the dropdown arrow next to the track title.
3. Select **Spectrogram** (look for text, numbers, or QR codes drawn in high frequencies).

---

## 3. Corrupted Files and Header Repair

If `file target_file` reports `data`, the magic bytes at the start of the file are corrupted.

### Step 1: Check Current Header
```bash
xxd target_file | head -n 2
```

### Step 2: Standard Magic Bytes Reference Table
| Format | Required Starting Hex Bytes | ASCII Indicator |
| :--- | :--- | :--- |
| **PNG** | `89 50 4E 47 0D 0A 1A 0A` | `.PNG....` |
| **JPG / JPEG** | `FF D8 FF E0` or `FF D8 FF E1` | `....` (JFIF or Exif) |
| **GIF** | `47 49 46 38 39 61` | `GIF89a` |
| **ZIP / DOCX** | `50 4B 03 04` | `PK..` |
| **PDF** | `25 50 44 46` | `%PDF` |
| **ELF (Linux)**| `7F 45 4C 46` | `.ELF` |
| **GZIP** | `1F 8B 08` | `...` |

### Step 3: Repair Header
Use a hex editor to overwrite the first corrupted bytes:
```bash
hexedit target_file
# Type the correct hex bytes, press Ctrl+X to save and exit.
```

---

## 4. Compressed Archives

When given an archive or when `binwalk` extracts compressed streams:

```bash
# Gzip archive (.gz)
gzip -dc file.gz > extracted_content

# Tar archive (.tar, .tar.gz, .tgz)
tar -xvf file.tar
tar -xvzf file.tar.gz

# 7-Zip (handles zip, 7z, rar, bz2, iso)
7z x file.7z

# Bzip2 (.bz2)
bzip2 -d file.bz2

# XZ (.xz)
xz -d file.xz
```

---

## 5. Raw Bitstreams and Encoding

### 1s and 0s Files (.bin or .txt)
When given a file containing only ASCII `1` and `0` characters:

1. **Option A: Plain Text Conversion (CyberChef)**
   - Open CyberChef.
   - Add `From Binary` operation (Byte length: 8).
   - If output is unreadable, prepend `To Inverted Bitwise` or `XOR` with key `01`.

2. **Option B: Reconstruct Square Image / QR Code (Python)**
   If the bit count is a square number ($21^2, 25^2, 29^2, 33^2$):
   ```python
   import math
   from PIL import Image

   with open("data.bin", "r") as f:
       bits = f.read().replace(" ", "").replace("\n", "").strip()

   side = math.isqrt(len(bits))
   if side * side == len(bits):
       img = Image.new("1", (side, side))
       # 1 = black (0), 0 = white (255)
       img.putdata([0 if b == "1" else 255 for b in bits])
       img.save("reconstructed_qr.png")
       print(f"Generated {side}x{side} image: reconstructed_qr.png")
   ```

### Recursive Base64 Decoder
When a string or password is encoded through multiple layers of Base64:
```python
import base64

data = "PASTE_ENCODED_STRING_HERE"

while True:
    try:
        data = base64.b64decode(data).decode('utf-8')
        print(f"Decoded layer: {data}")
    except Exception:
        print(f"Final result: {data}")
        break
```

---

## 6. Network Captures (.pcap / .pcapng)

### Essential Wireshark Display Filters
```text
http.request.method == "POST"       # Submitted login forms and passwords
frame contains "flag"               # Search payload text (case-sensitive)
frame matches "(?i)flag\{"          # Search payload text with regex (case-insensitive)
tcp.stream eq 0                     # Follow full TCP communication stream
dns.flags.response == 0             # Inspect outbound DNS requests (DNS exfiltration)
icmp                                # Check ICMP ping payloads for hidden data
```

### File Extraction in Wireshark
- Go to `File` > `Export Objects` > `HTTP...` to export transferred documents and files.

### Fast Command-Line Extraction (Tshark)
Extract fields directly without opening the Wireshark GUI:
```bash
# Extract full URLs requested over HTTP
tshark -r capture.pcap -Y "http.request" -T fields -e http.request.full_uri

# Extract HTTP POST bodies (submitted credentials)
tshark -r capture.pcap -Y "http.request.method == POST" -T fields -e urlencoded-form.value

# Extract DNS queried domains
tshark -r capture.pcap -Y "dns.flags.response == 0" -T fields -e dns.qry.name

# Extract raw data payload bytes
tshark -r capture.pcap -T fields -e data.text
```

---

## 7. Memory Forensics (Volatility 3)

For memory dump files (`.raw`, `.dmp`, `.vmem`):

```bash
# 1. List running processes and command line arguments
python3 vol.py -f memory.raw windows.pslist
python3 vol.py -f memory.raw windows.cmdline

# 2. Search for flag, desktop files, or configuration secrets
python3 vol.py -f memory.raw windows.filescan | grep -iE 'flag|desktop|secret|pass'

# 3. Dump a specific file using its virtual memory address
python3 vol.py -f memory.raw windows.dumpfiles --virtaddr <VIRTUAL_ADDRESS>

# 4. Extract Windows NTLM password hashes
python3 vol.py -f memory.raw windows.hashdump
```

---

## 8. Deep Multi-Layer Reconnaissance

When initial triage fails and you suspect multi-layered or obfuscated artifacts:

### 1. Entropy Analysis
Identify whether data is plain, compressed, or encrypted:
```bash
binwalk -E target_file
```
- Flat line around 0.0 to 0.4: Empty or padded space.
- Medium line around 0.5 to 0.7: Plain text or uncompressed executable code.
- High flat line around 0.9 to 1.0: Compressed archive (zip, gz) or encrypted data.

### 2. Deep File Carving (Foremost)
Extracts all embedded files (PNG, JPG, PDF, ZIP) even when file system metadata is destroyed:
```bash
foremost -i target_file -o carved_output/
```

### 3. Bulk Extractor
Scans raw unformatted disk, memory, or network dumps for URLs, email addresses, IP packets, and AES keys:
```bash
bulk_extractor -o bulk_out/ target_file
```

### 4. PDF Embedded File Extraction
PDF challenges often embed secret files or scripts inside PDF stream objects:
```bash
# Check PDF metadata and embedded attachments
pdfinfo target.pdf

# List embedded files
pdfdetach -list target.pdf

# Extract all embedded files
pdfdetach -saveall target.pdf
```

### 5. Encrypted ZIP / Archive Password Cracking
When an extracted archive requires a password:
```bash
# Fast ZIP cracker using rockyou
fcrackzip -u -D -p /usr/share/wordlists/rockyou.txt encrypted.zip

# Or extract hash and crack using John the Ripper
zip2john encrypted.zip > zip.hash
john --wordlist=/usr/share/wordlists/rockyou.txt zip.hash
```
