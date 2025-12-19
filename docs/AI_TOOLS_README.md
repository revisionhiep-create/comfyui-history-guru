# AI Coding Assistant Tools

## Overview

These tools help AI assistants understand codebases, analyze changes, and code more effectively. Based on research of what professional AI coding tools provide.

## Tools Available

### 1. `ai_code_analyzer.py`
**Purpose**: Analyzes code structure, dependencies, and complexity

**Usage:**
```bash
python ai_code_analyzer.py "Guru Manager.html"
```

**What it does:**
- Extracts function definitions
- Finds DOM queries and event listeners
- Identifies async operations
- Detects potential issues
- Analyzes function complexity

**When to use:**
- Before making changes to understand code structure
- When debugging to find dependencies
- When refactoring to understand complexity

### 2. `ai_code_diff.py`
**Purpose**: Compares code before and after changes

**Usage:**
```bash
# Compare two files
python ai_code_diff.py "backup/Guru Manager_20251219_130722.html" "Guru Manager.html"

# Compare specific function
python ai_code_diff.py file1.html file2.html "functionName"
```

**What it does:**
- Shows line-by-line differences
- Analyzes what changed (added/removed functions, DOM changes, API changes)
- Compares specific functions

**When to use:**
- After making changes to verify what changed
- When debugging to see what broke
- To understand evolution of code

### 3. `ai_pattern_matcher.py`
**Purpose**: Finds code patterns and suggests improvements

**Usage:**
```bash
python ai_pattern_matcher.py "Guru Manager.html"
```

**What it does:**
- Finds good patterns (async/await, error handling, const usage)
- Detects anti-patterns (var usage, missing error handling, eval)
- Identifies code smells (long functions, deep nesting, magic numbers)
- Suggests improvements

**When to use:**
- Before refactoring to identify issues
- When reviewing code quality
- To find areas for improvement

### 4. `ai_context_builder.py`
**Purpose**: Builds context about codebase relationships

**Usage:**
```bash
# Full context report
python ai_context_builder.py "Guru Manager.html"

# Context for specific function
python ai_context_builder.py "Guru Manager.html" "initFileSystem"
```

**What it does:**
- Extracts function signatures and parameters
- Builds dependency graph (what calls what)
- Finds related functions (calls, called by, uses same DOM)
- Identifies critical functions

**When to use:**
- Before modifying a function to understand dependencies
- When adding new features to see what's related
- To understand code flow

### 5. `backup_file.py`
**Purpose**: Creates timestamped backups

**Usage:**
```bash
python backup_file.py "Guru Manager.html"  # Create backup
python backup_file.py list "Guru Manager"  # List backups
python backup_file.py restore "backup/..." # Restore
```

### 6. `load_coding_reference.py`
**Purpose**: Searches coding reference databases

**Usage:**
```bash
python load_coding_reference.py js "file system"
python load_coding_reference.py python "metadata"
python load_coding_reference.py html5 "context menu"
```

### 7. `test_guru_manager.py`
**Purpose**: Validates code before changes

**Usage:**
```bash
python test_guru_manager.py
```

## Workflow Integration

### Before Making Changes

1. **Create backup**
   ```bash
   python backup_file.py "Guru Manager.html"
   ```

2. **Analyze current code**
   ```bash
   python ai_code_analyzer.py "Guru Manager.html" > analysis.json
   python ai_context_builder.py "Guru Manager.html" > context.json
   ```

3. **Check references**
   ```bash
   python load_coding_reference.py js "file system"
   ```

4. **Run tests**
   ```bash
   python test_guru_manager.py
   ```

### During Development

1. **Check patterns**
   ```bash
   python ai_pattern_matcher.py "Guru Manager.html"
   ```

2. **Understand function context**
   ```bash
   python ai_context_builder.py "Guru Manager.html" "functionName"
   ```

### After Making Changes

1. **Compare changes**
   ```bash
   python ai_code_diff.py "backup/Guru Manager_20251219_130722.html" "Guru Manager.html"
   ```

2. **Run tests**
   ```bash
   python test_guru_manager.py
   ```

3. **Check for issues**
   ```bash
   python ai_pattern_matcher.py "Guru Manager.html"
   ```

## Tool Capabilities

### Code Understanding
- Function extraction and analysis
- Dependency mapping
- Context building
- Pattern recognition

### Quality Assurance
- Pattern matching (good vs bad)
- Code smell detection
- Complexity analysis
- Suggestion generation

### Change Tracking
- Before/after comparison
- Function-level diffs
- Change analysis
- Impact assessment

### Reference Lookup
- API patterns
- Best practices
- Common pitfalls
- Code examples

## Integration with AI Workflow

These tools are designed to:
1. **Reduce errors** - Understand code before changing it
2. **Improve quality** - Detect issues and suggest improvements
3. **Track changes** - Compare before/after to verify modifications
4. **Build context** - Understand relationships between functions
5. **Reference patterns** - Use proven patterns from reference databases

## Best Practices

1. **Always backup** before changes
2. **Analyze first** to understand structure
3. **Check references** for correct API usage
4. **Test after** to verify changes work
5. **Compare diffs** to understand what changed
6. **Update docs** with new learnings
