# Cai hoac cap nhat kit /eggs, khong can git (Windows PowerShell 5.1 / 7).
#   Cai:      irm https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.ps1 | iex
#   Cap nhat: $env:EGGS_KIT_UPDATE='1'; irm https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.ps1 | iex
# Tham so them cho install.ps1 (vd. --keep-old): $env:EGGS_KIT_ARGS='--keep-old' truoc khi chay.
# File nay chi dung ky tu ASCII: irm | iex tren PowerShell 5.1 co the doc sai UTF-8.
& {
  $ErrorActionPreference = "Stop"
  $ProgressPreference = "SilentlyContinue"
  $repo = "eggstech/eggs-agent-kit"
  $branch = if ($env:EGGS_KIT_BRANCH) { $env:EGGS_KIT_BRANCH } else { "main" }
  $dir = if ($env:EGGS_KIT_DIR) { $env:EGGS_KIT_DIR } else { Join-Path $HOME "eggs-agent-kit" }
  $archive = if ($env:EGGS_KIT_ARCHIVE_URL) { $env:EGGS_KIT_ARCHIVE_URL } else { "https://codeload.github.com/$repo/zip/refs/heads/$branch" }
  $mcpUrl = if ($env:EGGS_MCP_URL) { $env:EGGS_MCP_URL } else { "https://jira.eggstech.io.vn/eggs-mcp/mcp" }
  $update = $env:EGGS_KIT_UPDATE -eq "1"
  $extra = @()
  if ($env:EGGS_KIT_ARGS) { $extra = @($env:EGGS_KIT_ARGS -split "\s+" | Where-Object { $_ }) }
  Remove-Item Env:EGGS_KIT_UPDATE -ErrorAction SilentlyContinue

  $hasGit = [bool](Get-Command git -ErrorAction SilentlyContinue)
  if ((Test-Path (Join-Path $dir ".git")) -and $hasGit) {
    # May cai kieu cu (git clone): van cap nhat bang git.
    git -C $dir pull --ff-only -q
    if ($LASTEXITCODE -ne 0) { throw "git pull loi trong $dir" }
  } else {
    $tmp = Join-Path ([IO.Path]::GetTempPath()) ("eggs-kit-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $tmp | Out-Null
    $new = "$dir.new.$PID"
    $old = "$dir.old.$PID"
    try {
      [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
      $zip = Join-Path $tmp "kit.zip"
      Invoke-WebRequest -UseBasicParsing -Uri $archive -OutFile $zip
      $out = Join-Path $tmp "x"
      Expand-Archive -Path $zip -DestinationPath $out
      $src = Get-ChildItem -Path $out -Directory | Select-Object -First 1
      if (-not $src -or -not (Test-Path (Join-Path $src.FullName "skills\eggs\SKILL.md"))) {
        throw "Tai kit loi: khong thay skills\eggs\SKILL.md."
      }
      # Chep ban moi canh thu muc dich, roi doi ten (cung o dia).
      if (Test-Path $new) { Remove-Item -LiteralPath $new -Recurse -Force }
      Copy-Item -LiteralPath $src.FullName -Destination $new -Recurse
      if (Test-Path $dir) { Move-Item -LiteralPath $dir -Destination $old }
      try {
        Move-Item -LiteralPath $new -Destination $dir
      } catch {
        if (Test-Path $dir) { Remove-Item -LiteralPath $dir -Recurse -Force }
        if (Test-Path $old) { Move-Item -LiteralPath $old -Destination $dir }
        throw
      }
      if (Test-Path $old) { Remove-Item -LiteralPath $old -Recurse -Force }
    } finally {
      Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue
      if (Test-Path $new) { Remove-Item -LiteralPath $new -Recurse -Force -ErrorAction SilentlyContinue }
    }
  }

  $m = Select-String -Path (Join-Path $dir "skills\eggs\SKILL.md") -Pattern 'Kit version: `([0-9.]+)`' | Select-Object -First 1
  $ver = if ($m) { $m.Matches[0].Groups[1].Value } else { "?" }
  Write-Host "Kit /eggs $ver at $dir"

  if ($update) {
    Write-Host "Da cap nhat. Doc lai SKILL.md (hoac mo phien moi) de dung ban moi."
    return
  }
  $shell = (Get-Process -Id $PID).Path
  & $shell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $dir "install.ps1") --url $mcpUrl @extra
  if ($LASTEXITCODE -ne 0) { Write-Host "Bo cai bao loi (ma $LASTEXITCODE). Xem thong bao o tren." }
}
