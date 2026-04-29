# Copyright 2026 Ziffany Firdinal
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0

import argparse
import os
import sys

LICENSE_HEADER = """# Copyright 2026 Ziffany Firdinal
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
"""

_MARKER = "Licensed under the Apache License, Version 2.0"


def _has_header(content: str) -> bool:
    return _MARKER in content


def add_header(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if _has_header(content):
        return
    print(f"Adding header to {file_path}")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(LICENSE_HEADER + "\n" + content)


def _iter_py_files(dir_path: str):
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in ("venv", "node_modules", ".git", "__pycache__")]
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)


def process_directory(dir_path: str) -> None:
    for fp in _iter_py_files(dir_path):
        add_header(fp)


def check_directory(dir_path: str) -> list[str]:
    missing = []
    for fp in _iter_py_files(dir_path):
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        if not _has_header(content):
            missing.append(fp)
    return missing


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apache 2.0 license header tool")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check mode: report files missing headers, exit 1 if any found (no modifications)",
    )
    args = parser.parse_args()

    if args.check:
        missing = check_directory(".")
        if missing:
            print(f"ERROR: {len(missing)} .py file(s) missing Apache 2.0 license header:")
            for fp in missing:
                print(f"  {fp}")
            sys.exit(1)
        print(f"OK: all .py files have Apache 2.0 license header.")
        sys.exit(0)
    else:
        process_directory(".")
