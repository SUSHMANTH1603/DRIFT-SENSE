###############################################################################
# DRIFT-SENSE: Multi-stage Docker build
# Stage 1: Classical CV only (CPU)
# Stage 2: Full pipeline with DL fallback (GPU optional)
###############################################################################

# ---------- Stage 1: Base (Classical CV) ----------
FROM python:3.10-slim AS base

WORKDIR /app

# System dependencies for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx libglib2.0-0 gcc g++ make cmake \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install -e .

# Default: run inference
ENTRYPOINT ["python", "-m", "inference.infer"]

# ---------- Stage 2: Full pipeline (with ONNX Runtime GPU) ----------
FROM base AS full

RUN pip install --no-cache-dir onnxruntime-gpu>=1.16

ENTRYPOINT ["python", "-m", "inference.infer"]
