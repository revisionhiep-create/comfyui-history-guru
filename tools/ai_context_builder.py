#!/usr/bin/env python3
"""
AI Context Builder - Builds context about codebase for AI understanding.
Helps AI understand relationships between functions, files, and features.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Set

def extract_function_signatures(content: str) -> Dict[str, Dict]:
    """Extract all function signatures and their contexts."""
    functions = {}
    
    # Match function definitions
    patterns = [
        r'(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)\s*\{',
        r'const\s+(\w+)\s*=\s*(?:async\s+)?\(([^)]*)\)\s*=>',
        r'let\s+(\w+)\s*=\s*(?:async\s+)?\(([^)]*)\)\s*=>'
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            func_name = match.group(1)
            params = match.group(2) if len(match.groups()) > 1 else ''
            
            # Find function body (simplified)
            start = match.end()
            brace_count = 1
            end = start
            while end < len(content) and brace_count > 0:
                if content[end] == '{':
                    brace_count += 1
                elif content[end] == '}':
                    brace_count -= 1
                end += 1
            
            func_body = content[start:end-1]
            
            # Analyze what function does
            calls = re.findall(r'(\w+)\s*\(', func_body)
            dom_queries = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", func_body)
            async_ops = 'await' in func_body
            
            functions[func_name] = {
                'name': func_name,
                'params': params,
                'calls': list(set(calls)),
                'dom_elements': list(set(dom_queries)),
                'is_async': async_ops,
                'line': content[:match.start()].count('\n') + 1
            }
    
    return functions

def build_dependency_graph(functions: Dict) -> Dict:
    """Build graph of function dependencies."""
    graph = {}
    
    for func_name, func_info in functions.items():
        graph[func_name] = {
            'calls': [],
            'called_by': []
        }
        
        # Find what this function calls
        for called_func in func_info['calls']:
            if called_func in functions:
                graph[func_name]['calls'].append(called_func)
                if called_func not in graph:
                    graph[called_func] = {'calls': [], 'called_by': []}
                graph[called_func]['called_by'].append(func_name)
    
    return graph

def find_related_functions(function_name: str, functions: Dict, graph: Dict) -> Dict:
    """Find functions related to a given function."""
    related = {
        'calls': [],
        'called_by': [],
        'uses_same_dom': [],
        'similar_pattern': []
    }
    
    if function_name not in graph:
        return related
    
    # Direct relationships
    related['calls'] = graph[function_name]['calls']
    related['called_by'] = graph[function_name]['called_by']
    
    # Functions using same DOM elements
    target_dom = set(functions.get(function_name, {}).get('dom_elements', []))
    for func_name_other, func_info in functions.items():
        if func_name_other != function_name:
            other_dom = set(func_info.get('dom_elements', []))
            if target_dom & other_dom:  # Intersection
                related['uses_same_dom'].append(func_name_other)
    
    return related

def generate_context_report(file_path: Path) -> Dict:
    """Generate comprehensive context report."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    functions = extract_function_signatures(content)
    graph = build_dependency_graph(functions)
    
    # Find critical functions
    critical_functions = []
    for func_name, func_info in functions.items():
        if any(keyword in func_name.lower() for keyword in ['init', 'load', 'save', 'delete', 'create']):
            critical_functions.append(func_name)
    
    report = {
        'file': str(file_path),
        'functions': functions,
        'dependency_graph': graph,
        'critical_functions': critical_functions,
        'total_functions': len(functions)
    }
    
    return report

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ai_context_builder.py <file> [function_name]")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    
    report = generate_context_report(file_path)
    
    if len(sys.argv) > 2:
        # Show context for specific function
        func_name = sys.argv[2]
        related = find_related_functions(func_name, report['functions'], report['dependency_graph'])
        print(json.dumps({
            'function': func_name,
            'related': related,
            'info': report['functions'].get(func_name, {})
        }, indent=2))
    else:
        print(json.dumps(report, indent=2))
