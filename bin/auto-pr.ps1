param(
    # feat(core): bind -upstream to set github_name/repo_name:bransh_name
    [String]$upstream = "ymc-github/scoop_bucket_cn:main"
)

# feat(core): use value of '$env:SCOOP_HOME' if it exsits
# feat(core): set value of '$env:SCOOP_HOME' if it not exsits with 'scoop prefix scoop'
if(!$env:SCOOP_HOME) { $env:SCOOP_HOME = Resolve-Path (scoop prefix scoop) }
# feat(core): set bin/auto-pr.ps1 location with '$env:SCOOP_HOME'
$autopr = "$env:SCOOP_HOME/bin/auto-pr.ps1"
# feat(core): set bucket location
$dir = "$PSScriptRoot/../bucket" #

# feat(core): run bin/auto-pr.ps1
Invoke-Expression -command "& '$autopr' -dir '$dir' -upstream $upstream $($args | ForEach-Object { "$_ " })"
