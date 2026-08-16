# Architecture

## System Overview

DRIFT-SENSE uses a **Conditional Hybrid Classical-First with Learned Verification Fallback** architecture.

```
INPUT: reference.png (1µm FOV) + search.png (10µm FOV)
                    │
                    ▼
        ┌──────────────────────┐
        │  SEM Preprocessing   │  CLAHE + Unsharp + Normalize
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Coarse Phase Corr   │  256×256 pyramid → top-20 candidates
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  DT-NCC Refinement   │  512×512 → top-5 candidates
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Periodicity Analysis│  FFT pitch + alias clustering
        └──────────┬───────────┘
                   │
            ┌──────┴──────┐
            ▼             ▼
    ┌─────────────┐ ┌─────────────┐
    │ High Conf   │ │ Ambiguous   │
    │ Classical   │ │ DL Fallback │
    └──────┬──────┘ └──────┬──────┘
           │               │
           └───────┬───────┘
                   ▼
        ┌──────────────────────┐
        │  Validation + Output │  Reprojection + Confidence
        └──────────────────────┘
```

## Module Dependencies

```
generator/     → (standalone, no internal deps)
classical/     → (standalone, uses OpenCV/NumPy/SciPy)
models/        → (depends on PyTorch)
training/      → generator/ + models/
evaluation/    → classical/ + models/
inference/     → classical/ + models/ (ONNX Runtime)
cpp/           → (standalone C++ implementation)
```

## Key Design Decisions

1. **Classical-First**: DL is fallback only, not primary — determinism and explainability for fab deployment.
2. **DT-NCC over raw NCC**: Distance transform provides robustness to SEM intensity variations.
3. **Periodicity as explicit constraint**: Structural pitch from FFT, not learned — physics-informed.
4. **Independent noise**: Reference and search get separate noise realizations (physically mandatory).
5. **Center prior with guard**: Prevents bias when visual evidence is strong (margin > 15%).
