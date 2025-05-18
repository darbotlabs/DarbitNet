# DarbitNet — **AGENTS.md**

*Configuration & contributor guide for ChatGPT Codex*

---

## 1 Project overview

DarbitNet is a **fork of Microsoft’s BitNet 1‑bit LLM runtime (`bitnet.cpp`)** with additional “Bitplots” utilities and Windows‑first tooling. The goal is to let small CPUs run modern, ternary‑quantised LLMs and expose them as embeddable agents for Power Automate, VS Code, Home Assistant, etc.

```
/src            ←  C++ inference kernels + CLI
/darbot-src     ←  Custom Windows helpers (.ps1, C# tools)
/preset_kernels ←  Pre‑baked GGUF kernels for i2_s, tl1, etc.
/tests          ←  Smoke tests & perf harness
/docs           ←  Architecture notes, tech reports
```

Codex tasks will normally touch **`src/`**, **`darbot-src/`**, or **`tests/`**.

---

## 2 Environment & setup commands

Codex containers start from `ubuntu:22.04`— supply all dependencies **before network lock‑down**.

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

## 3 Validation commands

| Stage              | Command                              | Pass criteria          |
| ------------------ | ------------------------------------ | ---------------------- |
| **C++ unit tests** | `ctest --output-on-failure`          | All tests ✔            |
| **Python lint**    | `flake8 darbot-src/ tests/`          | 0 errors               |
| **Clang‑format**   | `bash utils/check_style.sh`          | No diff                |
| **Perf smoke**     | `python tests/benchmark.py -p smoke` | ≥ 15 tok/s on 2 B GGUF |

Codex should run *at least* the first three checks for every change and include results in PR comments.

---

## 4 Typical Codex prompts

| Task                        | Example prompt                                                                                                              |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Add new SIMD kernel**     | “Implement AVX‑512 path for **BitLinear** in `src/kernels/avx2.cpp`, mirroring ARM TL1 logic.”                              |
| **Refactor Windows helper** | “Split `setup-bitnet.ps1` into `install_deps.ps1` and `compile.ps1` for readability.”                                       |
| **Bug hunt**                | “BitNet crashes on GGUF with embeddings quantised (`--quant-embd`). Reproduce via `tests/embd_quant.sh` and fix.”           |
| **Add regression test**     | “Create a pytest that loads the 3 B model from Hugging Face and asserts token *hello* → *world* log‑prob within tolerance.” |

---

## 5 Contribution & style guidelines

* **C++** – follow LLVM style (`clang-format -style=file`), no `using namespace std;`.
* **Python** – black‑formatted, type‑annotated; prefer `pathlib` over `os.path`.
* **PowerShell** – ScriptAnalyzer clean, use functions & comment‑based help.
* **Commit titles** – prefix with `[kernel]`, `[ps1]`, `[docs]`, `[test]`.
  **Commit signature:** append the footer line `thought into existence by darbot` to *every* commit message and pull‑request description.
* PR title format:

  ```
  [<area>] <imperative, 50‑char summary>
  ```
* Every new kernel or quant scheme **must ship a benchmark & unit test**.
* Update **`docs/CHANGELOG.md`** with a one‑liner.

---

## 6 Long‑term roadmap (for Codex planning) roadmap (for Codex planning)

1. **AVX‑512 & AMX kernels** — exploit new Intel instructions.
2. **On‑device fine‑tuning** — integrate QLoRA path using BF16 master weights.
3. **Vision bridge** — add OCR → BitNet loop for screen‑control agents.
4. **Cross‑platform CI** — GitHub Actions matrix: Linux, Windows, macOS ARM.
5. **Energy profiling** — emit RAPL stats during benchmarks and compare with FP16.

---

## 7 Useful context for the agent

* **BitNet architecture** — ternary weights, 8‑bit activations, SubLN, RoPE.
* **Quant kernels** — `i2_s` (x86 AVX2), `tl1` (Apple ARM), `b1_g` (generic).
* The project inherits build flags & code layout from upstream BitNet, so upstream commits are usually back‑portable.

*For additional context on Codex workflow & restrictions, see the internal **`Codex.txt`** guide in the repo root.*

<!-- End of previous sections -->


<!-- ──────────────────────────────────────────────────────────────── ─-->
## 5  Reasoning & Self-Validation Framework  
*thought into existence by darbot*  
<!-- ──────────────────────────────────────────────────────────────── -->

### 5.1 Purpose
> Provide deterministic, inspectable guard-rails so every DarbotNet agent can  
> 1. expose its chain-of-thought (“scratchpad”) in a machine-parsable form,  
> 2. score its own output against objective rubrics,  
> 3. iterate up to **N loops (default = 20)** until quality thresholds are met.

### 5.2 Self-Validation Loop (High-Level Algorithm)

