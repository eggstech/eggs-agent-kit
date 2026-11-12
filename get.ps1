# Cài hoặc cập nhật kit /eggs, không cần git (Windows PowerShell).
#   Cài:      irm https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.ps1 | iex
#   Cập nhật: $env:EGGS_KIT_UPDATE='1'; irm https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.ps1 | iex
# Tham số thêm cho install.ps1 (vd. --keep-old): đặt $env:EGGS_KIT_ARGS='--keep-old' trước khi chạy.
& {
  $ErrorActionPreference = "Stop"
  $repo = "eggstech/eggs-agent-kit"
  $branch = if ($env:EGGS_KIT_BRANCH) { $env:EGGS_KIT_BRANCH } else { "main" }
  $dir = if ($env:EGGS_KIT_DIR) { $env:EGGS_KIT_DIR } else { Join-Path $HOME "eggs-agent-kit" }
  $archive = if ($env:EGGS_KIT_ARCHIVE_URL) { $env:EGGS_KIT_ARCHIVE_URL } else { "https://codeload.github.com/$repo/zip/refs/heads/$branch" }
  $mcpUrl = if ($env:EGGS_MCP_URL) { $env:EGGS_MCP_URL } else { "https://jira.eggstech.io.vn/eggs-mcp/mcp" }
  $update = $env:EGGS_KIT_UPDATE -eq "1"
  $extra = if ($env:EGGS_KIT_ARGS) { $env:EGGS_KIT_ARGS -split "\s+" | Where-Object { $_ } } else { @() }
  Remove-Item Env:EGGS_KIT_UPDATE -ErrorAction SilentlyContinue

  if ((Test-Path (Join-Path $dir ".git")) -and (Get-Command git -ErrorAction SilentlyContinue)) {
    # Máy cài kiểu cũ (git clone): vẫn cập nhật bằng git.
    git -C $dir pull --ff-only -q
    if ($LASTEXITCODE -ne 0) { throw "git pull lỗi trong $dir" }
  } else {
    $tmp = Join-Path ([IO.Path]::GetTempPath()) ("eggs-kit-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $tmp | Out-Null
    try {
      [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
      $zip = Join-Path $tmp "kit.zip"
      Invoke-WebRequest -UseBasicParsing -Uri $archive -OutFile $zip
      $out = Join-Path $tmp "x"
      Expand-Archive -Path $zip -DestinationPath $out
      $src = Get-ChildItem -Path $out -Directory | Select-Object -First 1
      if (-not $src -or -not (Test-Path (Join-Path $src.FullName "skills\eggs\SKILL.md"))) {
        throw "Tải kit lỗi: không thấy skills\eggs\SKILL.md."
      }
      $old = "$dir.old.$PID"
      if (Test-Path $dir) { Move-Item -LiteralPath $dir -Destination $old }
      try {
        Copy-Item -LiteralPath $src.FullName -Destination $dir -Recurse
      } catch {
        if (Test-Path $old) { Move-Item -LiteralPath $old -Destination $dir }
        throw
      }
      if (Test-Path $old) { Remove-Item -LiteralPath $old -Recurse -Force }
    } finally {
      Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue
    }
  }

  $ver = (Select-String -Path (Join-Path $dir "skills\eggs\SKILL.md") -Pattern 'Kit version: `([0-9.]+)`' | Select-Object -First 1).Matches.Groups[1].Value
  Write-Host "Kit /eggs $ver tại $dir"

  if ($update) {
    Write-Host "Đã cập nhật. Đọc lại SKILL.md (hoặc mở phiên mới) để dùng bản mới."
    return
  }
  & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $dir "install.ps1") --url $mcpUrl @extra
}
