<#
.SYNOPSIS
Validates the installed toolchain and presence of the default BitNet model.

.DESCRIPTION
Runs simple version checks for git, python, cmake, clang and ninja. It then
verifies that the expected model file exists in the repository.

.EXAMPLE
pwsh -File .\validate_installation.ps1
#>

function Test-Toolchain {
    git --version | Out-Null
    $gitStatus = $LASTEXITCODE

    python --version | Out-Null
    $pythonStatus = $LASTEXITCODE

    cmake --version | Out-Null
    $cmakeStatus = $LASTEXITCODE

    clang --version | Out-Null
    $clangStatus = $LASTEXITCODE

    ninja --version | Out-Null
    $ninjaStatus = $LASTEXITCODE

    return ($gitStatus -eq 0 -and $pythonStatus -eq 0 -and $cmakeStatus -eq 0 -and $clangStatus -eq 0 -and $ninjaStatus -eq 0)
}

function Test-Model {
    param(
        [string]$Path = "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf"
    )
    return (Test-Path $Path)
}

if (Test-Toolchain) {
    Write-Output "✅ ROUND 1 PASS"
} else {
    Write-Output "❌ ROUND 1 FAIL"
    exit 1
}

if (Test-Model) {
    Write-Output "✅ Model validation PASS"
} else {
    Write-Output "❌ Model validation FAIL"
    exit 1
}
