#!/usr/bin/env python3
"""
AI Code Diff Tool - Compares code before and after changes.
Helps AI understand what changed and verify modifications.
"""

import difflib
from pathlib import Path
from typing import List, Tuple

def compare_files(file1: Path, file2: Path) -> List[Tuple[str, int, str, int, str]]:
    """Compare two files and return differences."""
    with open(file1, 'r', encoding='utf-8') as f:
        lines1 = f.readlines()
    
    with open(file2, 'r', encoding='utf-8') as f:
        lines2 = f.readlines()
    
    diff = list(difflib.unified_diff(
        lines1, lines2,
        fromfile=str(file1),
        tofile=str(file2),
        lineterm=''
    ))
    
    return diff

def analyze_changes(diff: List[str]) -> Dict:
    """Analyze what changed in the diff."""
    changes = {
        'added_lines': 0,
        'removed_lines': 0,
        'modified_functions': [],
        'added_functions': [],
        'removed_functions': [],
        'dom_changes': [],
        'api_changes': []
    }
    
    current_function = None
    for line in diff:
        if line.startswith('+') and not line.startswith('+++'):
            changes['added_lines'] += 1
            # Check for function definitions
            if 'function' in line or '=>' in line:
                func_match = re.search(r'function\s+(\w+)|const\s+(\w+)\s*=', line)
                if func_match:
                    func_name = func_match.group(1) or func_match.group(2)
                    if func_name not in changes['added_functions']:
                        changes['added_functions'].append(func_name)
        
        elif line.startswith('-') and not line.startswith('---'):
            changes['removed_lines'] += 1
            # Check for removed functions
            if 'function' in line:
                func_match = re.search(r'function\s+(\w+)', line)
                if func_match:
                    func_name = func_match.group(1)
                    if func_name not in changes['removed_functions']:
                        changes['removed_functions'].append(func_name)
        
        # Check for DOM changes
        if 'getElementById' in line or 'querySelector' in line:
            changes['dom_changes'].append(line.strip())
        
        # Check for API changes
        if any(api in line for api in ['showDirectoryPicker', 'indexedDB', 'localStorage']):
            changes['api_changes'].append(line.strip())
    
    return changes

def find_function_changes(file1: Path, file2: Path, function_name: str) -> List[str]:
    """Find changes to a specific function."""
    with open(file1, 'r', encoding='utf-8') as f:
        content1 = f.read()
    
    with open(file2, 'r', encoding='utf-8') as f:
        content2 = f.read()
    
    # Extract function from both files
    pattern1 = rf'function\s+{function_name}\s*{{([^}}]+)}}'
    match1 = re.search(pattern1, content1, re.DOTALL)
    match2 = re.search(pattern1, content2, re.DOTALL)
    
    if not match1 or not match2:
        return []
    
    func1_lines = match1.group(1).split('\n')
    func2_lines = match2.group(1).split('\n')
    
    diff = list(difflib.unified_diff(
        func1_lines, func2_lines,
        fromfile=f'{function_name} (before)',
        tofile=f'{function_name} (after)',
        lineterm=''
    ))
    
    return diff

if __name__ == '__main__':
    import sys
    import re
    
    if len(sys.argv) < 3:
        print("Usage: python ai_code_diff.py <file1> <file2> [function_name]")
        sys.exit(1)
    
    file1 = Path(sys.argv[1])
    file2 = Path(sys.argv[2])
    
    if not file1.exists() or not file2.exists():
        print("Error: Both files must exist")
        sys.exit(1)
    
    if len(sys.argv) > 3:
        # Compare specific function
        func_name = sys.argv[3]
        diff = find_function_changes(file1, file2, func_name)
        print('\n'.join(diff))
    else:
        # Compare entire files
        diff = compare_files(file1, file2)
        changes = analyze_changes(diff)
        
        print(f"Changes: +{changes['added_lines']} -{changes['removed_lines']}")
        if changes['added_functions']:
            print(f"Added functions: {', '.join(changes['added_functions'])}")
        if changes['removed_functions']:
            print(f"Removed functions: {', '.join(changes['removed_functions'])}")
        print("\nDiff:")
        print('\n'.join(diff[:50]))  # Show first 50 lines
