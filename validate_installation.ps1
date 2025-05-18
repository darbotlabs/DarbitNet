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
