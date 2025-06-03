````markdown
# 🕹️ **DarbitNet “Build-Quest” – Gameified Task List for GPT-4-1 Agent**

Welcome, Agent!  
Your mission is to provision a **bare Windows 11** PC, compile **darbotlabs/DarbitNet** (BitNet fork), download the 1-bit model, and validate inference – _all through a single PowerShell script_ you’ll create in this workspace. The journey is split into **6 Rounds**; each ends with a **Validation Gate** that must pass before you advance.

---

## 🎯 **Quest Rules**

| Rule | Detail |
|------|--------|
| **Language** | _PowerShell_ only – script named **`setup-bitnet.ps1`** |
| **Scope** | End-to-end: tooling → repo → Conda → build → model → smoke test |
| **Persistence** | Everything installs under `C:\DarbotNet` (create if absent). |
| **Automation** | Use silent / unattended flags where possible. |
| **Checkpoints** | After each Validation Gate, emit “✅ ROUND X PASS” or “❌ ROUND X FAIL”. |
| **Logging** | Pipe all script output to `setup-log.txt` for later inspection. |

## 📋 **Prerequisites**

⚠️ **IMPORTANT**: These instructions require **Administrator privileges** to install system tools and configure the environment.

| Requirement | Details |
|-------------|---------|
| **OS** | Windows 11 (bare minimum install) |
| **PowerShell** | Version 5.1+ (included with Windows 11) |
| **Execution Policy** | Must allow script execution (handled automatically) |
| **Administrator** | **REQUIRED** - Run PowerShell as Administrator |
| **Internet Access** | Required for downloading tools, repos, and models |
| **Disk Space** | ~10GB free space recommended (tools + models) |
| **Memory** | 8GB+ RAM recommended for model inference |

---

## 🗺️ **Round Map**

### **Round 1 – Bootstrap Essentials**

