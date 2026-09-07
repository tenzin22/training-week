#!/usr/bin/env python3
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
source = root / "starter-project"
destination = root / "docs" / "assets" / "downloads" / "starter-project.zip"
destination.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(source.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc" or ".git" in path.parts:
            continue
        archive.write(path, Path("starter-project") / path.relative_to(source))
print(destination)
