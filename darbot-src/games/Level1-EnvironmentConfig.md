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
   choco install -y git python3 cmake llvm clang 7zip visualstudio2022buildtools
   ```

   *Supply VS Build Tools with the **Desktop-C++**, **CMake**, **Clang** workloads using the `/Quiet /Add` flags via Chocolatey’s package.* ([Chocolatey Software][1], [Microsoft Learn][2], [Microsoft Learn][3])

**Validation Gate 1**

```powershell
git --version; python --version; cmake --version; clang --version
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

1. ```powershell
   git clone --recursive https://github.com/darbotlabs/DarbitNet.git C:\DarbotNet
   cd C:\DarbotNet
   ```
2. ```powershell
   pip install -r requirements.txt
   ```

**Validation Gate 3**

```powershell
Test-Path C:\DarbotNet\src\CMakeLists.txt
python -c "import torch, sentencepiece, numpy, tqdm, packaging, huggingface_hub; print('Deps OK')"
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
   cmake -G "Ninja" -DCMAKE_BUILD_TYPE=Release ..
   cmake --build . --config Release
   ```

**Validation Gate 4**

```powershell
Test-Path .\bin\bitnet_cpp.dll
```

DLL present → **PASS**; else fail. ([GitHub][8])

---

### **Round 5 – Model Fetch & Quantize**

1. **Log-in to Hugging Face (if token provided)**.

   ```powershell
   huggingface-cli login --token $Env:HF_TOKEN
   ```
2. **Download model locally:**

   ```powershell
   huggingface-cli download microsoft/bitnet-b1.58-2B-4T-gguf --local-dir C:\DarbotNet\models\BitNet-b1.58-2B-4T
   ```
3. **Prepare environment & quantization (i2\_s):**

   ```powershell
   python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s
   ```

**Validation Gate 5**

```powershell
Test-Path C:\DarbotNet\models\BitNet-b1.58-2B-4T\ggml-model-i2_s.gguf
```

File exists → **PASS**. ([Hugging Face][9], [Hugging Face][10], [Hugging Face][7])

---

### **Round 6 – Smoke-Test Inference**

1. ```powershell
   python run_inference.py -m models/BitNet-b1.58-2B-4T\ggml-model-i2_s.gguf -p "You are a helpful assistant" -n 16 -cnv
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

1. **Run the `setup-bitnet.ps1` script** to install Chocolatey and the required toolchain and helpers:
   ```powershell
   .\setup-bitnet.ps1
   ```

2. **Validate the installation** by running the `validate_installation.ps1` script:
   ```powershell
   .\validate_installation.ps1
   ```

3. **Dependency Validation**:
   - Verify that all required dependencies are installed and their versions are correct.
   - Check for the presence of specific files or directories that indicate successful installation of dependencies.
   - Validate the integrity of downloaded files by comparing checksums.