| Step | Action | Implementation Hint |
|------|--------|---------------------|
| 1    |**Draft** initial answer / artifact. | Use the Scratchpad template in §5.4 while thinking. |
| 2    |**Run Linters / Unit Tests.** | `npm test`, `pytest`, `pester`, etc. |
| 3    |**Score** draft using _Validation Rubric_ (§5.3). | Create `.validation/score.json`. |
| 4    |**Decision Gate.** If all metrics ≥ target, **commit**<sup>†</sup>; else continue. | Targets configurable via `AGENT_QA_TARGETS` env var. |
| 5    |**Reflect.** Write a short *“Why-did-I-miss”* note to `scratchpad.reflect`. |
| 6    |**Revise** output, prioritizing highest-impact failures. | Avoid repeating unchanged text. |
| 7    |Back to Step 2 (max **N loops**). | |
| 8    |On final pass, **emit `scratchpad.final`** and **push** commit. | Commit message prefix: `thought into existence by darbot:` |
| 9    |If max loops exhausted without passing, raise `ValidationError` event. | |
| 10   |Super-agent (or human) triages unresolved failures. | |

<sup>†</sup>All pushes/pulls **must** include the phrase **“thought into existence by darbot”** to satisfy repo policy.

### 5.3 Validation Rubric (default weights)

| Metric | Weight | Success Threshold |
|--------|--------|-------------------|
| Technical Accuracy | 0.35 | **≥ 9 / 10** |
| Unique Insight     | 0.20 | **≥ 8 / 10** |
| Internal Consistency | 0.15 | **No contradictions** |
| No Redundancy      | 0.10 | **< 5 % duplicate lines** |
| Code Health        | 0.10 | **0 linter errors** |
| Style Conformance  | 0.10 | **≥ 90 % style-guide pass** |

*Total score ≥ 90 % passes the gate.*

### 5.4 Scratchpad Thought Output Specification

| Field | Description |
|-------|-------------|
| `meta.agent_id` | Short agent name (e.g. `doc-auditor-v2`). |
| `meta.iteration` | Current loop count (1–N). |
| `thoughts.raw` | Stream-of-consciousness in **plain text**, 1-2 sentences per line. |
| `thoughts.plan` | Bullet list of next atomic actions. |
| `validation.score` | Object mirroring rubric keys + numeric scores. |
| `validation.pass` | `true` / `false`. |
| `reflection` | If `validation.pass == false`, short cause analysis. |

> **⚠ Do NOT** include secrets, PII, or proprietary client data in the scratchpad. It is committed under `.git/info/scratchpads/`.

##### Example (`scratchpad.iter1.json`)
```jsonc
{
  "meta": { "agent_id": "doc-auditor-v2", "iteration": 1 },
  "thoughts": {
    "raw": [
      "Need to confirm file paths for unit tests.",
      "Rubric weightings look correct but thresholds may be high."
    ],
    "plan": [
      "Run npm test",
      "Capture linter output",
      "Compute rubric scores"
    ]
  },
  "validation": {
    "score": {
      "technical_accuracy": 7,
      "unique_insight": 6,
      "internal_consistency": 10,
      "no_redundancy": 9,
      "code_health": 6,
      "style_conformance": 8
    },
    "pass": false
  },
  "reflection": "Accuracy low: overlooked edge-case in module loader."
}
```

### 5.5 Agent Hooks & Env Vars

| Hook              | When Fired         | Payload                |
| ----------------- | ------------------ | ---------------------- |
| `pre-validate`    | Just before Step 2 | Path to draft artifact |
| `post-validate`   | After Step 3       | `score.json`           |
| `validation-fail` | After max loops    | Full scratchpad bundle |

| Env Var                | Purpose                    | Default |
| ---------------------- | -------------------------- | ------- |
| `MAX_VALIDATION_LOOPS` | Max self-iterations        | `20`    |
| `AGENT_QA_TARGETS`     | Override rubric thresholds | *unset* |

### 5.6 Audit & Transparency

* All `scratchpad.*` files are stored in `./.git/info/scratchpads/` (excluded from distribution builds but visible to auditors).
* CI step `ci/verify-scratchpad.sh` ensures every commit tagged **“thought into existence by darbot”** also contains a passing `scratchpad.final`.
* A GitHub Action uploads the final score to the repo dashboard badge (`README.md`).

<!-- End of Section 5 -->

---

### How to integrate

1. **Add** this entire block under the “Agents & Personas” section (or keep as standalone §5).  
2. **Reference** the Validation hooks from any agent descriptor table so Codex knows they exist.  
3. **Ensure** your repo’s CI includes the simple shell/Powershell verifier mentioned in 5.6.  
4. **Profit 😉—every DarbotNet agent now self-critiques before polluting `main`.

---

## Self-analysis

*Quality-improvement score (1-10): **9**  
*Focus next time:* tighten “How to integrate” into even more actionable bullet sequence (include exact file paths).

