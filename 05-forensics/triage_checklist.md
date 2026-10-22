# Forensics Triage Checklist

Standard triage procedure for forensics artifacts:

```text
[1. File Type and Strings] -> [2. Embedded Data Extraction] -> [3. Deep Protocol/Memory Analysis]
```

---

## 1. Initial File Inspection
```bash
file target_file
exiftool target_file
strings -n 8 target_file | grep -iE 'flag|ctf|key|pass'
```

---

## 2. Steganography Analysis

### PNG Images
```bash
zsteg -a image.png                   # Inspects all LSB channels
pngcheck -v image.png                # Checks chunk integrity and hidden IHDR data
```

### JPG Images
```bash
binwalk -e image.jpg                 # Extracts embedded files
steghide extract -sf image.jpg       # Extracts hidden data (empty password or wordlist)
stegseek image.jpg /usr/share/wordlists/rockyou.txt
```

### Audio Files (.wav, .mp3)
1. Open file in Audacity.
2. Select audio track dropdown menu next to the track name.
3. Switch display from Waveform to Spectrogram to check for embedded text or QR codes.

---

## 3. Magic Bytes and File Header Repair

Inspect the first 8 bytes of an unrecognized file with `xxd target_file | head`:

| File Type | Hex Signature | ASCII Representation |
| :--- | :--- | :--- |
| **PNG** | `89 50 4E 47 0D 0A 1A 0A` | `.PNG....` |
| **JPG** | `FF D8 FF E0` or `FF D8 FF E1` | `....` |
| **GIF** | `47 49 46 38 39 61` | `GIF89a` |
| **ZIP / DOCX** | `50 4B 03 04` | `PK..` |
| **PDF** | `25 50 44 46` | `%PDF` |
| **ELF (Linux Binary)** | `7F 45 4C 46` | `.ELF` |

Edit corrupted header bytes using `hexedit target_file` and save with `Ctrl+X`.

---

## 4. Network PCAP Analysis (Wireshark)

### Useful Display Filters
```text
http.request.method == "POST"       # Inspect submitted forms and credentials
frame contains "flag"               # Case-sensitive search across packets
frame matches "(?i)flag\{"          # Case-insensitive regex match
tcp.stream eq 0                     # Follow full TCP conversation stream
dns                                 # Check for DNS tunneling or anomalous queries
icmp                                # Inspect data fields in ping requests
```

### File Extraction
- Go to `File` > `Export Objects` > `HTTP...` to download files transferred over unencrypted connections.
- Filter for `Authorization: Basic` to decode base64 HTTP authentication credentials.

---

## 5. Memory Dump Analysis (Volatility 3)
```bash
# Process list and command-line arguments
python3 vol.py -f memory.raw windows.pslist
python3 vol.py -f memory.raw windows.cmdline

# Scan for files on disk
python3 vol.py -f memory.raw windows.filescan | grep -iE 'flag|desktop|secret'

# Dump identified file from virtual address
python3 vol.py -f memory.raw windows.dumpfiles --virtaddr <address>

# Extract password hashes
python3 vol.py -f memory.raw windows.hashdump
```

---

## 6. Raw Binary Bitstreams (1s and 0s Files)

When given a file containing raw ASCII `1` and `0` characters:

### Quick CyberChef Steps
1. Open [CyberChef](https://gchq.github.io/CyberChef/).
2. For text: Add `From Binary` operation (Byte length: 8).
3. For image rendering: Add `From Binary`, then add `Render Image` or click the Save icon in the Output pane to download as raw `.jpg` or `.png`.
4. If output is unreadable, prepend `To Inverted Bitwise` or `XOR` with key `01`.

### Python Parser (Text and QR Code Reconstruction)
```python
import math

with open("data.bin", "r") as f:
    bits = f.read().replace(" ", "").replace("\n", "").strip()

# Check for ASCII text
text = "".join([chr(int(bits[i:i+8], 2)) for i in range(0, len(bits) - (len(bits) % 8), 8)])
print("ASCII output:", text[:100])

# Check for Square Image or QR Code (Length is perfect square)
side = math.isqrt(len(bits))
if side * side == len(bits):
    from PIL import Image
    img = Image.new("1", (side, side))
    # 1 is black (0), 0 is white (255)
    img.putdata([0 if b == "1" else 255 for b in bits])
    img.save("reconstructed.png")
    print(f"Saved {side}x{side} image to reconstructed.png")
```

---

## 7. Checksum and Integrity Verification

### Verify Files Against Known Hash
```bash
# Check single file
sha256sum target_file
md5sum target_file

# Search all files in current directory matching a target SHA-256 hash
sha256sum * | grep "<TARGET_HASH>"

# Windows equivalent in PowerShell / CMD
certutil -hashfile target_file SHA256
Get-FileHash target_file -Algorithm SHA256
```

---

## 8. Compressed Archive Decompression

When encountering unknown compressed archives:

```bash
# Gzip (.gz)
gzip -dc file.gz > uncompressed_output

# Tar archives (.tar, .tar.gz, .tgz)
tar -xvf file.tar
tar -xvzf file.tar.gz

# 7-Zip (supports 7z, rar, zip, iso, dmg, bz2)
7z x file.7z

# Bzip2 (.bz2)
bzip2 -d file.bz2

# XZ (.xz)
xz -d file.xz
```

---

## 9. Recursive Base64 and Metadata Extraction

### Automated Metadata Base64 Scanner
Extract strings from metadata that match Base64 patterns (20 or more characters):
```bash
exiftool target_file | grep -oE '[A-Za-z0-9+/]{20,}={0,2}'
```

### Recursive Base64 Decoder (Python One-Liner)
When data is encoded multiple times in Base64:
```python
import base64

data = "Vm0wd2QyUXlVWGxWV0d4V1YwZDRWMVl3WkRSV01WbDNXa2M1VjFadGNGbFZNakExVjBaS2RHVkdXbGRYYlVaclVteHplRll5U2tWVWJHaG9UVlZ3VjFacWFFOVZNalZUVld4V1ExWnVRbFZXYmtwb1VqQmFZV1JIVmtOQlJFWjVXVmM1YWxkcmVGZFdSVXBvVmtSS1QyUkVUWGxUUmxweVZtMDFRMVp1..."

while True:
    try:
        decoded = base64.b64decode(data).decode('utf-8')
        data = decoded
        print(f"Decoded layer: {data}")
    except Exception:
        print(f"Final plaintext: {data}")
        break
```

---

## 10. Tshark Fast Data Extraction from PCAP

Extract transferred data directly from terminal without navigating Wireshark GUI:

```bash
# Extract HTTP request URLs
tshark -r capture.pcap -Y "http.request" -T fields -e http.request.full_uri

# Extract HTTP POST bodies (passwords, form data)
tshark -r capture.pcap -Y "http.request.method == POST" -T fields -e urlencoded-form.value

# Extract DNS query names (detects DNS data exfiltration)
tshark -r capture.pcap -Y "dns.flags.response == 0" -T fields -e dns.qry.name

# Extract raw data payload bytes
tshark -r capture.pcap -T fields -e data.text
```
