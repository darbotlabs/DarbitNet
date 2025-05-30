<#
.SYNOPSIS
Installs Chocolatey and the Visual Studio build toolchain required for BitNet.

.EXAMPLE
pwsh -File .\install_choco.ps1
#>

function Install-Chocolatey {
    if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
        Set-ExecutionPolicy Bypass -Scope Process -Force
        powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr https://community.chocolatey.org/install.ps1 -UseBasicParsing | iex"
    }
}

function Install-Toolchain {
    choco install -y git python3 cmake llvm clang 7zip visualstudio2022buildtools
    choco install -y visualstudio2022buildtools --params "'/Quiet /Add Microsoft.VisualStudio.Workload.VCTools /Add Microsoft.VisualStudio.Component.VC.CMake.Project /Add Microsoft.VisualStudio.Component.VC.Llvm.Clang /Add Microsoft.VisualStudio.Component.VC.Llvm.ClangToolset /Add Microsoft.VisualStudio.Component.VC.Llvm.ClangToolset.MSBuild'"
}

Install-Chocolatey
Install-Toolchain
