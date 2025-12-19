#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guru Manager HTML Static Analyzer
Comprehensive testing and debugging tool for the HTML file
"""

import re
import json
import sys
from collections import defaultdict
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

class GuruManagerAnalyzer:
    def __init__(self, html_file_path):
        self.html_file_path = Path(html_file_path)
        self.content = ""
        self.issues = []
        self.warnings = []
        self.info = []
        self.stats = defaultdict(int)
        
    def load_file(self):
        """Load the HTML file"""
        try:
            with open(self.html_file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            self.info.append(f"[OK] File loaded: {len(self.content)} characters")
            return True
        except FileNotFoundError:
            self.issues.append(f"[ERROR] File not found: {self.html_file_path}")
            return False
        except Exception as e:
            self.issues.append(f"[ERROR] Error loading file: {e}")
            return False
    
    def analyze_structure(self):
        """Analyze HTML structure"""
        print("\n[STRUCTURE] Analyzing HTML Structure...")
        
        # Basic structure checks
        checks = {
            'DOCTYPE': ('<!DOCTYPE', 'Missing DOCTYPE declaration'),
            '<html': ('<html', 'Missing <html> tag'),
            '<head': ('<head', 'Missing <head> tag'),
            '<body': ('<body', 'Missing <body> tag'),
            '</html>': ('</html>', 'Missing closing </html> tag'),
        }
        
        for name, (pattern, error) in checks.items():
            if pattern in self.content:
                self.info.append(f"[OK] {name}: Found")
            else:
                self.issues.append(f"[ERROR] {name}: {error}")
    
    def analyze_javascript(self):
        """Analyze JavaScript code"""
        print("\n[JS] Analyzing JavaScript...")
        
        # Extract all script tags
        script_pattern = r'<script[^>]*>([\s\S]*?)</script>'
        scripts = re.findall(script_pattern, self.content, re.IGNORECASE)
        
        self.stats['script_tags'] = len(scripts)
        self.info.append(f"Found {len(scripts)} script tag(s)")
        
        all_js = '\n'.join(scripts)
        
        # Find function definitions
        function_pattern = r'function\s+(\w+)\s*\([^)]*\)'
        functions = re.findall(function_pattern, all_js)
        self.stats['functions'] = len(functions)
        self.info.append(f"Found {len(functions)} function definitions")
        
        # Find arrow functions
        arrow_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>'
        arrow_functions = re.findall(arrow_pattern, all_js)
        self.stats['arrow_functions'] = len(arrow_functions)
        self.info.append(f"Found {len(arrow_functions)} arrow functions")
        
        # Critical functions check
        critical_functions = [
            'initFileSystem', 'fullScan', 'rend', 'setView', 'enterDet',
            'exitDetail', 'pop', 'parseComfy', 'parseA1111', 'extractText',
            'toggleTheme', 'showBatchOps', 'exportMetadata', 'applyAdvSearch',
            'addToCompare', 'clearComparison', 'toggleFavorite'
        ]
        
        all_functions = functions + arrow_functions
        missing_critical = [f for f in critical_functions if f not in all_functions]
        
        if missing_critical:
            self.issues.append(f"[ERROR] Missing critical functions: {', '.join(missing_critical)}")
        else:
            self.info.append("[OK] All critical functions found")
        
        # Check for common issues
        if 'console.log' in all_js:
            count = all_js.count('console.log')
            self.warnings.append(f"[WARN] Found {count} console.log statements (consider removing)")
        
        if 'debugger' in all_js:
            self.warnings.append("[WARN] Found 'debugger' statements")
        
        # Check for try-catch balance
        try_count = all_js.count('try {')
        catch_count = all_js.count('catch')
        if try_count != catch_count:
            self.warnings.append(f"[WARN] Try-catch mismatch: {try_count} try, {catch_count} catch")
        
        # Check for event listeners
        if 'addEventListener' in all_js:
            add_count = all_js.count('addEventListener')
            remove_count = all_js.count('removeEventListener')
            if remove_count < add_count:
                self.warnings.append(f"[WARN] Potential memory leak: {add_count} addEventListener, {remove_count} removeEventListener")
    
    def analyze_elements(self):
        """Analyze HTML elements"""
        print("\n[HTML] Analyzing HTML Elements...")
        
        # Critical element IDs
        critical_ids = [
            'grid', 'sidebar', 'tree', 'inspector', 'sIn', 'bGrid', 'bList',
            'bStats', 'bTree', 'bCompare', 'themeToggle', 'detailView',
            'batchOps', 'advSearch', 'keyboardHelp'
        ]
        
        missing_elements = []
        for elem_id in critical_ids:
            if f'id="{elem_id}"' not in self.content and f"id='{elem_id}'" not in self.content:
                missing_elements.append(elem_id)
        
        if missing_elements:
            self.issues.append(f"[ERROR] Missing critical elements: {', '.join(missing_elements)}")
        else:
            self.info.append("[OK] All critical elements found")
        
        # Count elements
        self.stats['buttons'] = len(re.findall(r'<button[^>]*>', self.content, re.IGNORECASE))
        self.stats['inputs'] = len(re.findall(r'<input[^>]*>', self.content, re.IGNORECASE))
        self.stats['divs'] = len(re.findall(r'<div[^>]*>', self.content, re.IGNORECASE))
        self.stats['overlays'] = len(re.findall(r'class="overlay"', self.content, re.IGNORECASE))
        
        self.info.append(f"Found {self.stats['buttons']} buttons, {self.stats['inputs']} inputs, {self.stats['divs']} divs")
    
    def analyze_css(self):
        """Analyze CSS"""
        print("\n[CSS] Analyzing CSS...")
        
        # Extract CSS
        style_pattern = r'<style[^>]*>([\s\S]*?)</style>'
        styles = re.findall(style_pattern, self.content, re.IGNORECASE)
        css_content = '\n'.join(styles)
        
        # Check for CSS variables
        if 'var(--' in css_content or 'var(--' in self.content:
            self.info.append("[OK] Using CSS custom properties")
        else:
            self.warnings.append("[WARN] No CSS variables found")
        
        # Check for responsive design
        if '@media' in css_content:
            self.info.append("[OK] Found media queries (responsive design)")
        else:
            self.warnings.append("[WARN] No media queries found")
        
        # Check for modern layout
        has_flex = 'display:flex' in css_content or 'display:flex' in self.content
        has_grid = 'display:grid' in css_content or 'display:grid' in self.content
        
        if has_flex and has_grid:
            self.info.append("[OK] Using Flexbox & Grid")
        elif has_flex:
            self.info.append("[OK] Using Flexbox")
        elif has_grid:
            self.info.append("[OK] Using Grid")
        else:
            self.warnings.append("[WARN] No modern layout system detected")
    
    def analyze_dependencies(self):
        """Analyze dependencies and APIs"""
        print("\n[DEPS] Analyzing Dependencies...")
        
        # Check for File System Access API
        if 'showDirectoryPicker' in self.content:
            self.info.append("[OK] Using File System Access API")
        else:
            self.warnings.append("[WARN] Not using File System Access API")
        
        # Check for IndexedDB
        if 'indexedDB' in self.content or 'IndexedDB' in self.content:
            self.info.append("[OK] Using IndexedDB")
        else:
            self.warnings.append("[WARN] Not using IndexedDB")
        
        # Check for localStorage
        if 'localStorage' in self.content:
            self.info.append("[OK] Using localStorage")
        else:
            self.warnings.append("[WARN] Not using localStorage")
        
        # Check for external scripts
        if re.search(r'<script\s+src=', self.content, re.IGNORECASE):
            self.warnings.append("[WARN] Found external script dependencies")
        else:
            self.info.append("[OK] No external dependencies (offline-friendly)")
    
    def analyze_code_quality(self):
        """Analyze code quality issues"""
        print("\n[QUALITY] Analyzing Code Quality...")
        
        # Check for TODO/FIXME
        todos = len(re.findall(r'TODO|FIXME|XXX', self.content, re.IGNORECASE))
        if todos > 0:
            self.warnings.append(f"[WARN] Found {todos} TODO/FIXME comments")
        
        # Check for hardcoded values
        hardcoded_colors = len(re.findall(r'#[0-9a-fA-F]{6}', self.content))
        if hardcoded_colors > 10:
            self.warnings.append(f"[WARN] Found {hardcoded_colors} hardcoded hex colors")
        
        # Check for inline styles
        inline_styles = len(re.findall(r'style="[^"]*"', self.content))
        if inline_styles > 50:
            self.warnings.append(f"[WARN] Found {inline_styles} inline styles (consider using CSS classes)")
        
        # Check for magic numbers
        magic_numbers = re.findall(r'\b\d{3,}\b', self.content)
        if len(magic_numbers) > 20:
            self.warnings.append(f"[WARN] Found many magic numbers (consider using constants)")
    
    def check_function_calls(self):
        """Check if functions are called"""
        print("\n[CALLS] Checking Function Calls...")
        
        # Extract function definitions
        function_pattern = r'function\s+(\w+)\s*\('
        defined_functions = set(re.findall(function_pattern, self.content))
        
        # Check if functions are called
        unused_functions = []
        for func in defined_functions:
            # Count occurrences (definition + calls)
            pattern = rf'\b{func}\s*\('
            count = len(re.findall(pattern, self.content))
            if count <= 1:  # Only definition, no calls
                unused_functions.append(func)
        
        if unused_functions:
            self.warnings.append(f"[WARN] Potentially unused functions: {', '.join(unused_functions[:5])}")
    
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "="*60)
        print("[REPORT] GURU MANAGER HTML ANALYSIS REPORT")
        print("="*60)
        
        print(f"\n[FILE] File: {self.html_file_path}")
        print(f"[SIZE] Size: {len(self.content):,} characters")
        
        print("\n[OK] INFO:")
        for item in self.info:
            print(f"  {item}")
        
        if self.warnings:
            print("\n[WARN] WARNINGS:")
            for item in self.warnings:
                print(f"  {item}")
        
        if self.issues:
            print("\n[ERROR] ISSUES:")
            for item in self.issues:
                print(f"  {item}")
        
        print("\n[STATS] STATISTICS:")
        for key, value in sorted(self.stats.items()):
            print(f"  {key}: {value}")
        
        # Summary
        print("\n" + "="*60)
        print("[SUMMARY] SUMMARY")
        print("="*60)
        print(f"[OK] Info items: {len(self.info)}")
        print(f"[WARN] Warnings: {len(self.warnings)}")
        print(f"[ERROR] Issues: {len(self.issues)}")
        
        if len(self.issues) == 0 and len(self.warnings) < 5:
            print("\n[SUCCESS] Overall: Code looks good!")
        elif len(self.issues) == 0:
            print("\n[OK] Overall: Minor warnings, but no critical issues")
        else:
            print("\n[WARN] Overall: Some issues need attention")
        
        return {
            'info': self.info,
            'warnings': self.warnings,
            'issues': self.issues,
            'stats': dict(self.stats)
        }
    
    def run_all_analyses(self):
        """Run all analyses"""
        if not self.load_file():
            return None
        
        self.analyze_structure()
        self.analyze_javascript()
        self.analyze_elements()
        self.analyze_css()
        self.analyze_dependencies()
        self.analyze_code_quality()
        self.check_function_calls()
        
        return self.generate_report()

def main():
    """Main function"""
    # Try apps folder, then root
    html_file = Path(__file__).parent.parent / "apps" / "Guru Manager.html"
    if not html_file.exists():
        html_file = Path(__file__).parent / "Guru Manager.html"
    if not html_file.exists():
        html_file = Path("apps/Guru Manager.html")
    
    if not html_file.exists():
        print(f"[ERROR] File not found: {html_file}")
        print("Please ensure 'Guru Manager.html' is in apps/ folder or root")
        return
    
    analyzer = GuruManagerAnalyzer(html_file)
    report = analyzer.run_all_analyses()
    
    # Save report to JSON
    if report:
        report_file = html_file.parent / "guru_manager_analysis_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print(f"\n[SAVED] Report saved to: {report_file}")

if __name__ == "__main__":
    main()
