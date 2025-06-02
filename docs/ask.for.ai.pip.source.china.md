在 Docker 中为 `pip install --user -r requirements.txt` 指定国内源，可以通过以下几种方式实现：

---

### **方法 1：直接在 pip 命令中指定镜像源**（推荐）
在 `Dockerfile` 中修改安装命令，添加 `-i` 参数：
```dockerfile
RUN pip install --user -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

**参数说明：**
- `-i`：指定镜像源地址
- `--trusted-host`：标记镜像源为可信（避免 SSL 错误）

---

### **方法 2：通过环境变量全局配置**
在 `Dockerfile` 中设置环境变量：
```dockerfile
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
RUN pip install --user -r requirements.txt
```

---

### **方法 3：创建 pip 配置文件**（持久化生效）
在 `Dockerfile` 中生成配置文件：
```dockerfile
RUN mkdir -p /etc/pip && \
    echo -e "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple\ntrusted-host = pypi.tuna.tsinghua.edu.cn" > /etc/pip.conf
RUN pip install --user -r requirements.txt
```

---

### **国内常用镜像源列表**
| 镜像名称       | URL                                      |
|----------------|-----------------------------------------|
| 清华大学       | `https://pypi.tuna.tsinghua.edu.cn/simple` |
| 阿里云         | `https://mirrors.aliyun.com/pypi/simple`   |
| 腾讯云         | `https://mirrors.cloud.tencent.com/pypi/simple` |
| 华为云         | `https://repo.huaweicloud.com/repository/pypi/simple` |
| 豆瓣           | `https://pypi.doubanio.com/simple`         |

---

### **完整 Dockerfile 示例**
```dockerfile
FROM python:3.11-alpine

# 方法1：直接指定镜像源（推荐）
RUN pip install --user -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn

# 方法2：通过环境变量
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
RUN pip install --user -r requirements.txt

# 方法3：配置文件
RUN mkdir -p /etc/pip && \
    echo -e "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple\ntrusted-host = pypi.tuna.tsinghua.edu.cn" > /etc/pip.conf
RUN pip install --user -r requirements.txt
```

---

### **注意事项**
1. **缓存问题**
   如果镜像源更新不及时，可以强制禁用缓存：
   ```dockerfile
   RUN pip install --no-cache-dir --user -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

2. **企业内网代理**
   如果需要通过代理访问，添加 `--proxy` 参数：
   ```dockerfile
   RUN pip install --user -r requirements.txt \
       --proxy http://your-proxy:port \
       -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. **Alpine 兼容性**
   确保安装的包有 Alpine 兼容的版本（某些包可能需要额外系统依赖）。

---

### **验证是否生效**
构建时观察输出，确认下载地址显示为镜像源域名（如 `tuna.tsinghua.edu.cn`）。如果仍有问题，可以临时添加调试命令：
```dockerfile
RUN pip config list && pip install --user -r requirements.txt
```

选择最适合你场景的方式即可！ 🚀
