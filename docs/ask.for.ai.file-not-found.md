It looks like you're encountering the error `/bin/sh: ./scripts/setup-alpine-path.sh: not found` when trying to execute a script in your Alpine Linux container, despite the file clearly existing in your directory structure. Here's how to diagnose and fix this issue:

---

### **Root Cause**
This typically happens due to:
1. **Missing execute permissions** (`chmod +x`)
2. **Windows-style line endings** (CRLF instead of LF)
3. **Shell interpreter mismatch** (e.g., script requires `bash` but runs in `sh`)
4. **File not actually existing at runtime** (Docker build context issue)

---

### **Solution Steps**

#### **1. Verify File Exists in Container**
```bash
# Inside container:
ls -la ./scripts/setup-alpine-path.sh
```
- If missing, ensure it's copied in your `Dockerfile`:
  ```dockerfile
  COPY ./scripts/setup-alpine-path.sh /app/scripts/
  ```

#### **2. Add Execute Permissions**
```bash
chmod +x ./scripts/setup-alpine-path.sh
```
Or in `Dockerfile`:
```dockerfile
RUN chmod +x /app/scripts/setup-alpine-path.sh
```

#### **3. Fix Line Endings (CRLF → LF)**
```bash
# Install dos2unix if needed
apk add dos2unix

# Convert line endings
dos2unix ./scripts/setup-alpine-path.sh
```
Or in `Dockerfile`:
```dockerfile
RUN apk add --no-cache dos2unix && \
    dos2unix /app/scripts/setup-alpine-path.sh
```

#### **4. Verify Shebang Line**
Ensure the first line of `setup-alpine-path.sh` is:
```bash
#!/bin/sh
```
(For Alpine compatibility, avoid `#!/bin/bash` unless you've installed bash)

#### **5. Run with Explicit Interpreter**
```bash
sh ./scripts/setup-alpine-path.sh
```

---

### **Complete Dockerfile Example**
```dockerfile
FROM alpine:latest

WORKDIR /app

# Copy scripts with correct permissions
COPY ./scripts/ ./scripts/
RUN chmod +x ./scripts/*.sh && \
    dos2unix ./scripts/*.sh

# Run the script
CMD ["sh", "./scripts/setup-alpine-path.sh"]
```

---

### **Debugging Checklist**
| Issue | Test Command | Fix |
|-------|-------------|-----|
| File missing? | `ls -la /app/scripts/` | Adjust `COPY` in Dockerfile |
| Permissions? | `ls -la /app/scripts/setup-alpine-path.sh` | `chmod +x` |
| Line endings? | `cat -v setup-alpine-path.sh` (look for `^M`) | `dos2unix` |
| Shebang wrong? | `head -1 setup-alpine-path.sh` | Change to `#!/bin/sh` |

---

### **Key Takeaways**
1. Alpine uses `sh` (not `bash`) by default
2. Windows CRLF breaks scripts in Linux
3. Docker `COPY` preserves permissions but not execute bits

Let me know if you still see issues after trying these! 🐳
