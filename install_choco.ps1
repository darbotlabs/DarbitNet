# Install Chocolatey if not already installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr https://community.chocolatey.org/install.ps1 -UseBasicParsing | iex"
}

# Install toolchain and helpers
choco install -y git python3 cmake llvm clang 7zip visualstudio2022buildtools

# Supply VS Build Tools with the Desktop-C++, CMake, Clang workloads
choco install -y visualstudio2022buildtools --params "'/Quiet /Add Microsoft.VisualStudio.Workload.VCTools /Add Microsoft.VisualStudio.Component.VC.CMake.Project /Add Microsoft.VisualStudio.Component.VC.Llvm.Clang /Add Microsoft.VisualStudio.Component.VC.Llvm.ClangToolset /Add Microsoft.VisualStudio.Component.VC.Llvm.ClangToolset.MSBuild'"
