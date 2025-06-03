## update bucket text (tsx)
```bash
# replace "https://ghproxy.com" to  "https://ghfast.top" in bucket/*.json
tsx scripts/update.ts bucket "https://ghproxy.com" "https://ghfast.top"
```

## update bucket text (github + workflow)
- get more on `.github/workflows/files-gh-proxy-update.yml`


## update bucket text (docker)
- win -> wsl(alpine)->docker(alpine)

```bash
# login default wsl machine
# wsl


prefix="zero";name="scoop-bucket";
# sh -c "rm -f Dockerfile; cp Dockerfile-alpine Dockerfile;"

# 为中国网络构建
docker build --build-arg NETWORK_REGION=cn -t ${prefix}-${name}:cn .

# 为国际网络构建
# docker build --build-arg NETWORK_REGION=global -t ${prefix}-${name}:global .

# 添加 DOCKERFILE LABEL
# docker build --build-arg NETWORK_REGION=cn -t ${prefix}-${name}:cn --label "dockerfile=$(cat Dockerfile | base64)" .

# 查看 DOCKERFILE LABEL
# docker inspect ${prefix}-${name}:cn --format '{{index .Config.Labels "dockerfile"}}' | base64 -d

# sh -c "docker images | grep ${prefix}.*"

# docker images -q --filter "reference=${prefix}-${name}*"
# docker images -q --filter "reference=${prefix}*"


# docker image ls --format "{{.ID}} {{.Repository}} {{.Tag}}" | grep "${prefix}-${name}"

# del untaged images
# docker rmi $(docker images -f "dangling=true" -q)

# get images id with prefix
# docker images --format "{{.ID}} {{.Repository}}" | grep "${prefix}" | awk '{print $1}'
# del images wih prefix
# docker rmi $(docker images --format "{{.ID}} {{.Repository}}" | grep "${prefix}" | awk '{print $1}')

# get images name and tag  with prefix
# docker images --format "{{.Repository}}:{{.Tag}}" | grep "${prefix}"

# login bash of docker(alpine)
# docker run --rm -it --name ${prefix}-${name} -v ./bucket:/app/bucket ${prefix}-${name}:cn /bin/sh


# login bash of docker(alpine)
# docker exec -it "${prefix}-${name}:cn" /bin/sh
#

# tsx scripts/update.ts ./bucket "https://ghproxy.com" "https://ghfast.top"

docker exec -it "${prefix}-${name}:cn" /bin/sh tsx scripts/update.ts ./bucket "https://ghproxy.com" "https://ghfast.top"
```

## code scripts in development in local - docker(alpine)
```bash
docker run --rm -it --name ${prefix}-${name} -v ./bucket:/app/bucket -v ./scripts:/app/scripts ${prefix}-${name}:cn /bin/sh
# node --version;npm --version;pnpm --version;tsx --version;
# tree .;

# edit(code) scripts
# ...

# tsx scripts/update.ts ./bucket "https://ghproxy.com" "https://ghfast.top"
echo "https://ghproxy.com" > ./scripts/ghproxy-url.txt
echo "https://ghfast.top" > ./scripts/ghproxy-url-latest.txt
tsx scripts/update.ts ./bucket ./scripts/ghproxy-url.txt ./scripts/ghproxy-url-latest.txt
```


## fresh gh proxy (docker)
- win -> wsl(alpine) -> docker(alpine) -> python(alpine)

