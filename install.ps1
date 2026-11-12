# Cài/cập nhật kit /eggs (Windows). Ví dụ:
#   powershell -ExecutionPolicy Bypass -File .\install.ps1 --url https://<máy chủ MCP>/mcp
# Tham số: xem .\install.ps1 --help
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
$py = $null
foreach ($c in @(@("py", "-3"), @("python3"), @("python"))) {
  if (Get-Command $c[0] -ErrorAction SilentlyContinue) {
    $v = & $c[0] @($c | Select-Object -Skip 1) -c "import sys; print(sys.version_info[0])" 2>$null
    if ($v -eq "3") { $py = $c; break }
  }
}
if (-not $py) {
  Write-Host "Cần Python 3. Cài bằng: winget install Python.Python.3.12  (rồi mở lại PowerShell)"
  exit 2
}
& $py[0] @($py | Select-Object -Skip 1) "scripts\install.py" @args
exit $LASTEXITCODE
