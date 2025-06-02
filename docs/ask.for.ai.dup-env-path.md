In **Alpine Linux** (or any Unix-like system), if your `$PATH` contains duplicate entries like:

```
/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```
*(Notice `/usr/local/bin` appears twice)*

You can **remove duplicates** while preserving order using:

---

### **1. Using `awk` (Best for Alpine’s minimal `ash`)**
```sh
PATH=$(echo "$PATH" | awk -v RS=: '!a[$0]++ {printf "%s%s", (NR==1 ? "" : ":"), $0}')
```
**How it works:**
- Splits `PATH` by `:` and keeps only the first occurrence of each entry.
- Maintains original order.

**Example:**
```sh
echo "$PATH"
# Before: /usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin

PATH=$(echo "$PATH" | awk -v RS=: '!a[$0]++ {printf "%s%s", (NR==1 ? "" : ":"), $0}')

echo "$PATH"
# After: /usr/local/bin:/usr/local/sbin:/usr/bin:/bin
```

---

### **2. Using `tr` + `sort -u` (Less order-preserving)**
*(Not recommended—may reorder paths)*
```sh
PATH=$(echo "$PATH" | tr ':' '\n' | sort -u | tr '\n' ':' | sed 's/:$//')
```

---

### **3. For a Permanent Fix in Alpine Docker**
Add this to your `Dockerfile`:
```dockerfile
RUN echo "export PATH=$(echo \"\$PATH\" | awk -v RS=: '!a[\$0]++ {printf \"%s%s\", (NR==1 ? \"\" : \":\"), \$0}')" >> /etc/profile
```

---

### **Why This Matters**
- **Performance**: Duplicate paths slow down command lookup.
- **Predictability**: Ensures the first occurrence takes precedence.

Let me know if you need further tweaks! 🐧