1. **Install Chocolatey** (skip if `choco` exists).  
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr https://community.chocolatey.org/install.ps1 -UseBasicParsing | iex"
   ```

2. **Install toolchain & helpers:**

   ```powershell
   choco install -y git python3 cmake llvm clang ninja 7zip visualstudio2022buildtools
   ```

   *Supply VS Build Tools with the **Desktop-C++**, **CMake**, **Clang** workloads using the `/Quiet /Add` flags via Chocolatey’s package.* ([Chocolatey Software][1], [Microsoft Learn][2], [Microsoft Learn][3])
3. **Install Visual Studio Build Tools with required components:**

   ```powershell
   choco install -y visualstudio2022buildtools --params "'/Quiet /Add Microsoft.VisualStudio.Workload.VCTools /Add Microsoft.VisualStudio.Component.VC.CMake.Project /Add Microsoft.VisualStudio.Component.VC.Llvm.Clang /Add Microsoft.VisualStudio.Component.VC.Llvm.ClangToolset /Add Microsoft.VisualStudio.Component.VC.Llvm.ClangToolset.MSBuild'"
   ```

**Validation Gate 1**

```powershell
git --version; python --version; cmake --version; clang --version; ninja --version
If ($LASTEXITCODE -eq 0) { "✅ ROUND 1 PASS" } Else { "❌ ROUND 1 FAIL"; Exit 1 }
```

💡 **Expected Output**: Each command should display version information. All tools must be accessible from PATH.

---

### **Round 2 – Python & Conda Arena**

1. **Silent-install Miniconda** to `C:\Miniconda3` if missing.

   ```powershell
   $minInstaller = "$env:TEMP\miniconda.exe"
   Invoke-WebRequest -Uri "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile $minInstaller
   & $minInstaller /S /InstallationType=AllUsers /AddToPath=1 /RegisterPython=0 /D=C:\Miniconda3
   ```
2. **Create & activate env** and update PATH:

   ```powershell
   $env:PATH += ';C:\Miniconda3;C:\Miniconda3\Scripts'
   conda create -y -n bitnet-cpp python=3.9
   ```

   📝 **Note**: The environment activation will be handled via `conda run -n bitnet-cpp` in subsequent steps for better script automation.

**Validation Gate 2**

```powershell
conda info --envs | Select-String "bitnet-cpp"
conda run -n bitnet-cpp python -c "print('Py OK')"
```

💡 **Expected Output**: First command shows "bitnet-cpp" environment listed, second command prints "Py OK".
If both succeed → **PASS**. ([docs.conda.io][4], [docs.conda.io][5])

---

### **Round 3 – Clone & Prep Sources**

1. **Clone repository** (or use existing if running from repository directory):
   ```powershell
   # If running from outside repository:
   git clone --recursive https://github.com/darbotlabs/DarbitNet.git C:\DarbotNet
   cd C:\DarbotNet
   
   # If already in repository directory:
   git submodule update --init --recursive
   ```

2. **Install Python dependencies** using conda environment:
   ```powershell
   conda run -n bitnet-cpp pip install -r requirements.txt
   ```

**Validation Gate 3**

```powershell
Test-Path ".\src\CMakeLists.txt"
conda run -n bitnet-cpp python -c "import torch, sentencepiece, numpy, tqdm, packaging, huggingface_hub; print('Deps OK')"
```

💡 **Expected Output**: First command returns `True`, second command prints **Deps OK** → gate passes. ([GitHub][6], [Hugging Face][7])

---

### **Round 4 – Build bitnet.cpp**

1. **Enter Developer PowerShell for VS 2022** automatically:

   ```powershell
   Import-Module "$Env:ProgramFiles\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Microsoft.VisualStudio.DevShell.dll"
   Enter-VsDevShell -SkipAutomaticLocation -DevCmdArguments "-arch=x64 -host_arch=x64"
   ```

2. **Configure & build** (Release x64):

   ```powershell
   if (!(Test-Path build)) { New-Item -Type Directory -Path build | Out-Null }
   cd build
   cmake -G "Ninja" -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ ..
   cmake --build . --config Release
   cd ..
   ```

**Validation Gate 4**

```powershell
# Check for build artifacts (DLL/EXE may vary by configuration)
$buildSuccess = (Test-Path ".\build\bin\llama-cli.exe") -or (Test-Path ".\build\bin\Release\llama-cli.exe") -or (Test-Path ".\build\bin\bitnet_cpp.dll")
if ($buildSuccess) { "✅ ROUND 4 PASS" } else { "❌ ROUND 4 FAIL" }
```

💡 **Expected Output**: Build artifacts present → **PASS**; else fail. ([GitHub][8])

---

### **Round 5 – Model Fetch & Quantize**

1. **Log-in to Hugging Face** (optional, if token provided):

   ```powershell
   if ($Env:HF_TOKEN) { huggingface-cli login --token $Env:HF_TOKEN }
   ```

2. **Download model locally** using relative paths:

   ```powershell
   huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir .\models\BitNet-b1.58-2B-4T
   ```

3. **Prepare environment & quantization** (i2_s format):

   ```powershell
   conda run -n bitnet-cpp python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s
   ```

   📝 **Note**: The `-q i2_s` parameter specifies the quantization format. Available options depend on platform (see `setup_env.py` for supported types).

**Validation Gate 5**

```powershell
Test-Path ".\models\BitNet-b1.58-2B-4T\ggml-model-i2_s.gguf"
```

💡 **Expected Output**: File exists → **PASS**. ([Hugging Face][9], [Hugging Face][10], [Hugging Face][7])

---

### **Round 6 – Smoke-Test Inference**

1. **Run inference test** with the quantized model:
   ```powershell
   $output = conda run -n bitnet-cpp python run_inference.py -m models/BitNet-b1.58-2B-4T\ggml-model-i2_s.gguf -p "You are a helpful assistant" -n 16 -cnv | Out-String
   ```

2. **Validate output**: If script returns text within reasonable time, declare success.

**Validation Gate 6**

```powershell
if ($LASTEXITCODE -eq 0 -and $output.Trim().Length -gt 0) { 
    "🏆 ALL ROUNDS CLEAR" 
} else { 
    "❌ Inference failed"; Exit 1 
}
```

💡 **Expected Output**: Non-empty text response from the model within 30 seconds → **ALL ROUNDS CLEAR**. ([GitHub][6])

---

## 🛠️ **Troubleshooting Common Issues**

| Issue | Solution |
|-------|----------|
| **"choco not found"** | Restart PowerShell after Chocolatey installation, or add `C:\ProgramData\chocolatey\bin` to PATH |
| **VS Build Tools errors** | Ensure you run as Administrator; installation may take 10+ minutes |
| **Conda activation fails** | Use `conda run -n bitnet-cpp` instead of `conda activate` for script automation |
| **Git submodule errors** | Run `git submodule update --init --recursive` manually |
| **CMake configuration fails** | Ensure VS Build Tools with C++ workload is properly installed |
| **Build fails with clang errors** | Verify clang is in PATH: `clang --version` |
| **Model download fails** | Check internet connection; some models require HuggingFace authentication |
| **Inference hangs** | Model may be too large for available RAM; try smaller model or increase memory |
| **Path errors** | Use backslashes `\` for Windows paths in PowerShell |

### **Debug Commands**

```powershell
# Check installation status
choco list --local-only
conda info --envs
git submodule status
```

---

## 🛠️ **Script Implementation**

The repository includes a complete **`setup-bitnet.ps1`** script that implements all the rounds above. Key features:

- **Automated installation** of all required tools and dependencies
- **Logging** with `Start-Transcript -Path setup-log.txt`
- **Error handling** with validation gates that abort on failure
- **Administrator detection** with automatic privilege checking
- **Conda environment management** using `conda run -n bitnet-cpp`

Additionally, **`validate_installation.ps1`** provides post-installation verification.

---

## 📑 **Mission Complete Checklist**

**For Manual Implementation:**
* [ ] Follow each round step-by-step in Administrator PowerShell
* [ ] Verify each validation gate passes before proceeding  
* [ ] Address any errors using the troubleshooting guide
* [ ] Confirm final inference test produces text output

**For Automated Implementation:**  
* [ ] Run `.\setup-bitnet.ps1` **as Administrator**
* [ ] Monitor console for six **✅ PASS** banners
* [ ] Review `setup-log.txt` for any warnings or errors
* [ ] Run `.\validate_installation.ps1` for final verification
* [ ] Test inference manually if needed: `conda run -n bitnet-cpp python run_inference.py -m models/BitNet-b1.58-2B-4T\ggml-model-i2_s.gguf -p "Hello" -n 10`

Good luck, Agent GPT-4-1 … the BitNet awaits!

[1]: https://community.chocolatey.org/packages/visualstudio2022buildtools?utm_source=chatgpt.com "Visual Studio 2022 Build Tools 117.13.6 - Chocolatey Community"
[2]: https://learn.microsoft.com/en-us/visualstudio/install/workload-component-id-vs-build-tools?view=vs-2022&utm_source=chatgpt.com "Visual Studio Build Tools workload and component IDs"
[3]: https://learn.microsoft.com/en-us/visualstudio/install/use-command-line-parameters-to-install-visual-studio?view=vs-2022&utm_source=chatgpt.com "Use command-line parameters to install Visual Studio"
[4]: https://docs.conda.io/projects/conda/en/stable/user-guide/install/windows.html?utm_source=chatgpt.com "Installing on Windows — conda 25.3.1 documentation"
[5]: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html?utm_source=chatgpt.com "Installing conda — conda 25.3.2.dev60 documentation"
[6]: https://github.com/microsoft/BitNet?utm_source=chatgpt.com "microsoft/BitNet: Official inference framework for 1-bit LLMs - GitHub"
[7]: https://huggingface.co/docs/huggingface_hub/main/en/guides/cli?utm_source=chatgpt.com "Command Line Interface (CLI) - Hugging Face"
[8]: https://github.com/microsoft/BitNet/issues/100?utm_source=chatgpt.com "Can't build on Windows 11 · Issue #100 · microsoft/BitNet - GitHub"
[9]: https://huggingface.co/microsoft/bitnet-b1.58-2B-4T-gguf?utm_source=chatgpt.com "microsoft/bitnet-b1.58-2B-4T-gguf - Hugging Face"
[10]: https://huggingface.co/QuantFactory/bitnet_b1_58-3B-GGUF?utm_source=chatgpt.com "QuantFactory/bitnet_b1_58-3B-GGUF - Hugging Face"

---

## 🛠️ **Setup Instructions**

### **Quick Start (Automated)**

1. **Open PowerShell as Administrator** (Required for system tool installation):
   ```powershell
   # Right-click PowerShell → "Run as Administrator"
   ```

2. **Run the setup script** to install all components automatically:
   ```powershell
   .\setup-bitnet.ps1
   ```

3. **Validate the installation** using the verification script:
   ```powershell
   .\validate_installation.ps1
   ```

### **Manual Step-by-Step (Learning Mode)**

Follow the **6 Rounds** above manually for educational purposes or troubleshooting.

### **Verification Steps**

After completion, verify your setup:

- **Tools installed**: `choco list --local-only` shows git, python, cmake, clang, ninja, VS Build Tools
- **Conda environment**: `conda info --envs` shows `bitnet-cpp` environment  
- **Repository cloned**: Current directory contains `src/`, `CMakeLists.txt`, `setup_env.py`
- **Build successful**: `build/bin/` contains compiled binaries
- **Model ready**: `models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf` exists
- **Inference working**: Test command produces text output

### **Next Steps**

Once setup is complete, you can:

- **Run inference**: `conda run -n bitnet-cpp python run_inference.py -m models/BitNet-b1.58-2B-4T\ggml-model-i2_s.gguf -p "Your prompt here"`
- **Explore other models**: Check `setup_env.py` for supported model list
- **Develop**: Use the configured build environment for development
