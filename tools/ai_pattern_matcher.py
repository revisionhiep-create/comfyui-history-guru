#!/usr/bin/env python3
"""
AI Pattern Matcher - Finds code patterns and suggests improvements.
Helps AI identify common patterns and anti-patterns.
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Tuple

# Common patterns to look for
PATTERNS = {
    'good_patterns': {
        'async_await': r'async\s+function\s+\w+\s*\([^)]*\)\s*\{[^}]*await',
        'error_handling': r'try\s*\{[^}]*\}\s*catch\s*\([^)]+\)',
        'const_usage': r'const\s+\w+\s*=',
        'arrow_functions': r'const\s+\w+\s*=\s*\([^)]*\)\s*=>',
        'template_literals': r'`[^`]*\$\{[^}]+\}[^`]*`'
    },
    'anti_patterns': {
        'var_usage': r'\bvar\s+\w+',
        'missing_error_handling': r'await\s+\w+\([^)]*\)(?!\s*\.catch)',
        'innerHTML_danger': r'\.innerHTML\s*=.*\+.*\+',
        'eval_usage': r'\beval\s*\(',
        'document_write': r'document\.write\s*\('
    },
    'code_smells': {
        'long_function': r'function\s+\w+\s*\{[^}]{500,}',
        'deeply_nested': r'\{[^}]*\{[^}]*\{[^}]*\{[^}]*\{',
        'magic_numbers': r'\b\d{3,}\b',
        'duplicate_code': None  # Would need more complex analysis
    }
}

def find_patterns(content: str, pattern_type: str) -> List[Dict]:
    """Find patterns in code."""
    results = []
    patterns = PATTERNS.get(pattern_type, {})
    
    for pattern_name, pattern in patterns.items():
        if pattern is None:
            continue
        
        matches = []
        for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
            line_num = content[:match.start()].count('\n') + 1
            matches.append({
                'line': line_num,
                'match': match.group(0)[:100],  # First 100 chars
                'position': match.start()
            })
        
        if matches:
            results.append({
                'pattern': pattern_name,
                'type': pattern_type,
                'matches': matches,
                'count': len(matches)
            })
    
    return results

def suggest_improvements(content: str) -> List[str]:
    """Suggest code improvements based on patterns."""
    suggestions = []
    
    # Check for common issues
    if re.search(r'\bvar\s+', content):
        suggestions.append("Consider using 'const' or 'let' instead of 'var'")
    
    if content.count('alert(') > 0:
        suggestions.append("Consider using toast notifications instead of alert()")
    
    if re.search(r'getElementById.*getElementById', content):
        suggestions.append("Consider caching DOM queries to avoid repeated lookups")
    
    if 'async function' in content and 'try' not in content:
        suggestions.append("Consider adding error handling for async functions")
    
    # Check function complexity
    func_pattern = r'function\s+\w+\s*\{([^}]+)\}'
    for match in re.finditer(func_pattern, content, re.DOTALL):
        func_body = match.group(1)
        if len(func_body) > 1000:
            suggestions.append("Long function detected - consider breaking into smaller functions")
        if func_body.count('{') > 5:
            suggestions.append("Deeply nested code - consider refactoring")
    
    return suggestions

def analyze_code_quality(file_path: Path) -> Dict:
    """Analyze overall code quality."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    analysis = {
        'file': str(file_path),
        'good_patterns': find_patterns(content, 'good_patterns'),
        'anti_patterns': find_patterns(content, 'anti_patterns'),
        'code_smells': find_patterns(content, 'code_smells'),
        'suggestions': suggest_improvements(content),
        'metrics': {
            'total_lines': content.count('\n'),
            'total_functions': len(re.findall(r'function\s+\w+', content)),
            'async_functions': len(re.findall(r'async\s+function', content)),
            'error_handlers': len(re.findall(r'try\s*\{', content))
        }
    }
    
    return analysis

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ai_pattern_matcher.py <file>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    
    analysis = analyze_code_quality(file_path)
    print(json.dumps(analysis, indent=2))
