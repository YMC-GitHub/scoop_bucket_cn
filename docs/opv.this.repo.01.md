- 代码解释（中文），并添加代码注释和提示（英文）
- rewrite this in typescript
- make emoji to safe
- add a dockerfile to run scripts/update.ts in alpine with nodejs 18 amd typescript
- use pnpm to install typescript
- let this workflow run on this file change
- dup `$PATH` value in alpine in bash
- python + poetry + docker (alpine vs bullseye vs bookworm)
- how to set apt repo with china proxy when passing `ARG NETWORK=cn APT_REPO_CN=mirrors.aliyun.com  APT_REPO_GLOBAL=deb.debian.org`
- how to set pip and poetry repo with china proxy when passing ``ARG NETWORK=cn ARG PIP_REPO_CN=XX`
- rewrie for bash - set vars with default value
- how to use env from .env file
- app deps to pyproject.toml based on requirements.txt
- rewrite these funcs in python (keep funcs names)
- according next bash, rewrite dockerfile

```bash
yours touch scripts/fresh-gh-proxy.py
yours touch requirements.txt
yours touch Dockerfile-python

yours touch docs/ask.for.ai.pip.source.china.md
yours touch docs/ask.for.ai.use-env-file.md

yours touch pyproject.toml
yours touch .env
# sh -c "mv scripts/setup-alpine-all-in-one.sh scripts/setup-alpine.sh"

# sh -c "mv scripts/setup-debian-all-in-one.sh scripts/setup-debian.sh"
# ls -la ./scripts/setup-debian-all-in-one.sh
# chmod +x ./scripts/*.sh

# sh -c "rm scripts/*todel*"
```

## git commit msg
```bash
git add docs/ask.for.ai.*.md
git commit -m "docs(core): put note"

git add docs/not.*.md
git commit -m "docs(core): put note"

git add scripts/update.ts
git commit -m "build(core): use ts to update gh proxy"

git add .github/workflows/files-gh-proxy-update.yml
git commit -m "build(core): use gh workflow to update gh proxy"

git add .github/workflows/files-gh-proxy-update.yml
git commit -m "build(core): fix workflow"


git add .editorconfig
git commit -m "build(core): put eof"

git add .gitattributes
git commit -m "build(core): put linguist-language"

git add .gitignore
git commit -m "build(core): put ignore files"


git add Dockerfile
git add scripts/setup-alpine-apk-repos.sh
git add scripts/ghproxy-url*.txt
git commit -m "build(core): dev in docker(alpine)"


git add Dockerfile-python
git add scripts/*.py
git add requirements.txt
git commit -m "build(core): dev in docker(alpine)"


git add scripts/fresh-gh-proxy.py
git commit -m "scripts(core): fresh gh proxy"

git add scripts/setup-debian.sh
git commit -m "scripts(core): use debian"

git add scripts/setup*.sh
git commit -m "scripts(core): put scripts"

git add .github/workflows/files-gh-proxy-update.yml;
git commit -m "build(core): use py"

git add scripts/fresh-gh-proxy.py
git commit -m "scripts(core): put screenshot name"

git add pyproject.toml requirements.txt;
git commit -m "build(core): use poetry and pyproject file"

git add scripts/fresh-gh-proxy.py
git commit -m "scripts(core): put screenshot name"

git add scripts/.gitignore
git commit -m "build(core): ignore unused files"

git add scripts/README.md
git commit -m "docs(core): put scripts usage"

git add scripts/put-apps-desc.py
git commit -m "scripts(core): put apps desc"

git add README.md template.README.md;
git commit -m "build(core): put apps desc"


git add Dockerfile-python
git commit -m "build(core): use python 3.10 in slim-bookworm"


git add .env
git commit -m "build(core): use .enf file"

git add docs/opv.this.repo*.md
git commit -m "docs(core): put note for opv.this.repo"


git add opv.md
git commit -m "docs(core): add dingtalk"


```
