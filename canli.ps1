# VERIQEN canli (gercek LLM) kosu baslatici.
# Kullanim (D:\verqien klasorunde):   .\canli.ps1 VERIQEN-T
#                                     .\canli.ps1 VERIQEN-SI
#                                     .\canli.ps1 B3 -Model openai/gpt-oss-120b -LogDir results/live/run4
#                                     .\canli.ps1 VERIQEN-T -InjectionTasks injection_task_0,injection_task_4
# Birden fazla gorev/saldiri VIRGULLE ayrilir (bosluk degil).
# Klasore gitme ve sanal ortami acma islerini kendisi yapar. Anahtari dosyaya yazmaz.
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$System,
    [string]$Model = "openai/gpt-oss-20b",
    [string]$LogDir = "results/live/run3-20b",
    [string[]]$UserTasks = @("user_task_0", "user_task_3", "user_task_5", "user_task_6"),
    [string[]]$InjectionTasks = @("injection_task_0", "injection_task_4"),
    [ValidateSet("v0", "v1", "v2", "v3", "v4")][string]$JudgePrompt = "v0"
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
    Write-Host "Kosu: $System | model $Model | klasor $LogDir" -ForegroundColor Cyan
    & $python run_live.py --provider groq --model $Model --system $System `
        --user-tasks $UserTasks --injection-tasks $InjectionTasks --logdir $LogDir --judge-prompt $JudgePrompt
} finally {
    Pop-Location
}
