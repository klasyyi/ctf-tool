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
3. If output is unreadable, prepend `To Inverted Bitwise` or `XOR` with key `01`.

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
