# GitHub Copilot Instructions for DarbitNet

## Project Overview

DarbitNet is a **fork of Microsoft's BitNet 1-bit LLM runtime (`bitnet.cpp`)** with additional "Bitplots" utilities and Windows-first tooling. The goal is to empower every person and organization to use their existing CPUs and devices to run modern, ternary-quantized LLMs and expose them as embeddable agents for Copilot, Windows, PowerShell, PowerFX, Power Automate, VS Code, Home Assistant, etc.

### Repository Structure
```
/src            ← C++ inference kernels + CLI
/darbot-src     ← Custom Windows helpers (.ps1, C# tools)
/preset_kernels ← Pre-baked GGUF kernels for i2_s, tl1, etc.
/tests          ← Smoke tests & performance harness
/docs           ← Architecture notes, tech reports
```

## Development Environment

### Dependencies
- **Build Tools**: CMake, Ninja, Clang-18, LLD
- **Python**: 3.9+ with pytest, flake8, bandit, safety
- **Optional**: PowerShell (for Windows scripts)

### Setup Commands
```bash
# Install build toolchain & Python
apt-get update -y
apt-get install -y clang-18 lld cmake ninja-build python3.10 python3-pip

# Install Python dependencies
pip install -r requirements.txt

# Compile core (AVX2 default)
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DLLAMA_AVX2=ON
cmake --build build -j $(nproc)
```

## Code Standards & Guidelines

### C++
- Follow LLVM style (`clang-format -style=file`)
- No `using namespace std;`
- Every new kernel or quantization scheme **must** include benchmark & unit test

### Python
- Black-formatted, type-annotated
- Prefer `pathlib` over `os.path`
- Use pytest for testing

### PowerShell
- ScriptAnalyzer clean
- Use functions & comment-based help

### Commit Guidelines
- **Commit titles**: Prefix with `[kernel]`, `[ps1]`, `[docs]`, `[test]`
- **Commit signature**: Append `thought into existence by darbot` to every commit message
- **PR title format**: `[<area>] <imperative, 50-char summary>`

## Validation Requirements

Before submitting changes, run these validation steps:

| Stage | Command | Pass Criteria |
|-------|---------|---------------|
| **C++ unit tests** | `ctest --output-on-failure` | All tests ✔ |
| **Python lint** | `flake8 darbot-src/ tests/` | 0 errors |
| **Python tests** | `python -m pytest tests/ -v` | All tests pass |
| **Security scan** | `bandit -r . -f json` | No critical issues |

Run *at least* the first three checks for every change.

## Common Development Tasks

### Adding New SIMD Kernel
- Implement in appropriate architecture file (`src/kernels/`)
- Mirror existing logic patterns (e.g., ARM TL1 for AVX-512)
- Add corresponding benchmark and unit test
- Update `docs/CHANGELOG.md`

### Refactoring Windows Helpers
- Split complex scripts for readability
- Maintain ScriptAnalyzer compliance
- Ensure backwards compatibility

### Bug Fixes
- Reproduce issue with minimal test case
- Add regression test to prevent recurrence
- Document fix in changelog

### Performance Optimization
- Benchmark before and after changes
- Target ≥ 15 tok/s on 2B GGUF models
- Profile with appropriate tools for the platform

## Architecture Context

### BitNet Architecture
- **Weights**: Ternary quantization
- **Activations**: 8-bit
- **Components**: SubLN, RoPE
- **Kernels**: `i2_s` (x86 AVX2), `tl1` (Apple ARM), `b1_g` (generic)

### Integration Points
- Copilot integration for VS Code
- Windows PowerShell automation
- Home Assistant agents
- Power Platform connectors

## Testing Strategy

### Unit Tests
- Located in `/tests/`
- Use pytest framework
- Mock external dependencies
- Cover edge cases and error conditions

### Integration Tests
- End-to-end benchmark validation
- Cross-platform compatibility
- Performance regression detection

### Security Testing
- Bandit for Python security issues
- Safety for dependency vulnerabilities
- Manual security review for C++ changes

## Best Practices for AI Assistance

When working with this codebase:

1. **Understand context**: Review existing patterns before suggesting changes
2. **Maintain compatibility**: Changes should be backward-compatible unless explicitly breaking
3. **Follow conventions**: Use established naming and coding patterns
4. **Test thoroughly**: Include appropriate tests for all changes
5. **Document changes**: Update relevant documentation and changelog
6. **Security first**: Consider security implications of all changes

## Long-term Roadmap

1. **AVX-512 & AMX kernels** — Exploit new Intel instructions
2. **On-device fine-tuning** — Integrate QLoRA path using BF16 master weights
3. **Vision bridge** — Add OCR → BitNet loop for screen-control agents
4. **Cross-platform CI** — GitHub Actions matrix: Linux, Windows, macOS ARM
5. **Energy profiling** — Emit RAPL stats during benchmarks

---

For additional context and detailed agent configuration, see `AGENTS.md` in the repository root.