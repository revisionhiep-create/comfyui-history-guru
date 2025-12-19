# Installation Guide

## Prerequisites

- ComfyUI installed and working
- Python 3.8 or higher
- Git (for cloning the repository)

## Installation Methods

### Method 1: ComfyUI Manager (Easiest - When Available)

1. Open ComfyUI
2. Open ComfyUI Manager (if installed)
3. Search for "Prompt Library"
4. Click Install
5. Restart ComfyUI

### Method 2: Git Clone (Recommended)

1. Open a terminal/command prompt

2. Navigate to your ComfyUI custom nodes directory:
   ```bash
   cd path/to/ComfyUI/custom_nodes
   ```

3. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/comfyui-prompt-library.git
   ```

4. Install Python dependencies:
   ```bash
   cd comfyui-prompt-library
   pip install -r requirements.txt
   ```

5. Restart ComfyUI

### Method 3: Manual Download

1. Download the repository as a ZIP file from GitHub

2. Extract the ZIP file

3. Copy the `comfyui-prompt-library` folder to your ComfyUI's `custom_nodes` directory:
   ```
   ComfyUI/custom_nodes/comfyui-prompt-library/
   ```

4. Install dependencies:
   ```bash
   cd ComfyUI/custom_nodes/comfyui-prompt-library
   pip install -r requirements.txt
   ```

5. Restart ComfyUI

## Verifying Installation

1. Start ComfyUI

2. Check the console output for:
   ```
   [Prompt Library] Database initialized at: ...
   [Prompt Library] API routes registered
   [Prompt Library] Extension loaded successfully!
   ```

3. In the ComfyUI interface:
   - Right-click to open the node menu
   - Look for "📚 Prompt Library" under the "📚 Prompt Library" category
   - You should be able to add it to your workflow

## Troubleshooting Installation

### Error: "No module named 'PIL'"

Install Pillow:
```bash
pip install Pillow
```

### Error: "No module named 'aiohttp'"

This is usually installed with ComfyUI, but if needed:
```bash
pip install aiohttp
```

### Error: "Node not found" or "Extension not loading"

1. Check that the folder structure is correct:
   ```
   ComfyUI/custom_nodes/comfyui-prompt-library/
   ├── __init__.py
   ├── prompt_library.py
   ├── py/
   ├── js/
   └── ...
   ```

2. Check ComfyUI console for error messages

3. Try restarting ComfyUI completely

### Database Permission Errors

Ensure ComfyUI has write permissions to the output directory:
```
ComfyUI/output/Prompt History/
```

### Python Version Issues

This extension requires Python 3.8+. Check your version:
```bash
python --version
```

## Updating

### If installed via Git:

```bash
cd ComfyUI/custom_nodes/comfyui-prompt-library
git pull
pip install -r requirements.txt --upgrade
```

Then restart ComfyUI.

### If installed manually:

1. Delete the old `comfyui-prompt-library` folder
2. Download the latest version
3. Extract to `custom_nodes/`
4. Reinstall dependencies if needed

## Uninstallation

1. Stop ComfyUI

2. Delete the extension folder:
   ```bash
   rm -rf ComfyUI/custom_nodes/comfyui-prompt-library
   ```

3. Optional: Delete the data folder:
   ```bash
   rm -rf ComfyUI/output/Prompt\ History
   ```

4. Restart ComfyUI

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting section](README.md#-troubleshooting) in the README
2. Look for existing [GitHub Issues](https://github.com/yourusername/comfyui-prompt-library/issues)
3. Create a new issue with:
   - Your ComfyUI version
   - Your Python version
   - Error messages from the console
   - Steps to reproduce the problem
