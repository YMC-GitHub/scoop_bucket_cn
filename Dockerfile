# ARG ALPINE_VERSION=3.18
# FROM alpine:${ALPINE_VERSION}

ARG NODE_VERSION=18-alpine
FROM node:${NODE_VERSION}

LABEL org.opencontainers.image.authors="ymc-github <yemiancheng@gmail.com>; yemiancheng <yemiancheng1993@163.com>"

ENV TIMEZONE=Asia/Shanghai

ARG NETWORK=cn APK_REPO_CN=mirrors.aliyun.com APK_REPO_GLOBAL=dl-cdn.alpinelinux.org
COPY scripts/setup-alpine-apk-repos.sh /usr/local/bin/setup-alpine-apk-repos.sh
RUN chmod +x /usr/local/bin/setup-alpine-apk-repos.sh && /usr/local/bin/setup-alpine-apk-repos.sh

# Set working directory
WORKDIR /app

# Install pnpm and TypeScript globally
RUN npm install -g pnpm nrm typescript tsx

# Copy package.json and pnpm-lock.yaml (if they exist)
# COPY package*.json pnpm-lock.yaml* ./

# Copy TypeScript configuration (if it exists)
# COPY tsconfig*.json ./

# Copy source files
COPY scripts/*.ts ./scripts/

# Install dependencies using pnpm
# RUN pnpm install

# Compile TypeScript
# RUN pnpm tsc

# Set the command to run the script
CMD ["tsc", "scripts/update.js"]
