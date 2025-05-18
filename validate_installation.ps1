# Validate the installation of git, python, cmake, clang, and ninja

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

# Check ninja version
ninja --version
$ninjaStatus = $LASTEXITCODE

# Validate installation
if ($gitStatus -eq 0 -and $pythonStatus -eq 0 -and $cmakeStatus -eq 0 -and $clangStatus -eq 0 -and $ninjaStatus -eq 0) {
    Write-Output "✅ ROUND 1 PASS"
} else {
    Write-Output "❌ ROUND 1 FAIL"
    Exit 1
}

# Validate the new model microsoft/BitNet-b1.58-2B-4T-gguf
$modelPath = "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf"
if (Test-Path $modelPath) {
    Write-Output "✅ Model validation PASS"
} else {
    Write-Output "❌ Model validation FAIL"
    Exit 1
}
