# feat(core): use value of '$env:SCOOP_HOME' if it exsits
# feat(core): set value of '$env:SCOOP_HOME' if it not exsits with 'scoop prefix scoop'
if(!$env:SCOOP_HOME) { $env:SCOOP_HOME = Resolve-Path (scoop prefix scoop) }
# feat(core): set bin/checkhashes.ps1 location with '$env:SCOOP_HOME'
$checkhashes = "$env:SCOOP_HOME/bin/checkhashes.ps1"
# feat(core): set bucket location
$dir = "$PSScriptRoot/../bucket" # checks the parent dir
# feat(core): run bin/checkhashes.ps1
Invoke-Expression -Command "& '$checkhashes' -Dir '$dir' $($args | ForEach-Object { "$_ " })"
