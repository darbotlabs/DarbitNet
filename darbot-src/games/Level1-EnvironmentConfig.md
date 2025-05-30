````markdown
# 🕹️ **DarbitNet “Build-Quest” – Gameified Task List for GPT-4-1 Agent**

Welcome, Agent!  
Your mission is to provision a **bare Windows 11** PC, compile **darbotlabs/DarbitNet** (BitNet fork), download the 1-bit model, and validate inference – _all through a single PowerShell script_ you’ll create in this workspace. The journey is split into **6 Rounds**; each ends with a **Validation Gate** that must pass before you advance.

---

## 📋 **Prerequisites**

Before starting the quest, ensure you have:

1. **Windows 11** with Administrator privileges
2. **PowerShell 5.1 or later** (included with Windows 11)
3. **Internet connection** for downloading tools and models
4. **Hugging Face account** (optional but recommended - for model access)
   - Sign up at [https://huggingface.co](https://huggingface.co)
   - Create access token at [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - Set environment variable: `$Env:HF_TOKEN = "your_token_here"`

---

## 🎯 **Quest Rules**

| Rule | Detail |
|------|--------|
| **Language** | _PowerShell_ only – script named **`setup-bitnet.ps1`** |
| **Scope** | End-to-end: tooling → repo → Conda → build → model → smoke test |
| **Persistence** | Clone repository and install tools in default locations. Models stored in `models/` directory. |
| **Automation** | Use silent / unattended flags where possible. |
| **Checkpoints** | After each Validation Gate, emit “✅ ROUND X PASS” or “❌ ROUND X FAIL”. |
| **Logging** | Pipe all script output to `setup-log.txt` for later inspection. |

---

## 🗺️ **Round Map**

### **Round 1 – Bootstrap Essentials**

1. **Install Chocolatey** (skip if `choco` exists).  
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr https://community.chocolatey.org/install.ps1 -UseBasicParsing | iex"
````

2. **Install toolchain & helpers:**

   ```powershell
   choco install -y git python3 cmake llvm clang ninja 7zip visualstudio2022buildtools
   ```

   *Supply VS Build Tools with the **Desktop-C++**, **CMake**, **Clang** workloads using the `/Quiet /Add` flags via Chocolatey’s package.* ([Chocolatey Software][1], [Microsoft Learn][2], [Microsoft Learn][3])

**Validation Gate 1**

```powershell
git --version; python --version; cmake --version; clang --version; ninja --version
If ($LASTEXITCODE -eq 0) { "✅ ROUND 1 PASS" } Else { "❌ ROUND 1 FAIL"; Exit 1 }
```

---

### **Round 2 – Python & Conda Arena**

1. **Silent-install Miniconda** to `C:\Miniconda3` if missing.

   ```powershell
   $minInstaller = "$env:TEMP\miniconda.exe"
   Invoke-WebRequest -Uri "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile $minInstaller
   & $minInstaller /S /InstallationType=AllUsers /AddToPath=1 /RegisterPython=0 /D=C:\Miniconda3
   ```
2. **Create & activate env**:

   ```powershell
   conda create -y -n bitnet-cpp python=3.9
   conda activate bitnet-cpp
   ```

**Validation Gate 2**

```powershell
conda info --envs | Select-String "bitnet-cpp"
python - <<<'import sys, platform, ctypes, json, os, subprocess, ssl, time;print("Py OK")'
```

If both succeed → **PASS**. ([docs.conda.io][4], [docs.conda.io][5])

---

### **Round 3 – Clone & Prep Sources**

1. **Clone the repository recursively:**

   ```powershell
   git clone --recursive https://github.com/darbotlabs/DarbitNet.git C:\DarbotNet
   cd C:\DarbotNet
   git submodule update --init --recursive
   ```
2. **Install Python dependencies in the conda environment:**

   ```powershell
   conda run -n bitnet-cpp pip install -r requirements.txt
   ```

**Validation Gate 3**

```powershell
Test-Path src\CMakeLists.txt
conda run -n bitnet-cpp python -c "import torch, sentencepiece, numpy, tqdm, packaging, huggingface_hub; print('Deps OK')"
```

Success prints **Deps OK** → gate passes. ([GitHub][6], [Hugging Face][7])

---

### **Round 4 – Build bitnet.cpp**

1. **Enter Developer PowerShell for VS 2022** automatically:

   ```powershell
   Import-Module "$Env:ProgramFiles\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Microsoft.VisualStudio.DevShell.dll"
   Enter-VsDevShell -SkipAutomaticLocation -DevCmdArguments "-arch=x64 -host_arch=x64"
   ```
2. **Configure & build** (Release x64):

   ```powershell
   mkdir build; cd build
   cmake -G "Ninja" -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ ..
   cmake --build . --config Release
   cd ..
   ```

**Validation Gate 4**

```powershell
Test-Path build\bin\bitnet_cpp.dll
```

DLL present → **PASS**; else fail. ([GitHub][8])

---

### **Round 5 – Model Fetch & Quantize**

1. **Ensure HF token is set (if required):**

   ```powershell
   # Optional: Set your Hugging Face token for model access
   # $Env:HF_TOKEN = "your_token_here"
   ```

2. **Download model using setup script:**

   ```powershell
   conda run -n bitnet-cpp python setup_env.py -hr microsoft/BitNet-b1.58-2B-4T -md models/BitNet-b1.58-2B-4T -q i2_s
   ```

**Validation Gate 5**

```powershell
Test-Path models\BitNet-b1.58-2B-4T\ggml-model-i2_s.gguf
```

File exists → **PASS**. ([Hugging Face][9], [Hugging Face][10], [Hugging Face][7])

---

### **Round 6 – Smoke-Test Inference**

1. **Run inference command:**

   ```powershell
   conda run -n bitnet-cpp python run_inference.py -m models/BitNet-b1.58-2B-4T\ggml-model-i2_s.gguf -p "You are a helpful assistant" -n 16 -cnv
   ```
2. Capture first output tokens; if script returns text within 10 s, declare success.

**Validation Gate 6**

```powershell
If ($output.Length -gt 0) { "🏆 ALL ROUNDS CLEAR" } Else { "❌ Inference failed"; Exit 1 }
```

([GitHub][6])

---

## 🛠️ **Script Skeleton to Generate**

Create **`setup-bitnet.ps1`** with the logic above (include comments + logging redirect: `Start-Transcript -Path setup-log.txt`). Ensure each Validation Gate aborts on failure.

---

## 📑 **Mission Complete Checklist**

* [ ] Generated `setup-bitnet.ps1`
* [ ] Ran script **as Administrator**
* [ ] All six **✅ PASS** banners observed
* [ ] `setup-log.txt` saved for audit

Good luck, Agent GPT-4-1 … the BitNet awaits!

```
::contentReference[oaicite:6]{index=6}
```

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

### **Option 1: Automated Setup (Recommended)**

1. **Clone the repository:**
   ```powershell
   git clone --recursive https://github.com/darbotlabs/DarbitNet.git
   cd DarbitNet
   ```

2. **Run the automated setup script** as Administrator:
   ```powershell
   .\setup-bitnet.ps1
   ```

3. **Validate the installation:**
   ```powershell
   .\validate_installation.ps1
   ```

### **Option 2: Manual Setup (Following the Game)**

Follow the 6 rounds outlined above, executing each validation gate before proceeding to ensure your environment is properly configured.

### **Common Issues & Solutions**

1. **Missing submodules**: Ensure you clone with `--recursive` flag or run `git submodule update --init --recursive`
2. **HuggingFace access**: Some models may require authentication - set `$Env:HF_TOKEN` with your access token
3. **Build failures**: Ensure Visual Studio Build Tools are properly installed with C++ workload
4. **Model download issues**: The setup_env.py script handles model download and quantization automatically