```bash
# login default wsl machine
# wsl

# poetry + docker (bookworm)
prefix="zero";name="poetry-bookworm";dockerfile="Dockerfile-python";python_version="3.10-slim-bookworm";
# poetry + docker (bullseye)
prefix="zero";name="poetry-bullseye";dockerfile="Dockerfile-python";python_version="3.10-slim-bullseye";

prefix="zero";name="playwright-python";dockerfile="Dockerfile-python";python_version="3.10-alpine";
prefix="zero";name="playwright-python";dockerfile="Dockerfile-python";python_version="3.10-slim";
# prefix="zero";name="playwright-python-debian";dockerfile="Dockerfile-python-debian";python_version="3.10-slim";

# sh -c "rm -f Dockerfile; cp Dockerfile-alpine Dockerfile;"
# sh -c "rm -f Dockerfile-python; cp Dockerfile-python-alpine Dockerfile-python;"

# build image for china network
docker build --build-arg NETWORK_REGION=cn -t ${prefix}-${name}:cn -f $dockerfile .

docker build --build-arg NETWORK_REGION=cn  --build-arg PYTHON_VERSION=3.10-slim -t ${prefix}-${name}:cn -f $dockerfile .


# build image for global network
# docker build --build-arg NETWORK_REGION=global -t ${prefix}-${name}:global -f $dockerfile .

# 添加 DOCKERFILE LABEL
# docker build --build-arg NETWORK_REGION=cn -t ${prefix}-${name}:cn --label "dockerfile=$(cat Dockerfile | base64)" -f $dockerfile .

# 查看 DOCKERFILE LABEL
# docker inspect ${prefix}-${name}:cn --format '{{index .Config.Labels "dockerfile"}}' | base64 -d

# sh -c "docker images | grep ${prefix}.*"

# docker images -q --filter "reference=${prefix}-${name}*"
# docker images -q --filter "reference=${prefix}*"


# docker image ls --format "{{.ID}} {{.Repository}} {{.Tag}}" | grep "${prefix}-${name}"

# del untaged images
# docker rmi $(docker images -f "dangling=true" -q)

# get images id with prefix
# docker images --format "{{.ID}} {{.Repository}}" | grep "${prefix}" | awk '{print $1}'
# del images wih prefix
# docker rmi $(docker images --format "{{.ID}} {{.Repository}}" | grep "${prefix}" | awk '{print $1}')

# get images name and tag  with prefix
# docker images --format "{{.Repository}}:{{.Tag}}" | grep "${prefix}"

# login bash of docker(alpine)
# docker run --rm -it --name ${prefix}-${name} -v ./scripts:/app/scripts ${prefix}-${name}:cn /bin/sh

# login bash of docker(alpine)
# docker exec -it "${prefix}-${name}:cn" /bin/sh

# tsx scripts/update.ts ./bucket "https://ghproxy.com" "https://ghfast.top"

# docker run --rm playwright-python pip config list



docker exec -it "${prefix}-${name}:cn" /bin/sh python scripts/fresh-gh-proxy.py
```
```bash
python --version;pip --version;

# pip config list ;pip config get global.index-url;

echo "$PATH"

```

```bash
chmod +x ./scripts/*.sh;
./scripts/setup-alpine-apk-repos.sh
./scripts/setup-pip-repos.sh
./scripts/setup-alpine-path.sh

./scripts/setup-alpine-all-in-one.sh set_apk_repo
./scripts/setup-alpine-all-in-one.sh set_pip_repo
./scripts/setup-alpine-all-in-one.sh dup_env_path

# case:1
./scripts/setup-debian.sh set_apt_repo
./scripts/setup-debian.sh set_pip_repo
./scripts/setup-debian.sh dup_env_path

# case:2
./scripts/setup-debian.sh all

# case:3
./scripts/setup-debian.sh set_apt_repo
./scripts/setup-debian.sh setup_poetry

# get python and pip version
# python --version;pip --version;

# get pip config
# pip config list

# install poetry
# pip install --no-cache-dir poetry

# pip install --root-user-action ignore --no-cache-dir playwright==1.52.0 && playwright install --with-deps chromium;
# pip index versions BeautifulSoup4
# pip install --root-user-action ignore --no-cache-dir BeautifulSoup4==4.13.4
#

# poetry add playwright@1.52.0 && playwright install --with-deps chromium;

# poetry install --no-cache --no-interaction --no-ansi

# run app
# python scripts/fresh-gh-proxy.py

# pip list --format=freeze > requirements.txt

# pip list playwright BeautifulSoup4 --format=freeze
```

## debug - python + debian(bookworm) + docker
```bash
docker run --rm -it --name 3.10-slim-bookworm -w /app -v ./scripts:/app/scripts python:3.10-slim-bookworm /bin/bash
# tree .
# ls -al scripts/
```
