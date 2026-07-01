# Запустить один раз на новом компе после git clone/pull
# Создаёт junction, чтобы Claude читал память из git-репо

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$claudeMemoryPath = "C:\Users\Denis\.claude\projects\c--Users-Denis-Desktop--------\memory"

if (Test-Path $claudeMemoryPath) {
    Remove-Item $claudeMemoryPath -Recurse -Force
}

New-Item -ItemType Directory -Force -Path (Split-Path $claudeMemoryPath) | Out-Null
cmd /c mklink /J "$claudeMemoryPath" "$repoRoot"

Write-Host "Junction created: $claudeMemoryPath -> $repoRoot"
