#!/usr/bin/env bash
set -euo pipefail

# Build script: assemble boot.asm into boot.bin and write into floppy.img
# Integrated with obfuscator: if SEED env var is set (non-empty), obfuscate boot.asm before assembling.

if ! command -v nasm >/dev/null 2>&1; then
  echo "Error: nasm not found. Install nasm to continue." >&2
  exit 1
fi

BOOT_SRC="boot.asm"
BOOT_BIN="boot.bin"
FLOPPY_IMG="floppy.img"

# Optional obfuscation
if [ -n "${SEED-}" ]; then
  if command -v python3 >/dev/null 2>&1 && [ -f "scripts/obfuscate.py" ]; then
    echo "[build] Running obfuscator with seed=${SEED}"
    python3 scripts/obfuscate.py --seed "${SEED}" "${BOOT_SRC}"
  else
    echo "[build] Obfuscator not available or python3 missing; skipping obfuscation"
  fi
fi

if [ ! -f "${BOOT_SRC}" ]; then
  echo "Error: ${BOOT_SRC} not found. Nothing to build." >&2
  exit 1
fi

echo "[build] Assembling ${BOOT_SRC} -> ${BOOT_BIN}"
nasm -f bin "${BOOT_SRC}" -o "${BOOT_BIN}"

echo "[build] Creating ${FLOPPY_IMG} (1.44MB) and writing boot sector"
# Create empty 1.44MB floppy
if command -v dd >/dev/null 2>&1; then
  dd if=/dev/zero of="${FLOPPY_IMG}" bs=512 count=2880 status=none
  # Write boot.bin into first sector(s)
  dd if="${BOOT_BIN}" of="${FLOPPY_IMG}" conv=notrunc status=none
else
  echo "Error: dd not found. Cannot create floppy image." >&2
  exit 1
fi

echo "[build] Build complete: ${FLOPPY_IMG}"