# Forensics 10-Minute Triage Checklist

When given an unknown file in Forensics, execute this exact 10-minute triage protocol:

```text
[Step 1: File Type & Strings] ──> [Step 2: Hidden Files (binwalk/zsteg)] ──> [Step 3: Protocol/Hex Fix]
```

---

## Step 1: Basic Inspection
```bash
file target_file
exiftool target_file                 # Check metadata, comments, GPS, author
strings -n 8 target_file | grep -iE 'flag|ctf|key|pass'
```

---

## Step 2: Steganography (Images & Audio)

### PNG Images
```bash
zsteg -a image.png                   # Checks all LSB channels (Solves 70% of PNG stego!)
pngcheck -v image.png                # Checks for corrupted chunks / hidden IHDR data
```

### JPG Images
```bash
binwalk -e image.jpg                 # Extract embedded zip/files
steghide extract -sf image.jpg       # Hit Enter for empty passphrase, or crack with stegseek:
stegseek image.jpg /usr/share/wordlists/rockyou.txt
```

### Audio (.wav / .mp3)
1. Open in **Audacity**.
2. Click the track dropdown (arrow next to audio name) $\rightarrow$ Switch from **Waveform** to **Spectrogram**.
3. Look for text or QR code drawn directly into the high audio frequencies!

---

## Step 3: Magic Bytes / File Header Fix
If `file target_file` says `data` or won't open in an image viewer, check the first 8 bytes with `xxd target_file | head`:

| Format | Correct Magic Bytes (Hex) | ASCII |
| :--- | :--- | :--- |
| **PNG** | `89 50 4E 47 0D 0A 1A 0A` | `.PNG....` |
| **JPG** | `FF D8 FF E0` or `FF D8 FF E1` | `....` |
| **GIF** | `47 49 46 38 39 61` (GIF89a) | `GIF89a` |
| **ZIP / DOCX** | `50 4B 03 04` | `PK..` |
| **PDF** | `25 50 44 46` | `%PDF` |
| **ELF (Linux)**| `7F 45 4C 46` | `.ELF` |

*Fixing via hexedit:*
```bash
hexedit target_file   # Overwrite the broken starting bytes and save with Ctrl+X
```

---

## Step 4: Network PCAP Analysis (Wireshark & Tshark)

### Top Wireshark Display Filters
```text
http.request.method == "POST"       # Look for submitted passwords or form data
frame contains "flag"               # Case-sensitive search
frame matches "(?i)flag\{"          # Case-insensitive regex search
tcp.stream eq 0                     # Right-click packet -> Follow -> TCP Stream
dns                                 # Check for DNS exfiltration (look at queried subdomains)
icmp                                # Check ICMP data payload for exfiltrated bytes
```

### Fast Extraction in Wireshark
- **Export Transferred Files**: `File` $\rightarrow$ `Export Objects` $\rightarrow$ `HTTP...` (Downloads images, zip files, scripts transferred over plaintext).
- **Credentials Extraction**: Search for `Authorization: Basic` (base64 decoded credentials).

---

## Step 5: Memory Analysis (Volatility 3)
```bash
# 1. Process tree / running commands
python3 vol.py -f memory.raw windows.pslist
python3 vol.py -f memory.raw windows.cmdline

# 2. File scanning & dumping
python3 vol.py -f memory.raw windows.filescan | grep -iE 'flag|desktop|secret'
python3 vol.py -f memory.raw windows.dumpfiles --virtaddr <address_from_filescan>

# 3. Dump password hashes
python3 vol.py -f memory.raw windows.hashdump
```
