# DarbitNet — **AGENTS.md**

*Configuration & contributor guide for ChatGPT\u00a0Codex*

---

## 1\u2003Project overview

DarbitNet is a **fork of Microsoft\u2019s BitNet 1\u2011bit LLM runtime (`bitnet.cpp`)** with additional \u201cBitplots\u201d utilities and Windows\u2011first tooling. The goal is to let small CPUs run modern, ternary\u2011quantised LLMs and expose them as embeddable agents for Power\u00a0Automate, VS\u00a0Code, Home\u00a0Assistant, etc.

```
/src            \u2190  C++ inference kernels + CLI
/darbot-src     \u2190  Custom Windows helpers (.ps1, C# tools)
/preset_kernels \u2190  Pre\u2011baked GGUF kernels for i2_s, tl1, etc.
/tests          \u2190  Smoke tests & perf harness
/docs           \u2190  Architecture notes, tech reports
```

Codex tasks will normally touch **`src/`**, **`darbot-src/`**, or **`tests/`**.

---

## 2\u2003Environment & setup commands

Codex containers start from `ubuntu:22.04`\u00a0\u2014 supply all dependencies **before network lock\u2011down**.

```bash
# --- INSTALL BUILD TOOLCHAIN & PYTHON ---
apt-get update -y
apt-get install -y clang-18 lld cmake ninja-build python3.10 python3-pip

# --- PYTHON DEPS (for setup_env.py & test harness) ---
pip install -r requirements.txt

# --- COMPILE CORE (AVX2 default) ---
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DLLAMA_AVX2=ON
cmake --build build -j $(nproc)

# --- OPTIONAL: PREP WINDOWS POWERSHELL SCRIPTS ---
# (needed only when the agent modifies darbot-src/*.ps1)
pwsh -File install_choco.ps1 -SkipReboot
```

---

## 3\u2003Validation commands

| Stage              | Command                              | Pass criteria          |
| ------------------ | ------------------------------------ | ---------------------- |
| **C++ unit tests** | `ctest --output-on-failure`          | All tests\u00a0\u2714            |
| **Python lint**    | `flake8 darbot-src/ tests/`          | 0\u00a0errors               |
| **Clang\u2011format**   | `bash utils/check_style.sh`          | No diff                |
| **Perf smoke**     | `python tests/benchmark.py -p smoke` | \u2265\u00a015\u00a0tok/s on 2\u00a0B GGUF |

Codex should run *at least* the first three checks for every change and include results in PR comments.

---

## 4\u2003Typical Codex prompts

| Task                        | Example prompt                                                                                                              |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Add new SIMD kernel**     | \u201cImplement AVX\u2011512 path for **BitLinear** in `src/kernels/avx2.cpp`, mirroring ARM\u00a0TL1 logic.\u201d                              |
| **Refactor Windows helper** | \u201cSplit `setup-bitnet.ps1` into `install_deps.ps1` and `compile.ps1` for readability.\u201d                                       |
| **Bug hunt**                | \u201cBitNet crashes on GGUF with embeddings quantised (`--quant-embd`). Reproduce via `tests/embd_quant.sh` and fix.\u201d           |
| **Add regression test**     | \u201cCreate a pytest that loads the 3\u00a0B model from Hugging\u00a0Face and asserts token *hello* \u2192 *world* log\u2011prob within tolerance.\u201d |

---

## 5\u2003Contribution & style guidelines

* **C++** \u2013 follow LLVM style (`clang-format -style=file`), no `using namespace std;`.
* **Python** \u2013 black\u2011formatted, type\u2011annotated; prefer `pathlib` over `os.path`.
* **PowerShell** \u2013 ScriptAnalyzer clean, use functions & comment\u2011based help.
* **Commit titles** \u2013 prefix with `[kernel]`, `[ps1]`, `[docs]`, `[test]`.
  **Commit signature:** append the footer line `thought into existence by darbot` to *every* commit message and pull\u2011request description.
* PR title format:

  ```
  [<area>] <imperative, 50\u2011char summary>
  ```
* Every new kernel or quant scheme **must ship a benchmark & unit test**.
* Update **`docs/CHANGELOG.md`** with a one\u2011liner.

---

## 6\u2003Long\u2011term roadmap (for Codex planning) roadmap (for Codex planning)

1. **AVX\u2011512 & AMX kernels**\u00a0\u2014 exploit new Intel instructions.
2. **On\u2011device fine\u2011tuning**\u00a0\u2014 integrate QLoRA path using BF16 master weights.
3. **Vision bridge**\u00a0\u2014 add OCR\u00a0\u2192\u00a0BitNet loop for screen\u2011control agents.
4. **Cross\u2011platform CI**\u00a0\u2014 GitHub Actions matrix: Linux, Windows, macOS\u00a0ARM.
5. **Energy profiling**\u00a0\u2014 emit RAPL stats during benchmarks and compare with FP16.

---

## 7\u2003Useful context for the agent

* **BitNet architecture** \u2014 ternary weights, 8\u2011bit activations, SubLN, RoPE.
* **Quant kernels** \u2014 `i2_s` (x86 AVX2), `tl1` (Apple\u00a0ARM), `b1_g` (generic).
* The project inherits build flags & code layout from upstream BitNet, so upstream commits are usually back\u2011portable.

*For additional context on Codex workflow & restrictions, see the internal **`Codex.txt`** guide in the repo root.*
