# Standard Trigger Words Loader - Installation Guide

## Quick Installation

### For ComfyUI Users

1. **Navigate to custom_nodes folder:**
   ```bash
   cd ComfyUI/custom_nodes/
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Standard_trigger_words_loader.git
   ```

3. **Restart ComfyUI**
   - Close and reopen ComfyUI
   - The node will appear automatically

4. **Find the node:**
   - Search for: `Standard Trigger Words` or `📝`
   - Located in category: `trigger_words`

## Verification

After installation, verify it works:

1. Open ComfyUI
2. Right-click on canvas → Add Node → Search "Standard Trigger"
3. Node should appear with name: **Standard Trigger Words 📝**
4. Add node to workflow
5. Select a category (e.g., "Quality")
6. Tags should appear in the widget

## Manual Installation

If you prefer to download manually:

1. Download ZIP from GitHub
2. Extract to `ComfyUI/custom_nodes/Standard_trigger_words_loader/`
3. Ensure folder structure:
   ```
   ComfyUI/
   └── custom_nodes/
       └── Standard_trigger_words_loader/
           ├── __init__.py
           ├── standard_trigger_node.py
           ├── standard_trigger_presets.py
           ├── js/
           │   └── standard_trigger_loader.js
           └── README.md
   ```
4. Restart ComfyUI

## Troubleshooting

### Node Not Appearing

**Issue**: Can't find node in search
**Solution**: 
- Restart ComfyUI completely
- Check console for error messages
- Verify files are in correct location

### Import Errors

**Issue**: Python import errors in console
**Solution**:
- Ensure Python 3.8+ is installed
- Check file permissions
- Verify `__init__.py` exists

### JavaScript Not Loading

**Issue**: Node appears but UI is broken
**Solution**:
- Clear browser cache (Ctrl+Shift+R)
- Check browser console for errors
- Verify `js/standard_trigger_loader.js` exists

### Tags Not Loading

**Issue**: Node works but no presets appear
**Solution**:
- Check `standard_trigger_presets.py` is present
- Select different category from dropdown
- Click "Toggle All ON" button

## Updating

To update to the latest version:

```bash
cd ComfyUI/custom_nodes/Standard_trigger_words_loader/
git pull origin main
```

Then restart ComfyUI.

## Uninstalling

To remove the node:

1. Delete the folder:
   ```bash
   rm -rf ComfyUI/custom_nodes/Standard_trigger_words_loader/
   ```

2. Restart ComfyUI

## Support

If you encounter issues:
- Check [README.md](README.md) troubleshooting section
- Open issue on GitHub
- Include error messages from console

## Next Steps

After installation:
1. Read the [README.md](README.md) for full documentation
2. Try the examples in the README
3. Customize presets in `standard_trigger_presets.py`
4. Share your workflows with the community!
