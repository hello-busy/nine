# CUDA Learning: Coda Cool

Welcome to the CUDA learning module for the Ultimate Bootable Challenge repo. This directory contains a small, self-contained example and guidance so you can start learning CUDA C/C++ locally.

## Prerequisites
- A machine with an NVIDIA GPU supported by the CUDA toolkit.
- NVIDIA CUDA Toolkit installed (nvcc compiler). For Ubuntu: follow instructions on developer.nvidia.com.
- Basic familiarity with C/C++ and terminal usage.

## Quick start
1. Build the example:
   cd docs/cuda
   make

   Or use the helper script:
   ./compile.sh

2. Run the example:
   ./vector_add

## Files
- simple_vector_add.cu — minimal CUDA example: vector addition with host/device memory management and basic error checking.
- Makefile — builds the example with nvcc and provides a 'run' target.
- compile.sh — convenience wrapper that checks for nvcc, builds, and runs the example.
- EXERCISES.md — progressive exercises to deepen knowledge.

## Notes
- This is educational material only. No networking or external downloads are performed by these scripts.
- If you do not have an NVIDIA GPU, you can still study the code and follow along but you cannot run the binary.

License: MIT
