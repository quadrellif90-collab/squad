#!/usr/bin/env python3
import shutil
from pathlib import Path
src = Path(".")
dst = Path.home() / ".agents" / "squad"
dst.mkdir(parents=True, exist_ok=True)
shutil.copytree("config", dst / "config", dirs_exist_ok=True)
shutil.copytree("disciplines", dst / "disciplines", dirs_exist_ok=True)
shutil.copy("src/squad_server.py", dst / "scripts")
print("Squad installed to", dst)
