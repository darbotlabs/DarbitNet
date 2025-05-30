# Requires -RunAsAdministrator

<#
.SYNOPSIS
Sets up the complete BitNet environment on Windows.

.DESCRIPTION
Installs the toolchain, configures Miniconda, builds bitnet.cpp and downloads
the default model. Run from an elevated PowerShell prompt.

.EXAMPLE
pwsh -File .\setup-bitnet.ps1
#>

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
    Write-Error "Please run this script as Administrator.";
    exit 1
}

Start-Transcript -Path setup-log.txt -Append

function Round1 {
    Write-Output "=== Round 1: Install Chocolatey and Toolchain ==="
    if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
        Set-ExecutionPolicy Bypass -Scope Process -Force
        powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr https://community.chocolatey.org/install.ps1 -UseBasicParsing | iex"
    }
    choco install -y git python3 cmake llvm clang ninja 7zip visualstudio2022buildtools
    choco install -y visualstudio2022buildtools --params "'/Quiet /Add Microsoft.VisualStudio.Workload.VCTools /Add Microsoft.VisualStudio.Component.VC.CMake.Project /Add Microsoft.VisualStudio.Component.VC.Llvm.Clang /Add Microsoft.VisualStudio.Component.VC.Llvm.ClangToolset /Add Microsoft.VisualStudio.Component.VC.Llvm.ClangToolset.MSBuild'"
    git --version; $gitStatus = $LASTEXITCODE
    python --version; $pythonStatus = $LASTEXITCODE
    cmake --version; $cmakeStatus = $LASTEXITCODE
    clang --version; $clangStatus = $LASTEXITCODE
    ninja --version; $ninjaStatus = $LASTEXITCODE
    if ($gitStatus -eq 0 -and $pythonStatus -eq 0 -and $cmakeStatus -eq 0 -and $clangStatus -eq 0 -and $ninjaStatus -eq 0) {
        Write-Output "✅ ROUND 1 PASS"
    } else {
        throw "❌ ROUND 1 FAIL"
    }
}

function Round2 {
    Write-Output "=== Round 2: Install Miniconda and create env ==="
    if (-not (Test-Path 'C:\Miniconda3\Scripts\conda.exe')) {
        $minInstaller = "$env:TEMP\miniconda.exe"
        Invoke-WebRequest -Uri 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe' -OutFile $minInstaller
        & $minInstaller /S /InstallationType=AllUsers /AddToPath=1 /RegisterPython=0 /D=C:\Miniconda3
    }
    $env:PATH += ';C:\Miniconda3;C:\Miniconda3\Scripts'
    conda create -y -n bitnet-cpp python=3.9 | Out-Null
    conda info --envs | Select-String 'bitnet-cpp' > $null
    $envStatus = $?
    conda run -n bitnet-cpp python -c "print('Py OK')" > $null
    $pyStatus = $?
    if ($envStatus -and $pyStatus) {
        Write-Output "✅ ROUND 2 PASS"
    } else {
        throw "❌ ROUND 2 FAIL"
    }
}

function Round3 {
    Write-Output "=== Round 3: Clone repository and install Python deps ==="
    $repoPath = $PSScriptRoot
    if (-not (Test-Path (Join-Path $repoPath '.git'))) {
        git clone --recursive https://github.com/darbotlabs/DarbotNet.git $repoPath
    }
    Set-Location $repoPath
    git submodule update --init --recursive # ensures 3rdparty/llama.cpp is present
    conda run -n bitnet-cpp pip install -r requirements.txt
    $hasFile = Test-Path "$repoPath\src\CMakeLists.txt"
    conda run -n bitnet-cpp python -c "import torch, sentencepiece, numpy, tqdm, packaging, huggingface_hub; print('Deps OK')" > $null
    $pyOk = $?
    if ($hasFile -and $pyOk) {
        Write-Output "✅ ROUND 3 PASS"
    } else {
        throw "❌ ROUND 3 FAIL"
    }
}

function Round4 {
    Write-Output "=== Round 4: Build bitnet.cpp ==="
    Import-Module "$Env:ProgramFiles\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Microsoft.VisualStudio.DevShell.dll"
    Enter-VsDevShell -SkipAutomaticLocation -DevCmdArguments "-arch=x64 -host_arch=x64"
    if (-not (Test-Path build)) { New-Item -Type Directory -Path build | Out-Null }
    Set-Location build
    cmake -G 'Ninja' -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ ..
    cmake --build . --config Release
    $dll = Test-Path '.\bin\bitnet_cpp.dll'
    if ($dll) {
        Write-Output "✅ ROUND 4 PASS"
    } else {
        throw "❌ ROUND 4 FAIL"
    }
    Set-Location ..
}

function Round5 {
    Write-Output "=== Round 5: Download model and quantize ==="
    if ($Env:HF_TOKEN) { huggingface-cli login --token $Env:HF_TOKEN }
    huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models\BitNet-b1.58-2B-4T
    conda run -n bitnet-cpp python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s
    $modelOk = Test-Path 'models\BitNet-b1.58-2B-4T\ggml-model-i2_s.gguf'
    if ($modelOk) {
        Write-Output "✅ ROUND 5 PASS"
    } else {
        throw "❌ ROUND 5 FAIL"
    }
}

function Round6 {
    Write-Output "=== Round 6: Smoke test inference ==="
    $output = conda run -n bitnet-cpp python run_inference.py -m models/BitNet-b1.58-2B-4T\ggml-model-i2_s.gguf -p 'You are a helpful assistant' -n 16 -cnv | Out-String
    if ($LASTEXITCODE -eq 0 -and $output.Trim().Length -gt 0) {
        Write-Output "🏆 ALL ROUNDS CLEAR"
    } else {
        throw "❌ Inference failed"
    }
}

try {
    Round1
    Round2
    Round3
    Round4
    Round5
    Round6
} catch {
    Write-Error $_
    exit 1
} finally {
    Stop-Transcript
}
exit 0
