# AI Assistant Coding Rules & Workflow

> **Note**: This file combines rules from:
> - `docs/AI_CODING_RULES.md` (this file - main rules)
> - `.cursor/coding_guru.md` (detailed patterns and learnings)
> - `.cursor/commands/rules.md` (ComfyUI-specific rules)
> - `.cursor/spec.md` (project specification)
>
> **Always check INDEX.md** to find all relevant documentation files.

## ⚠️ MANDATORY REQUIREMENTS

**Before ANY coding task:**
1. **🔍 RESEARCH FIRST** - Always search internet for best practices, solutions, and patterns
2. **🛠️ USE TOOLS** - Always use available tools for analysis, testing, and validation
3. **✅ VALIDATE** - Always test and verify with tools before and after changes

**These are NOT optional - they are REQUIRED for every task.**

## Quick Reference

### Before Making ANY Changes

1. **Research First** - Search internet for best practices, solutions, and patterns
2. **Use Tools** - Run analysis and test tools to understand current state
3. **Create Backup** - **MANDATORY**: Create timestamped backup before ANY file edit
   - Format: `{filename}_{YYYYMMDD}_{HHMMSS}.{ext}` in `backup/` directory
   - Maintain up to 10 revisions per file (delete older backups)
   - Use: `python tools/backup_file.py <filename>` or create manual backup
   - **Alternative**: Fetch originals from GitHub: https://github.com/revisionhiep-create/comfyui-history-guru
4. **Consult References** - Check coding_reference_*.json files
5. **Run Tests** - Ensure current code passes tests
6. **Plan Changes** - Know what you're modifying

### During Development

- **Use Tools** - Run analysis tools before and during coding
- Check references every 3-5 function implementations
- Test after each significant change using test tools
- Create backups before major refactoring
- Validate syntax and structure with test tools

### After Development

- **Run All Tests** - Use test tools to validate changes
- **Verify with Tools** - Run code analysis and validation tools
- Run automated tests before asking user to test
- Update coding_guru.md with new learnings
- **Maintain Backups** - Keep last 10 revisions per file (auto-delete older backups)
- **GitHub Reference** - Repository: https://github.com/revisionhiep-create/comfyui-history-guru

## Detailed Rules

### 0. Research & Internet Search (MANDATORY)

**Before starting ANY new feature or fix:**

1. **Search for Best Practices**
   - Search internet for current best practices (2024-2025 standards)
   - Look for similar implementations
   - Check for known issues and solutions
   - Review recent updates to APIs/libraries
   - Check GitHub for existing implementations
   - Review official documentation

2. **Search for Solutions**
   - If fixing a bug, search for similar issues
   - Look for documented solutions
   - Check Stack Overflow, MDN, GitHub issues
   - Review official documentation
   - Search for error messages

3. **Search for Patterns**
   - Find proven patterns for the feature
   - Look for performance optimizations
   - Check security best practices
   - Review accessibility guidelines
   - Find modern approaches (2024-2025)

**When to search:**
- ✅ Before implementing a new feature
- ✅ Before fixing a bug
- ✅ Before refactoring code
- ✅ When encountering an unfamiliar API
- ✅ When performance issues arise
- ✅ When security concerns exist
- ✅ When user reports an issue

**Search examples:**
- "JavaScript IndexedDB best practices 2024"
- "Firefox file input API limitations"
- "Virtual scrolling performance optimization"
- "Object URL memory leak prevention"
- "ComfyUI custom node patterns 2025"
- "Python async file monitoring best practices"

### 1. Tool Usage (MANDATORY)

**Always use tools for:**
- Code analysis and understanding
- Testing and validation
- Pattern detection
- Context building
- Reference lookup
- Change verification

**Available Tools:**

#### Analysis & Understanding Tools
1. **ai_code_analyzer.py** - Analyze code structure, dependencies, complexity
2. **ai_context_builder.py** - Build dependency graphs and context
3. **ai_pattern_matcher.py** - Find patterns, anti-patterns, code smells
4. **ai_code_diff.py** - Compare before/after changes

#### Testing & Validation Tools
5. **test_guru_manager.py** - Validate HTML/JS syntax, functions, DOM
6. **test_firefox_version.py** - Test Firefox-specific features
7. **test_list_view_features.py** - Test specific feature implementations

