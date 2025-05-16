# Install Chocolatey if not already installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr https://community.chocolatey.org/install.ps1 -UseBasicParsing | iex"
}

# Install toolchain and helpers
choco install -y git python3 cmake llvm clang 7zip visualstudio2022buildtools

# Supply VS Build Tools with the Desktop-C++, CMake, Clang workloads
choco install -y visualstudio2022buildtools --params "'/Quiet /Add Microsoft.VisualStudio.Workload.VCTools /Add Microsoft.VisualStudio.Component.VC.CMake.Project /Add Microsoft.VisualStudio.Component.VC.Llvm.Clang /Add Microsoft.VisualStudio.Component.VC.Llvm.ClangToolset /Add Microsoft.VisualStudio.Component.VC.Llvm.ClangToolset.MSBuild'"

# Validate the installation of git, python, cmake, and clang

# Check git version
git --version
$gitStatus = $LASTEXITCODE

# Check python version
python --version
$pythonStatus = $LASTEXITCODE

# Check cmake version
cmake --version
$cmakeStatus = $LASTEXITCODE

# Check clang version
clang --version
$clangStatus = $LASTEXITCODE

# Validate installation
if ($gitStatus -eq 0 -and $pythonStatus -eq 0 -and $cmakeStatus -eq 0 -and $clangStatus -eq 0) {
    Write-Output "✅ ROUND 1 PASS"
} else {
    Write-Output "❌ ROUND 1 FAIL"
    Exit 1
}
