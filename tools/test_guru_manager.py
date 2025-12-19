#!/usr/bin/env python3
"""
Comprehensive testing tool for Guru Manager.html
Tests JavaScript syntax, function definitions, DOM elements, and common issues.
"""

import re
import json
import sys
from pathlib import Path

def extract_script_content(html_path):
    """Extract JavaScript from HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract script tags
    script_pattern = r'<script[^>]*>(.*?)</script>'
    scripts = re.findall(script_pattern, content, re.DOTALL | re.IGNORECASE)
    return '\n'.join(scripts), content

def extract_html_elements(html_content):
    """Extract important HTML elements."""
    elements = {
        'buttons': re.findall(r'<button[^>]*onclick="([^"]+)"', html_content, re.IGNORECASE),
        'ids': re.findall(r'id="([^"]+)"', html_content, re.IGNORECASE),
        'functions_called': re.findall(r'onclick="([^"]+)"', html_content, re.IGNORECASE),
    }
    return elements

def check_function_definitions(js_content):
    """Check if required functions are defined."""
    required_functions = [
        'initFileSystem',
        'fullScan',
        'setView',
        'rend',
        'proc',
        'extractText',
        'parseMetadata',
        'parseComfy',
        'parseA1111',
    ]
    
    found = {}
    for func in required_functions:
        # Check for function declaration
        pattern = rf'(?:function\s+{func}|const\s+{func}\s*=|let\s+{func}\s*=|var\s+{func}\s*=|\basync\s+function\s+{func})'
        if re.search(pattern, js_content):
            found[func] = True
        else:
            found[func] = False
    
    return found

def check_syntax_errors(js_content):
    """Basic syntax checking for common JavaScript errors."""
    errors = []
    
    # More accurate bracket counting (ignore strings and comments)
    # Remove strings first
    no_strings = re.sub(r'`[^`]*`', '', js_content)  # Template literals
    no_strings = re.sub(r"'[^']*'", '', no_strings)  # Single quotes
    no_strings = re.sub(r'"[^"]*"', '', no_strings)  # Double quotes
    
    # Check for unmatched brackets
    open_braces = no_strings.count('{')
    close_braces = no_strings.count('}')
    if open_braces != close_braces:
        errors.append(f"Unmatched braces: {open_braces} open, {close_braces} close")
    
    open_parens = no_strings.count('(')
    close_parens = no_strings.count(')')
    if open_parens != close_parens:
        errors.append(f"Unmatched parentheses: {open_parens} open, {close_parens} close")
    
    open_brackets = no_strings.count('[')
    close_brackets = no_strings.count(']')
    if open_brackets != close_brackets:
        errors.append(f"Unmatched brackets: {open_brackets} open, {close_brackets} close")
    
    return errors

def check_function_calls(js_content, html_elements):
    """Check if functions called in HTML exist in JavaScript."""
    missing = []
    for func_call in html_elements['functions_called']:
        # Extract function name (before first parenthesis)
        func_name = func_call.split('(')[0].strip()
        if func_name:
            # Check if function is defined
            pattern = rf'(?:function\s+{re.escape(func_name)}|const\s+{re.escape(func_name)}\s*=|let\s+{re.escape(func_name)}\s*=|var\s+{re.escape(func_name)}\s*=|\basync\s+function\s+{re.escape(func_name)})'
            if not re.search(pattern, js_content):
                missing.append(func_name)
    
    return list(set(missing))

def check_dom_access(js_content, html_elements):
    """Check if DOM elements accessed in JS exist in HTML."""
    issues = []
    # Find getElementById calls
    get_element_calls = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js_content)
    for element_id in get_element_calls:
        if element_id not in html_elements['ids']:
            issues.append(f"JavaScript accesses element '{element_id}' but it doesn't exist in HTML")
    
    return issues

def check_critical_functions(js_content):
    """Check critical functions for common issues."""
    issues = []
    
    # Check initFileSystem
    if 'async function initFileSystem' in js_content or 'function initFileSystem' in js_content:
        init_match = re.search(r'(?:async\s+)?function\s+initFileSystem\s*\{([^}]+)\}', js_content, re.DOTALL)
        if init_match:
            init_body = init_match.group(1)
            if 'showDirectoryPicker' not in init_body:
                issues.append("initFileSystem doesn't call showDirectoryPicker")
            if 'fullScan' not in init_body:
                issues.append("initFileSystem doesn't call fullScan")
    
    # Check extractText returns a string
    if 'async function extractText' in js_content or 'function extractText' in js_content:
        if 'return fullText' in js_content:
            pass  # Looks good - returns fullText
        elif 'return' in js_content:
            # Might return something else, but at least it returns
            pass
        else:
            issues.append("extractText might not return a value")
    
    return issues

def run_tests(html_path):
    """Run all tests on the HTML file."""
    print(f"Testing: {html_path}")
    print("=" * 60)
    
    try:
        js_content, html_content = extract_script_content(html_path)
        html_elements = extract_html_elements(html_content)
        
        results = {
            'syntax_errors': check_syntax_errors(js_content),
            'function_definitions': check_function_definitions(js_content),
            'missing_functions': check_function_calls(js_content, html_elements),
            'dom_issues': check_dom_access(js_content, html_elements),
            'critical_issues': check_critical_functions(js_content),
        }
        
        # Print results
        print("\n[SYNTAX CHECK]")
        if results['syntax_errors']:
            print("  [ERROR] Errors found:")
            for error in results['syntax_errors']:
                print(f"    - {error}")
        else:
            print("  [OK] No syntax errors detected")
        
        print("\n[FUNCTION DEFINITIONS]")
        all_defined = True
        for func, defined in results['function_definitions'].items():
            status = "[OK]" if defined else "[MISSING]"
            print(f"  {status} {func}")
            if not defined:
                all_defined = False
        
        print("\n[MISSING FUNCTIONS]")
        if results['missing_functions']:
            print("  [ERROR] Functions called in HTML but not defined:")
            for func in results['missing_functions']:
                print(f"    - {func}")
        else:
            print("  [OK] All called functions are defined")
        
        print("\n[DOM ACCESS]")
        if results['dom_issues']:
            print("  [WARN] Potential issues:")
            for issue in results['dom_issues']:
                print(f"    - {issue}")
        else:
            print("  [OK] All accessed DOM elements exist")
        
        print("\n[CRITICAL CHECKS]")
        if results['critical_issues']:
            print("  [WARN] Issues found:")
            for issue in results['critical_issues']:
                print(f"    - {issue}")
        else:
            print("  [OK] Critical functions look good")
        
        # Summary
        print("\n" + "=" * 60)
        total_issues = (
            len(results['syntax_errors']) +
            sum(1 for v in results['function_definitions'].values() if not v) +
            len(results['missing_functions']) +
            len(results['dom_issues']) +
            len(results['critical_issues'])
        )
        
        if total_issues == 0:
            print("[PASS] ALL TESTS PASSED")
            return 0
        else:
            print(f"[FAIL] {total_issues} issue(s) found")
            return 1
            
    except Exception as e:
        print(f"[ERROR] Error running tests: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    if len(sys.argv) > 1:
        html_file = Path(sys.argv[1])
    else:
        # Try apps folder first, then root
        html_file = Path('apps/Guru Manager.html')
        if not html_file.exists():
            html_file = Path('../apps/Guru Manager.html')
        if not html_file.exists():
            html_file = Path('Guru Manager.html')
    
    if not html_file.exists():
        print(f"Error: {html_file} not found")
        print("Usage: python test_guru_manager.py [path/to/file.html]")
        sys.exit(1)
    
    exit_code = run_tests(html_file)
    sys.exit(exit_code)