#### Reference & Backup Tools
8. **load_coding_reference.py** - Search coding reference databases
9. **backup_file.py** - Create/restore backups
10. **coding_reference_js.json** - JavaScript patterns
11. **coding_reference_python.json** - Python patterns
12. **coding_reference_html5.json** - HTML5 patterns

**Tool Usage Workflow:**
```bash
# Before changes
python tools/backup_file.py "filename.html"
python tools/ai_code_analyzer.py "filename.html"
python tools/ai_context_builder.py "filename.html" "functionName"
python tools/test_guru_manager.py "filename.html"

# During development
python tools/ai_pattern_matcher.py "filename.html"
python tools/load_coding_reference.py js "feature_name"

# After changes
python tools/test_guru_manager.py "filename.html"
python tools/ai_code_diff.py "backup/file.html" "filename.html"
python tools/ai_pattern_matcher.py "filename.html"
```

**Tool Usage Rules:**
- ✅ **MANDATORY**: Run tests before making changes
- ✅ **MANDATORY**: Run tests after making changes
- ✅ **MANDATORY**: Use analysis tools to understand code structure
- ✅ **MANDATORY**: Use reference tools before implementing features
- ✅ **MANDATORY**: Use diff tools to verify changes
- ✅ **MANDATORY**: Use pattern matcher to find issues

### 2. Coding Reference Usage

**When to check references:**

| What You're Doing | Which Reference | How Often |
|-------------------|----------------|-----------|
| File operations | `coding_reference_js.json` → `file_system_access_api` | **Every time** |
| Database operations | `coding_reference_js.json` → `indexeddb` | **Every time** |
| Context menus | `coding_reference_html5.json` → `context_menus` | **Every time** |
| Drag & drop | `coding_reference_html5.json` → `drag_and_drop` | **Every time** |
| Keyboard events | `coding_reference_html5.json` → `keyboard_events` | **Every time** |
| Python file ops | `coding_reference_python.json` → `file_operations` | **Every time** |
| Image metadata | `coding_reference_python.json` → `image_metadata` | **Every time** |
| DOM manipulation | `coding_reference_js.json` → `dom_manipulation` | Every 3-5 uses |

**How to use:**
```bash
# Search for patterns
python tools/load_coding_reference.py js "file system"
python tools/load_coding_reference.py python "metadata"
python tools/load_coding_reference.py html5 "context menu"
```

**Why this matters:**
- Prevents errors from incorrect API usage
- Ensures consistent patterns
- Saves debugging time
- Reduces user frustration

### 3. Backup System

**MANDATORY: Always backup before changes**

**GitHub Repository:** https://github.com/revisionhiep-create/comfyui-history-guru
- Use GitHub to restore originals if backups unavailable
- Check repository for latest versions before making changes
- Reference repository for project structure and file locations

**Commands:**
```bash
# Create backup
python tools/backup_file.py "Guru Manager.html"

# List backups
python tools/backup_file.py list "Guru Manager"

# Restore backup
python tools/backup_file.py restore "backup/Guru Manager_20251219_125740.html"
```

**Backup naming:**
- Format: `FILENAME_YYYYMMDD_HHMMSS.ext`
- Example: `Guru Manager_20251219_125740.html`
- Includes timestamp for chronological sorting

**When to backup:**
- ✅ Before editing any file
- ✅ Before adding new features
- ✅ Before fixing bugs
- ✅ Before refactoring code
- ✅ Before testing changes

**Backup management:**
- **Maintain up to 10 revisions per file** (delete older backups)
- Keep only the 10 most recent backups for each file
- Always keep at least one "known good" backup
- Use backups to compare before/after

**Restoration options:**
1. **From backup files** - Use timestamped backups in `backup/` directory
2. **From GitHub** - Fetch originals from repository: https://github.com/revisionhiep-create/comfyui-history-guru
3. **Manual restore** - Copy backup file back to original location

**Why this matters:**
- Can restore if changes break functionality
- Can compare what changed
- Can understand what worked before
- Reduces risk of losing working code
- Easy rollback to previous working versions

### 4. Documentation Updates (coding_guru.md)

**Update immediately when you learn:**
- API limitations or quirks
- Security issues
- Breaking changes
- Critical bugs and fixes

**Update after feature completion:**
- New patterns that worked well
- Performance optimizations
- Better approaches discovered
- User feedback incorporated

**Update at end of session:**
- Summarize key learnings
- Document what worked
- Note what didn't work and why
- Update patterns section

