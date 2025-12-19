# 📁 Project Index

Quick reference guide to find everything in this project.

## 🚀 Applications (Main HTML Files)

**Location:** `apps/`

| File | Description | Browser Support |
|------|-------------|-----------------|
| `Guru Manager.html` | **Main application** - Full-featured file manager with File System Access API | Chrome, Edge, Opera |
| `Guru Universal Node Version 3.3.html` | **Firefox version** - Same features, works without File System Access API | Firefox, Chrome, Edge, Opera |
| `Guru Manager Original Code.html` | Original working version (reference/backup) | Chrome, Edge, Opera |
| `index.html` | Legacy/alternative entry point | All browsers |
| `test_guru_manager.html` | Testing/debugging tool for HTML validation | All browsers |

**Quick Start:**
- **Chrome/Edge users:** Use `apps/Guru Manager.html`
- **Firefox users:** Use `apps/Guru Universal Node Version 3.3.html`

---

## 🛠️ AI Development Tools

**Location:** `tools/`

| File | Purpose |
|------|---------|
| `test_guru_manager.py` | Validates HTML syntax, function definitions, DOM access |
| `backup_file.py` | Creates timestamped backups before changes |
| `ai_code_analyzer.py` | Analyzes code structure, dependencies, complexity |
| `ai_code_diff.py` | Compares code before/after changes |
| `ai_pattern_matcher.py` | Finds coding patterns and suggests improvements |
| `ai_context_builder.py` | Builds codebase context and dependency graphs |
| `load_coding_reference.py` | Loads and searches coding reference databases |
| `analyze_civitai_metadata.py` | Analyzes Civitai image metadata formats |
| `analyze_guru_manager.py` | Analyzes Guru Manager codebase structure |
| `detailed_metadata_check.py` | Detailed metadata extraction analysis |

**Usage:** Run with `python tools/<filename>.py`

---

## 📚 Documentation

**Location:** `docs/`

| File | Content |
|------|---------|
| `Readme.md` | **Main README** - Project overview, features, quick start |
| `AI_CODING_RULES.md` | Rules for AI assistant coding workflow |
| `AI_TOOLS_README.md` | Documentation for all AI development tools |
| `IMPROVEMENTS_SUMMARY.md` | Summary of all improvements made to Guru Manager |
| `GEMINI.md` | Gemini-specific notes/documentation |
| `prompt.md` | Prompt templates/notes |

**Note:** `Readme.md` stays in root for GitHub visibility.

---

## 💾 Data & References

**Location:** `data/`

| File | Purpose |
|------|---------|
| `coding_reference_js.json` | JavaScript API patterns and examples |
| `coding_reference_python.json` | Python patterns and examples |
| `coding_reference_html5.json` | HTML5 features and patterns |
| `civitai_metadata_analysis.json` | Analysis results of Civitai metadata formats |
| `detailed_metadata_report.json` | Detailed metadata extraction report |
| `guru_manager_analysis_report.json` | Codebase analysis results |

**Usage:** These are reference databases used by AI tools for better coding assistance.

---

## 🧪 Test Data

**Location:** `test-data/`

| Folder | Contents |
|--------|----------|
| `Comfyui/` | Test images with various metadata formats (ComfyUI, Civitai, A1111) |

---

## 📦 Other Folders

| Folder | Purpose |
|--------|---------|
| `backup/` | Automatic backups of HTML files before changes |
| `Archive/` | Archived projects and code |
| `.cursor/` | Cursor IDE configuration and rules |
| `my-project/` | Project templates and agent configurations |

---

## 🔍 Quick Find

**Looking for:**
- **Main app?** → `apps/Guru Manager.html`
- **Firefox version?** → `apps/Guru Universal Node Version 3.3.html`
- **Documentation?** → `docs/` or root `Readme.md`
- **Quick start?** → `README_QUICK_START.md`
- **File index?** → `INDEX.md` (this file)
- **AI tools?** → `tools/`
- **Coding references?** → `data/coding_reference_*.json`
- **Backups?** → `backup/`
- **Test images?** → `test-data/Comfyui/`

---

## 📋 File Categories Summary

```
art/
├── apps/                    # Main applications (HTML files)
├── tools/                   # AI development tools (Python scripts)
├── docs/                    # Documentation (Markdown files)
├── data/                    # Reference data (JSON files)
├── test-data/               # Test images and samples
├── backup/                  # Automatic backups
├── Archive/                 # Archived projects
├── .cursor/                 # IDE configuration
├── my-project/              # Project templates
├── Readme.md                # Main README (stays in root)
├── README_QUICK_START.md    # Quick start guide
└── INDEX.md                 # This file (file index)
```

---

**Last Updated:** 2025-12-19  
**Maintained by:** AI Assistant

---

## 🔄 Migration Notes

If you have scripts or references to old file locations:

| Old Location | New Location |
|-------------|--------------|
| `Guru Manager.html` | `apps/Guru Manager.html` |
| `Guru Universal Node Version 3.3.html` | `apps/Guru Universal Node Version 3.3.html` |
| `Guru Manager Original Code.html` | `apps/Guru Manager Original Code.html` |
| `*.py` files | `tools/` |
| `*.md` files (except Readme.md) | `docs/` |
| `*.json` files | `data/` |
| `Comfyui/` | `test-data/Comfyui/` |

**Updated Scripts:**
- `tools/backup_file.py` - Now works from tools/ or root directory
- `tools/test_guru_manager.py` - Auto-detects apps/ folder
- `tools/analyze_guru_manager.py` - Updated to look in apps/ folder

**Usage Examples:**
```bash
# From root directory:
python tools/backup_file.py "apps/Guru Manager.html"
python tools/test_guru_manager.py "apps/Guru Manager.html"

# Or from tools directory:
cd tools
python backup_file.py "../apps/Guru Manager.html"
python test_guru_manager.py "../apps/Guru Manager.html"
```
