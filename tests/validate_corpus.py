# Copyright 2026 Ziffany Firdinal
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0

"""Corpus integrity validator — validates corpus/manifest.json against actual files."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from validate_manifest import validate_manifest

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    manifest_file = base_dir / "corpus" / "manifest.json"
    is_valid, n, errors = validate_manifest(manifest_file)
    if not is_valid:
        sys.exit(1)
    sys.exit(0)
