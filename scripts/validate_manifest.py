# Copyright 2026 Ziffany Firdinal
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0

import json
import sys
from pathlib import Path

def validate_manifest(manifest_path: Path):
    if not manifest_path.exists():
        print(f"Error: {manifest_path} does not exist.")
        return False, 0, 1

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return False, 0, 1

    regulations = manifest_data.get('regulations', [])
    num_regs = len(regulations)
    errors = 0
    
    # Map for easy lookup
    reg_map = {reg.get('regulation_id'): reg for reg in regulations if reg.get('regulation_id')}
    reg_ids = set(reg_map.keys())

    required_fields = ['regulation_id', 'full_name', 'hierarchy_level', 'date_enacted', 'status', 'file_path']
    valid_statuses = ["active", "revoked", "partially_revoked"]

    for reg in regulations:
        reg_id = reg.get('regulation_id', 'UNKNOWN')
        
        # 1. Required fields
        for field in required_fields:
            if field not in reg:
                print(f"[{reg_id}] Missing required field: {field}")
                errors += 1
        
        # 2. hierarchy_level validation
        hierarchy = reg.get('hierarchy_level')
        if hierarchy not in [1, 2, 3, 4]:
            print(f"[{reg_id}] Invalid hierarchy_level: {hierarchy}")
            errors += 1

        # 3. status validation
        status = reg.get('status')
        if status not in valid_statuses:
            print(f"[{reg_id}] Invalid status: {status}")
            errors += 1

        # 4. file_path validation
        file_path_str = reg.get('file_path')
        if file_path_str:
            # manifest is in corpus/manifest.json, so file_path (e.g. corpus/active/...)
            # relative to project root
            full_path = manifest_path.parent.parent / file_path_str
            if not full_path.exists():
                print(f"[{reg_id}] file_path does not exist: {file_path_str}")
                errors += 1

        # 5. date_revoked validation
        if reg.get('date_revoked') and status not in ["revoked", "partially_revoked"]:
            print(f"[{reg_id}] status must be 'revoked' or 'partially_revoked' if date_revoked is present")
            errors += 1

        # 6. Revokes references (List of Objects)
        revokes = reg.get('revokes') or []
        for rev_entry in revokes:
            target_id = rev_entry.get('regulation_id')
            if target_id not in reg_ids:
                # If target is not in our 7-file corpus, we don't strictly fail 
                # but for this specific task MT-2.3 we expect they are within corpus
                print(f"[{reg_id}] references unknown regulation in 'revokes': {target_id}")
                errors += 1
            else:
                # Symmetry check: target_id's 'revoked_by' should include reg_id
                target_reg = reg_map[target_id]
                revoked_by_list = target_reg.get('revoked_by') or []
                if not any(rb.get('regulation_id') == reg_id for rb in revoked_by_list):
                    print(f"[{reg_id}] revokes {target_id}, but {target_id}'s 'revoked_by' is missing {reg_id}")
                    errors += 1

        # 7. Revoked_by references (List of Objects)
        revoked_by = reg.get('revoked_by') or []
        for rb_entry in revoked_by:
            source_id = rb_entry.get('regulation_id')
            if source_id not in reg_ids:
                 # Again, if it's out-of-corpus we might skip, but let's check for symmetry if it IS in corpus
                 pass
            else:
                source_reg = reg_map[source_id]
                revokes_list = source_reg.get('revokes') or []
                if not any(rev.get('regulation_id') == reg_id for rev in revokes_list):
                    print(f"[{reg_id}] revoked_by {source_id}, but {source_id}'s 'revokes' is missing {reg_id}")
                    errors += 1

    print(f"{num_regs} regulations, {errors} validation errors")
    return errors == 0, num_regs, errors

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    manifest_file = base_dir / "corpus" / "manifest.json"
    
    is_valid, n, m = validate_manifest(manifest_file)
    if not is_valid:
        sys.exit(1)
    sys.exit(0)
