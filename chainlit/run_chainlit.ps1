[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Sample = "chainlit_chat.py",

    [switch]$List,

    [switch]$Headless,

    [switch]$Watch,

    [ValidateRange(1, 65535)]
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Definition
$repositoryDirectory = Split-Path -Parent $scriptDirectory
$pythonPath = Join-Path $repositoryDirectory ".venv-chainlit\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
    throw "Python 3.13 virtual environment not found at '$pythonPath'. Create it with: py -3.13 -m venv .venv-chainlit"
}

$samples = @(Get-ChildItem -LiteralPath $scriptDirectory -Filter "*.py" -File | Sort-Object Name)

if ($List) {
    Write-Host "Available Chainlit samples:"
    $samples | ForEach-Object { Write-Host "  $($_.Name)" }
    exit 0
}

$samplePath = Join-Path $scriptDirectory $Sample
if (-not (Test-Path -LiteralPath $samplePath -PathType Leaf)) {
    throw "Sample '$Sample' was not found. Run '$($MyInvocation.MyCommand.Name) -List' to see the available samples."
}

$sampleFile = Get-Item -LiteralPath $samplePath
if ($sampleFile.Extension -ne ".py") {
    throw "Sample '$Sample' is not a Python file."
}

$requiredVariables = switch -Wildcard ($sampleFile.Name) {
    "chainlit_anthropic*" { @("ANTHROPIC_API_KEY"); break }
    "chainlit_openrouter*" { @("OPENROUTER_API_KEY"); break }
    "chainlit_openai_data_analyst*" { @("OPENAI_API_KEY", "OPENAI_ASSISTANT_ID"); break }
    default { @("OPENAI_API_KEY"); break }
}

$missingVariables = @(
    $requiredVariables | Where-Object {
        [string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($_))
    }
)

if ($missingVariables.Count -gt 0) {
    throw "Missing environment variable(s): $($missingVariables -join ', ')"
}

$pythonVersion = & $pythonPath --version 2>&1
Write-Host "Using $pythonVersion"
Write-Host "Starting $($sampleFile.Name) at http://127.0.0.1:$Port"

$chainlitArguments = @(
    "-m",
    "chainlit",
    "run",
    $sampleFile.FullName,
    "--host",
    "127.0.0.1",
    "--port",
    $Port.ToString()
)

if ($Headless) {
    $chainlitArguments += "--headless"
}

if ($Watch) {
    $chainlitArguments += "--watch"
}

Push-Location $scriptDirectory
try {
    & $pythonPath @chainlitArguments
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}