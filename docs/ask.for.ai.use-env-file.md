Here's how to use environment variables from a `.env` file in combination with your Docker build, with support for both bash scripts and Docker:

### 1. First, create a `.env` file in your project root:

```ini
# .env file
NETWORK=cn
APT_REPO_CN=mirrors.aliyun.com
APT_REPO_GLOBAL=deb.debian.org
APT_REPO_FILE=/etc/apt/sources.list.d/debian.sources
PIP_REPO_CN=https://pypi.tuna.tsinghua.edu.cn/simple
PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
PIP_REPO_GLOBAL=https://pypi.org/simple
POETRY_REPO_CN=https://pypi.tuna.tsinghua.edu.cn/simple
POETRY_REPO_GLOBAL=https://pypi.org/simple
PYTHON_VERSION=3.10-slim-bookworm
```

### 2. Update the bash script to source from `.env`:

```bash
#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Set default values if not set in .env
NETWORK=${NETWORK:-"cn"}
APT_REPO_CN=${APT_REPO_CN:-"mirrors.aliyun.com"}
APT_REPO_GLOBAL=${APT_REPO_GLOBAL:-"deb.debian.org"}
APT_REPO_FILE=${APT_REPO_FILE:-"/etc/apt/sources.list.d/debian.sources"}
PIP_REPO_CN=${PIP_REPO_CN:-"https://pypi.tuna.tsinghua.edu.cn/simple"}
PIP_TRUSTED_HOST=${PIP_TRUSTED_HOST:-"pypi.tuna.tsinghua.edu.cn"}
PIP_REPO_GLOBAL=${PIP_REPO_GLOBAL:-"https://pypi.org/simple"}
POETRY_REPO_CN=${POETRY_REPO_CN:-"https://pypi.tuna.tsinghua.edu.cn/simple"}
POETRY_REPO_GLOBAL=${POETRY_REPO_GLOBAL:-"https://pypi.org/simple"}

# Rest of your script remains the same...
[configure_apt_repo, configure_pip_repo, configure_poetry_repo functions]
```

### 3. Update your Dockerfile to use the `.env` file:

```dockerfile
# syntax=docker/dockerfile:1

# First stage: load .env file for build arguments
FROM alpine as env_loader
WORKDIR /app
COPY .env ./
RUN apk add --no-cache gettext && \
    envsubst < .env > .env.substituted

# Main build stage
FROM python:${PYTHON_VERSION} as builder

# Copy substituted .env file
COPY --from=env_loader /app/.env.substituted ./.env

# Install gettext for envsubst if needed
RUN apt-get update && apt-get install -y --no-install-recommends gettext && rm -rf /var/lib/apt/lists/*

# Copy and make executable
COPY setup-repos.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/setup-repos.sh

# Source .env and run configuration
RUN . ./.env && /usr/local/bin/setup-repos.sh set_apt_repo && \
    . ./.env && /usr/local/bin/setup-repos.sh set_pip_repo && \
    . ./.env && /usr/local/bin/setup-repos.sh set_poetry_repo

# Rest of your Dockerfile...
[rest of your build stages]
```

### 4. Alternative Docker Approach (recommended):

A simpler way is to use `docker-compose` which has built-in `.env` support:

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      args:
        - NETWORK=${NETWORK}
        - APT_REPO_CN=${APT_REPO_CN}
        - APT_REPO_GLOBAL=${APT_REPO_GLOBAL}
        - PIP_REPO_CN=${PIP_REPO_CN}
        - PIP_REPO_GLOBAL=${PIP_REPO_GLOBAL}
        - POETRY_REPO_CN=${POETRY_REPO_CN}
        - POETRY_REPO_GLOBAL=${POETRY_REPO_GLOBAL}
    environment:
      - NETWORK=${NETWORK}
      - PIP_INDEX_URL=${PIP_REPO_CN}
      - PIP_TRUSTED_HOST=${PIP_TRUSTED_HOST}
```

### 5. Usage Examples:

**With bash script directly:**
```bash
# Just run the script - it will auto-load .env
./setup-repos.sh set_apt_repo

# Or override specific variables
NETWORK=global ./setup-repos.sh set_apt_repo
```

**With Docker build:**
```bash
# Using docker-compose (auto-loads .env)
docker-compose build

# Using plain docker build
docker build -t myapp .
```

**With docker run:**
```bash
# Using variables from .env
docker run --env-file .env myapp

# Overriding specific variables
docker run -e NETWORK=global myapp
```

### Key Benefits:

1. **Single source of truth** - All configurations in `.env`
2. **Flexible overrides** - Can override any variable at runtime
3. **Consistent behavior** - Same variables work in bash and Docker
4. **Security** - Keep sensitive configurations out of scripts/Dockerfiles
5. **Easy maintenance** - Change configurations in one place

Remember to add `.env` to your `.gitignore` if it contains sensitive information!
