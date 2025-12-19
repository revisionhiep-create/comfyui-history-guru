#!/usr/bin/env python3
"""
Load and search coding reference databases for JS, Python, and HTML5.
This helps AI assistants understand coding patterns and APIs.
"""

import json
import sys
from pathlib import Path

def load_reference(lang):
    """Load coding reference for a language."""
    # Try data folder first, then current directory
    ref_file = Path(f'data/coding_reference_{lang}.json')
    if not ref_file.exists():
        ref_file = Path(f'../data/coding_reference_{lang}.json')
    if not ref_file.exists():
        ref_file = Path(f'coding_reference_{lang}.json')
    if not ref_file.exists():
        return None
    with open(ref_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_reference(lang, query):
    """Search coding reference for a query."""
    ref = load_reference(lang)
    if not ref:
        return None
    
    query_lower = query.lower()
    results = []
    
    for category, content in ref.items():
        if query_lower in category.lower():
            results.append((category, content))
            continue
        
        if isinstance(content, dict):
            for key, value in content.items():
                if query_lower in key.lower() or (isinstance(value, str) and query_lower in value.lower()):
                    results.append((f"{category}.{key}", value))
    
    return results

def get_pattern(lang, category, pattern_name):
    """Get a specific pattern from reference."""
    ref = load_reference(lang)
    if not ref or category not in ref:
        return None
    
    category_data = ref[category]
    if isinstance(category_data, dict) and 'patterns' in category_data:
        patterns = category_data['patterns']
        if pattern_name in patterns:
            return patterns[pattern_name]
    
    return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python load_coding_reference.py <lang> [query]")
        print("Languages: js, python, html5")
        sys.exit(1)
    
    lang = sys.argv[1]
    query = sys.argv[2] if len(sys.argv) > 2 else None
    
    if query:
        results = search_reference(lang, query)
        if results:
            for key, value in results:
                print(f"\n=== {key} ===")
                if isinstance(value, dict):
                    print(json.dumps(value, indent=2))
                else:
                    print(value)
        else:
            print(f"No results found for '{query}' in {lang}")
    else:
        ref = load_reference(lang)
        if ref:
            print(f"\n=== {lang.upper()} Coding Reference ===")
            print(f"Categories: {', '.join(ref.keys())}")
        else:
            print(f"Reference file for {lang} not found")
