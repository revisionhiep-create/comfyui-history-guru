#!/usr/bin/env python3
"""
AI Code Analyzer - Analyzes code structure, dependencies, and patterns.
Helps AI understand codebase before making changes.
"""

import re
import json
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple

def analyze_javascript_structure(js_content: str) -> Dict:
    """Analyze JavaScript code structure."""
    analysis = {
        'functions': [],
        'variables': [],
        'event_listeners': [],
        'dom_queries': [],
        'async_operations': [],
        'dependencies': set(),
        'potential_issues': []
    }
    
    # Find function definitions
    func_pattern = r'(?:async\s+)?function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>|let\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>'
    for match in re.finditer(func_pattern, js_content):
        func_name = match.group(1) or match.group(2) or match.group(3)
        if func_name:
            analysis['functions'].append(func_name)
    
    # Find DOM queries
    dom_patterns = [
        r"getElementById\(['\"]([^'\"]+)['\"]\)",
        r"querySelector\(['\"]([^'\"]+)['\"]\)",
        r"querySelectorAll\(['\"]([^'\"]+)['\"]\)"
    ]
    for pattern in dom_patterns:
        for match in re.finditer(pattern, js_content):
            analysis['dom_queries'].append(match.group(1))
    
    # Find event listeners
    event_pattern = r"addEventListener\(['\"]([^'\"]+)['\"]"
    for match in re.finditer(event_pattern, js_content):
        analysis['event_listeners'].append(match.group(1))
    
    # Find async operations
    async_patterns = [
        r"await\s+(\w+)\([^)]*\)",
        r"\.then\([^)]*\)",
        r"Promise\.(all|race|resolve|reject)"
    ]
    for pattern in async_patterns:
        if re.search(pattern, js_content):
            analysis['async_operations'].append(pattern)
    
    # Find potential issues
    if 'getElementById' in js_content and 'querySelector' not in js_content:
        analysis['potential_issues'].append("Mixing getElementById and querySelector - consider consistency")
    
    if js_content.count('async function') > 10:
        analysis['potential_issues'].append("Many async functions - consider error handling patterns")
    
    return analysis

def analyze_code_dependencies(file_path: Path) -> Dict:
    """Analyze what a file depends on."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    dependencies = {
        'apis': set(),
        'functions_called': set(),
        'dom_elements': set(),
        'external_libs': set()
    }
    
    # File System Access API
    if 'showDirectoryPicker' in content:
        dependencies['apis'].add('File System Access API')
    if 'indexedDB' in content:
        dependencies['apis'].add('IndexedDB')
    if 'localStorage' in content:
        dependencies['apis'].add('localStorage')
    
    # Function calls
    func_call_pattern = r'(\w+)\s*\('
    for match in re.finditer(func_call_pattern, content):
        func_name = match.group(1)
        if func_name not in ['console', 'document', 'window', 'Math', 'Array', 'Object', 'String', 'Number', 'Date', 'JSON', 'Promise', 'URL', 'Blob', 'TextDecoder', 'TextEncoder', 'DataView', 'Uint8Array', 'new', 'await', 'async', 'if', 'for', 'while', 'return', 'try', 'catch', 'throw', 'typeof', 'instanceof']:
            dependencies['functions_called'].add(func_name)
    
    # DOM elements
    dom_pattern = r"getElementById\(['\"]([^'\"]+)['\"]\)"
    for match in re.finditer(dom_pattern, content):
        dependencies['dom_elements'].add(match.group(1))
    
    return dependencies

def find_code_patterns(file_path: Path, patterns: List[str]) -> Dict[str, List[Tuple[int, str]]]:
    """Find specific code patterns in a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    results = {}
    for pattern_name, pattern in patterns:
        matches = []
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                matches.append((i, line.strip()))
        results[pattern_name] = matches
    
    return results

def analyze_function_complexity(js_content: str) -> List[Dict]:
    """Analyze function complexity."""
    functions = []
    
    # Find functions and count complexity
    func_pattern = r'(?:async\s+)?function\s+(\w+)\s*\{([^}]+)\}'
    for match in re.finditer(func_pattern, js_content, re.DOTALL):
        func_name = match.group(1)
        func_body = match.group(2)
        
        complexity = {
            'name': func_name,
            'lines': func_body.count('\n'),
            'nested_levels': func_body.count('{') - func_body.count('}'),
            'async_operations': len(re.findall(r'await\s+', func_body)),
            'conditionals': len(re.findall(r'\b(if|else|switch|case)\b', func_body)),
            'loops': len(re.findall(r'\b(for|while|forEach|map|filter)\b', func_body))
        }
        functions.append(complexity)
    
    return functions

def generate_code_report(file_path: Path) -> Dict:
    """Generate comprehensive code analysis report."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    report = {
        'file': str(file_path),
        'size': len(content),
        'lines': content.count('\n'),
        'structure': analyze_javascript_structure(content),
        'dependencies': analyze_code_dependencies(file_path),
        'complexity': analyze_function_complexity(content),
        'suggestions': []
    }
    
    # Generate suggestions
    if report['structure']['functions']:
        if len(report['structure']['functions']) > 20:
            report['suggestions'].append("Consider breaking into smaller modules - many functions detected")
    
    if report['dependencies']['apis']:
        report['suggestions'].append(f"Uses APIs: {', '.join(report['dependencies']['apis'])}")
    
    return report

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ai_code_analyzer.py <file>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    
    report = generate_code_report(file_path)
    print(json.dumps(report, indent=2))
