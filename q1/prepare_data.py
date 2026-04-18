#!/usr/bin/env python3
"""Prepare burning-liquid images for HW9 (Martinka et al., supplementary images).

1) Builds assignment-style ``data/{ethanol,pentane,propanol}/`` (symlinks into
   ``S1_Raw_Photographs_Full_Study/``) for a flat ``torchvision.datasets.ImageFolder`` root.

2) Builds ``prepared_data/{train,val,test}/<class>/`` with a 70/15/15 stratified split
   per class (seed 42), for training without leakage.

Run from ``HW9/`` or ``HW9/q1/`` (script may live under ``q1/``; datasets are written next to ``S1_Raw_Photographs_Full_Study/``).
"""
from __future__ import annotations

import random
import shutil
from pathlib import Path

# Project root: parent of q1/, or directory containing this file if not under q1
_THIS = Path(__file__).resolve().parent
HW9_HOME = _THIS.parent if _THIS.name == "q1" else _THIS

RAW_DIR = HW9_HOME / "S1_Raw_Photographs_Full_Study"
# PDF layout: data/ethanol, data/pentane, data/propanol (all images, ImageFolder-ready)
DATA_ROOT = HW9_HOME / "data"
OUT_ROOT = HW9_HOME / "prepared_data"

CLASS_SPECS = [
    ("Ethanol", "ethanol"),
    ("Pentane", "pentane"),
    ("Propanol", "propanol"),
]

TRAIN_FRAC, VAL_FRAC = 0.70, 0.15


def main() -> None:
    if not RAW_DIR.is_dir():
        raise SystemExit(f"Missing raw image directory: {RAW_DIR}")

    rng = random.Random(42)

    # 1) Flat class folders per assignment (Supplementary File #2 → organized by filename)
    if DATA_ROOT.exists():
        shutil.rmtree(DATA_ROOT)
    for prefix, folder in CLASS_SPECS:
        dest_dir = DATA_ROOT / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        for src in sorted(RAW_DIR.glob(f"{prefix}_*")):
            if src.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue
            link = dest_dir / src.name
            try:
                link.symlink_to(src.resolve())
            except OSError:
                shutil.copy2(src, link)

    # 2) Stratified train / val / test splits (documented ratio for N≈3000)
    if OUT_ROOT.exists():
        shutil.rmtree(OUT_ROOT)

    for prefix, folder in CLASS_SPECS:
        paths = sorted(
            p
            for p in RAW_DIR.glob(f"{prefix}_*")
            if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
        )
        if not paths:
            raise SystemExit(f"No images found for prefix {prefix!r} under {RAW_DIR}")
        paths = list(paths)
        rng.shuffle(paths)
        n = len(paths)
        n_train = int(round(n * TRAIN_FRAC))
        n_val = int(round(n * VAL_FRAC))
        n_test = n - n_train - n_val
        splits = (
            ["train"] * n_train + ["val"] * n_val + ["test"] * n_test
        )
        for split, src in zip(splits, paths):
            dest = OUT_ROOT / split / folder / src.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                dest.symlink_to(src.resolve())
            except OSError:
                shutil.copy2(src, dest)

    counts = {s: sum(1 for _ in (OUT_ROOT / s).rglob("*") if _.is_file()) for s in ("train", "val", "test")}
    n_flat = sum(1 for _ in DATA_ROOT.rglob("*") if _.is_file())
    print("Wrote flat ImageFolder root:", DATA_ROOT, f"({n_flat} symlinks)")
    print("Wrote split layout:", OUT_ROOT, "train/val/test = 70%/15%/15% per class, seed 42")
    for k, v in counts.items():
        print(f"  {k}: {v} files")


if __name__ == "__main__":
    main()
