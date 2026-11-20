# VERIQEN hakem test seti calistirici (gercek LLM).
# Kullanim (herhangi bir klasorde):
#   & (Resolve-Path D:\verq*\hakem.ps1) v0
#   & (Resolve-Path D:\verq*\hakem.ps1) v1
#   & (Resolve-Path D:\verq*\hakem.ps1) v2 -Model openai/gpt-oss-120b -Split val
# Kaldigi yerden devam eder. Anahtari dosyaya yazmaz.
param(
    [Parameter(Mandatory = $true, Position = 0)][ValidateSet("v0", "v1", "v2", "v3")][string]$Version,
    [string]$Model = "openai/gpt-oss-20b",
    [ValidateSet("dev", "val", "all")][string]$Split = "dev",
    [string[]]$Ids = @(),
    [string]$Tag = ""
)

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$workdir = Join-Path $PSScriptRoot "experiments\agentdojo"
if (-not (Test-Path $python)) { Write-Host "Sanal ortam bulunamadi: $python" -ForegroundColor Red; exit 1 }

if (-not $env:GROQ_API_KEY) {
    $secure = Read-Host "Groq API anahtarini yapistir (ekranda gorunmez)" -AsSecureString
    if (-not $secure -or $secure.Length -eq 0) { Write-Host "Anahtar girilmedi." -ForegroundColor Red; exit 1 }
    $env:GROQ_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure))
}

$env:PYTHONIOENCODING = "utf-8"
Push-Location $workdir
try {
    Write-Host "Hakem testi: talimat $Version | model $Model | bolme $Split" -ForegroundColor Cyan
    $pyArgs = @("judge_bench.py", "run", "--provider", "groq", "--model", $Model, "--version", $Version,
                "--split", $Split, "--out", "$($Model.Replace('/', '_'))_$($Version)_$($Split)$($Tag).jsonl")
    if ($Ids.Count -gt 0) { $pyArgs += @("--ids", ($Ids -join ",")) }
    & $python @pyArgs
} finally {
    Pop-Location
}
