# AI Assistant Coding Rules & Workflow

## Quick Reference

### Before Making ANY Changes

1. **Create Backup** - `python backup_file.py <filename>`
2. **Consult References** - Check coding_reference_*.json files
3. **Run Tests** - Ensure current code passes tests
4. **Plan Changes** - Know what you're modifying

### During Development

- Check references every 3-5 function implementations
- Test after each significant change
- Create backups before major refactoring

### After Development

- Run automated tests before asking user to test
- Update coding_guru.md with new learnings
- Keep recent backups (last 10-20)

## Detailed Rules

### 1. Coding Reference Usage

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
python load_coding_reference.py js "file system"
python load_coding_reference.py python "metadata"
python load_coding_reference.py html5 "context menu"
```

**Why this matters:**
- Prevents errors from incorrect API usage
- Ensures consistent patterns
- Saves debugging time
- Reduces user frustration

### 2. Backup System

**MANDATORY: Always backup before changes**

**Commands:**
```bash
# Create backup
python backup_file.py "Guru Manager.html"

# List backups
python backup_file.py list "Guru Manager"

# Restore backup
python backup_file.py restore "backup/Guru Manager_20251219_125740.html"
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
- Keep last 10-20 backups
- Remove backups older than 30 days
- Always keep at least one "known good" backup
- Use backups to compare before/after

**Why this matters:**
- Can restore if changes break functionality
- Can compare what changed
- Can understand what worked before
- Reduces risk of losing working code

### 3. Documentation Updates (coding_guru.md)

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
- [ ] Create backup
- [ ] Consult coding references
- [ ] Review existing code
- [ ] Plan the change
- [ ] Run tests on current code

### During Development
- [ ] Check references every 3-5 functions
- [ ] Make small, testable changes
- [ ] Test after each change
- [ ] Create backups before major refactoring

### Post-Development
- [ ] Run automated tests
- [ ] Fix any test failures
- [ ] Update coding_guru.md
- [ ] Document learnings
- [ ] Keep recent backups

## Tools Available

1. **backup_file.py** - Create/restore backups
2. **load_coding_reference.py** - Search coding references
3. **test_guru_manager.py** - Validate code before changes
4. **coding_reference_js.json** - JavaScript patterns
5. **coding_reference_python.json** - Python patterns
6. **coding_reference_html5.json** - HTML5 patterns

## Success Metrics

**Good development session:**
- ✅ Created backups before changes
- ✅ Consulted references when needed
- ✅ All tests pass
- ✅ User doesn't report bugs
- ✅ Updated documentation

**Bad development session:**
- ❌ No backups created
- ❌ Didn't check references
- ❌ Tests fail
- ❌ User reports broken features
- ❌ No documentation updates