**What to document:**
- ✅ What you learned (the knowledge)
- ✅ Why it matters (the problem it solves)
- ✅ Code examples (show the pattern)
- ✅ Common pitfalls (what to avoid)
- ✅ Best practices (recommended approach)

**Documentation format:**
```markdown
## [Feature/Pattern Name] (YYYY-MM-DD)

### What I Learned
[Clear description]

### Why It Matters
[Explanation]

### Code Pattern
```language
[Working example]
```

### Common Pitfalls
- [Pitfall 1]
- [Pitfall 2]

### Best Practice
[Recommended approach]
```

**Why this matters:**
- Future you will thank you
- Prevents repeating mistakes
- Shares knowledge with others
- Creates institutional memory

## Workflow Checklist

### Pre-Development
- [ ] **🔍 Search internet for best practices and solutions**
- [ ] **🛠️ Run analysis tools** (`ai_code_analyzer.py`, `ai_context_builder.py`)
- [ ] **✅ Run test tools** (`test_guru_manager.py` or feature-specific tests)
- [ ] **💾 Create backup** (`backup_file.py`)
- [ ] **📚 Consult coding references** (`load_coding_reference.py`)
- [ ] **🔍 Review existing code** with tools
- [ ] **📋 Plan the change**
- [ ] **✅ Verify current code passes tests**

### During Development
- [ ] **🛠️ Use tools for validation** (pattern matcher, syntax checker)
- [ ] **📚 Check references** every 3-5 functions
- [ ] **✏️ Make small, testable changes**
- [ ] **✅ Test after each change** (run test tools)
- [ ] **💾 Create backups** before major refactoring
- [ ] **🔍 Use diff tool** to verify changes

### Post-Development
- [ ] **✅ Run all test tools** (syntax, function, feature tests)
- [ ] **🛠️ Run code analysis tools** (pattern matcher, analyzer)
- [ ] **🔍 Use diff tool** to review changes
- [ ] **🐛 Fix any test failures**
- [ ] **📝 Update coding_guru.md**
- [ ] **📝 Document learnings**
- [ ] **💾 Keep recent backups**

## Success Metrics

**Good development session:**
- ✅ **Searched internet for best practices**
- ✅ **Used tools for analysis and testing**
- ✅ Created backups before changes
- ✅ Consulted references when needed
- ✅ All tests pass (verified with tools)
- ✅ Code validated with analysis tools
- ✅ User doesn't report bugs
- ✅ Updated documentation

**Bad development session:**
- ❌ **No internet research done**
- ❌ **Didn't use available tools**
- ❌ No backups created
- ❌ Didn't check references
- ❌ Tests fail (or not run)
- ❌ User reports broken features
- ❌ No documentation updates

## Mandatory Tool Usage Examples

### Example 1: Adding a New Feature
```bash
# 1. Research (MANDATORY)
# Search: "JavaScript feature implementation best practices 2024"

# 2. Analyze current code (MANDATORY)
python tools/ai_code_analyzer.py "Guru Manager.html"
python tools/ai_context_builder.py "Guru Manager.html" "relatedFunction"

# 3. Check references (MANDATORY)
python tools/load_coding_reference.py js "feature_name"

# 4. Test current state (MANDATORY)
python tools/test_guru_manager.py "Guru Manager.html"

# 5. Backup (MANDATORY)
python tools/backup_file.py "Guru Manager.html"

# 6. Implement changes

# 7. Test (MANDATORY)
python tools/test_guru_manager.py "Guru Manager.html"
python tools/ai_pattern_matcher.py "Guru Manager.html"

# 8. Verify changes (MANDATORY)
python tools/ai_code_diff.py "backup/file.html" "Guru Manager.html"
```

### Example 2: Fixing a Bug
```bash
# 1. Research (MANDATORY)
# Search: "JavaScript bug type solutions 2024"

# 2. Analyze (MANDATORY)
python tools/ai_code_analyzer.py "file.html"
python tools/ai_pattern_matcher.py "file.html"

# 3. Test current state (MANDATORY)
python tools/test_guru_manager.py "file.html"

# 4. Backup (MANDATORY)
python tools/backup_file.py "file.html"

# 5. Fix bug

# 6. Test (MANDATORY)
python tools/test_guru_manager.py "file.html"
python tools/ai_code_diff.py "backup/file.html" "file.html"
```

