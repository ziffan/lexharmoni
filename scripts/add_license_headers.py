# Copyright 2026 Ziffany Firdinal
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0

import os

LICENSE_HEADER = """# Copyright 2026 Ziffany Firdinal
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
"""

def add_header(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "Licensed under the Apache License, Version 2.0" in content:
        return # Already has header
    
    print(f"Adding header to {file_path}")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(LICENSE_HEADER + "\n" + content)

def process_directory(dir_path):
    for root, dirs, files in os.walk(dir_path):
        # Skip venv and node_modules
        if 'venv' in root or 'node_modules' in root or '.git' in root:
            continue
            
        for file in files:
            if file.endswith('.py'):
                add_header(os.path.join(root, file))

if __name__ == "__main__":
    # Process root and specific folders if they exist
    process_directory('.')
