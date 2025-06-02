Here's how to properly clean up temporary build dependencies in Alpine Linux after using `--virtual .build-deps`:

### **Cleanup Method (Best Practice)**
```dockerfile
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev && \
    # Your build commands here && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*
```

### **Breakdown:**
1. **Install build dependencies**
   Marked as virtual package `.build-deps`:
   ```dockerfile
   RUN apk add --no-cache --virtual .build-deps \
       gcc \
       musl-dev \
       libffi-dev
   ```

2. **Run your build commands**
   (e.g., `pip install` or compilation):
   ```dockerfile
   pip install --no-cache-dir some-package
   ```

3. **Cleanup in the same RUN layer**
   Prevents build tools from bloating the final image:
   ```dockerfile
   apk del .build-deps && \
   rm -rf /var/cache/apk/*
   ```

---

### **Complete Docker Example**
```dockerfile
FROM alpine:latest

# Install and cleanup in one layer
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev && \
    pip install --no-cache-dir cryptography && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*

# Verify cleanup
RUN apk info | grep -E 'gcc|musl-dev'  # Should return nothing
```

---

### **Key Points:**
1. **Single RUN layer**
   Combining install/build/cleanup prevents intermediate bloat.

2. **Cache cleanup**
   `rm -rf /var/cache/apk/*` removes downloaded package files.

3. **Verification**
   Check remaining packages with `apk info`.

4. **Alternative for multi-stage builds**
   Even cleaner approach:
   ```dockerfile
   # Build stage
   FROM alpine as builder
   RUN apk add --virtual .build-deps gcc musl-dev...
   RUN pip install...

   # Final stage
   FROM alpine
   COPY --from=builder /usr/local /usr/local
   ```

---

### **Why This Matters**
- Reduces image size by ~50-100MB
- Removes potential security risks from build tools
- Follows Docker best practices

For Python projects, this is especially crucial when compiling C extensions (like `cryptography` or `numpy`).