### Example 3: Understanding Code
```bash
# Always use tools to understand code before modifying (MANDATORY)
python tools/ai_code_analyzer.py "file.html"
python tools/ai_context_builder.py "file.html" "functionName"
python tools/load_coding_reference.py js "api_name"
```

## Project-Specific Rules

### For Guru Manager (HTML/JavaScript)

**Key APIs:**
- File System Access API (Chrome/Edge)
- File Input API (Firefox)
- IndexedDB for caching
- localStorage for preferences

**Testing:**
- Always test both Chrome and Firefox versions
- Use `test_guru_manager.py` for syntax validation
- Use `test_firefox_version.py` for Firefox-specific features
- Use `test_list_view_features.py` for feature validation

**Common Patterns:**
- Use Maps for O(1) lookups
- Use Sets for unique collections
- Virtual scrolling for large lists
- Object URL caching for images
- Debounced scroll events

**File System Access API Limitations (Critical):**
- **Rename Not Supported**: Direct renaming of directories is not possible
- **Cut/Paste Complexity**: Use drag-and-drop instead
- **Delete Works Reliably**: `removeEntry()` works well for both files and directories

### For ComfyUI Custom Nodes (Python/JavaScript)

**Python Standards:**
- Methods must return a `tuple`, e.g., `return (output_value,)`
- Use `INPUT_TYPES(s)` class methods strictly
- Follow the `NODE_CLASS_MAPPINGS` registry pattern in `__init__.py`
- Prohibit `eval()` or `exec()` for security
- Use type hints extensively
- Implement proper async patterns
- Use `pathlib` over `os.path` for file operations
- Use dataclasses for configuration objects

**JavaScript Standards:**
- Use `app.registerExtension` for UI modifications
- Ensure compatibility with `LiteGraph` system
- Use ES6+ syntax, avoid deprecated callbacks
- Use functional programming patterns
- Implement proper error boundaries
- Use event delegation for dynamic elements
- Clean up event listeners to prevent memory leaks

**Research Requirements (MANDATORY):**
- Search GitHub for existing ComfyUI node implementations
- Search ComfyUI Official Docs for recent API changes (2025 standards)
- Verify JS/Python best practices for 2025
- Check specialized libraries (torch, numpy, PIL) usage efficiency

**ComfyUI Integration:**
- Use ComfyUI's built-in web server (`server.PromptServer.instance.app.router.add_static()`)
- Register custom settings in ComfyUI's gear menu
- Access settings through server integration
- Use `/view` endpoint for image serving

## Tool Usage Requirements Summary

**MANDATORY for every task:**
1. **🔍 Research** - Internet search before starting (MANDATORY)
2. **🛠️ Analyze** - Use analysis tools to understand code (MANDATORY)
3. **✅ Test** - Run tests before and after changes (MANDATORY)
4. **💾 Backup** - Create backups before changes (MANDATORY)
5. **📚 Reference** - Check coding references (MANDATORY)
6. **🔍 Validate** - Use tools to verify changes (MANDATORY)
7. **📝 Document** - Update coding_guru.md with learnings (MANDATORY)

**These are NOT optional - they are REQUIRED for every coding task.**

## Additional Resources

### Reference Files Location
- **Coding References**: `data/coding_reference_*.json`
- **Knowledge Base**: `.cursor/coding_guru.md`
- **Project Spec**: `.cursor/spec.md`
- **ComfyUI Rules**: `.cursor/commands/rules.md`
- **Tools Documentation**: `docs/AI_TOOLS_README.md`

### Quick Tool Reference
```bash
# Analysis
python tools/ai_code_analyzer.py "file.html"
python tools/ai_context_builder.py "file.html" "function"
python tools/ai_pattern_matcher.py "file.html"

# Testing
python tools/test_guru_manager.py "file.html"
python tools/test_firefox_version.py
python tools/test_list_view_features.py

# References
python tools/load_coding_reference.py js "query"
python tools/load_coding_reference.py python "query"
python tools/load_coding_reference.py html5 "query"

# Backup
python tools/backup_file.py "file.html"
python tools/backup_file.py list "filename"
python tools/backup_file.py restore "backup/file.html"

# Diff
python tools/ai_code_diff.py "backup/file.html" "file.html"
```

---

**Remember: Research → Tools → Backup → Code → Test → Validate → Document**

**Every. Single. Time.**
