# Modify String Node - Quick Start

## What is it?

An advanced trigger word management node for ComfyUI with 50+ built-in SDXL Illustrious presets, editable tags, toggle on/off functionality, and Lora integration.

## Quick Start

### 1. Add Node
Search for **"Modify String (LoraManager)"** in ComfyUI

### 2. Load Presets
Select a category from dropdown:
- **Quality** - masterpiece, best quality, 8K, etc.
- **Lighting** - volumetric lighting, cinematic lighting, etc.
- **Composition** - dynamic angle, portrait, etc.
- **Style** - anime illustration, detailed, etc.
- **Detail** - detailed eyes, intricate details, etc.
- **Aesthetic** - vivid colors, atmospheric, etc.
- **Motion** - dynamic movement, wind, etc.
- **All** - Load all categories

### 3. Toggle Tags
- **Green** = Active (included in output)
- **Gray** = Inactive (excluded from output)
- Click to toggle

### 4. Connect Output
Connect **output_string** to your CLIP Text Encode positive prompt

## Example Usage

```
Input: "a beautiful anime girl"
Preset: Quality (active: masterpiece, best quality, 8K)
Mode: Append
Output: "a beautiful anime girl, masterpiece, best quality, 8K"
```

## Key Features

- ✅ **50+ SDXL Illustrious Presets** - Research-backed quality tags
- ✅ **Toggle On/Off** - Click any tag to enable/disable
- ✅ **Inline Editing** - Double-click to edit tag text
- ✅ **Strength Control** - Mouse wheel to adjust (tag:1.2)
- ✅ **Lora Integration** - Auto-receive tags from Lora Loader
- ✅ **Batch Operations** - Toggle all, clear all buttons
- ✅ **4 Modes** - Append, Prepend, Replace, Tagged Only
- ✅ **Smart Merging** - Handle duplicate tags intelligently

## Connect with Lora Loader

```
Lora Loader → trigger_words → Modify String → output_string → Prompt
```

Lora trigger words automatically merge with your presets!

## Parameters Explained

| Parameter | Description | Default |
|-----------|-------------|---------|
| **preset_category** | Category to load | All |
| **mode** | How to combine tags | Append |
| **separator** | Between tags | ", " |
| **merge_strategy** | Handle Lora duplicates | Keep Both |
| **deduplicate** | Remove duplicates | True |
| **default_active** | New tags start active | True |
| **allow_strength_adjustment** | Enable (tag:strength) | False |

## Modes

- **Append**: input + tags → `"girl, masterpiece, 8K"`
- **Prepend**: tags + input → `"masterpiece, 8K, girl"`
- **Replace**: tags only → `"masterpiece, 8K"`
- **Tagged Only**: same as Replace

## Tips

💡 **Start with Quality category** - Essential for good results
💡 **Toggle unwanted tags off** - Don't delete, just deactivate
💡 **Use strength 1.0-1.3** - For emphasized tags
💡 **Enable deduplication** - Cleaner prompts
💡 **Save presets with workflow** - Tag states persist

## Full Documentation

See [MODIFY_STRING_NODE.md](docs/MODIFY_STRING_NODE.md) for:
- Complete preset list
- Advanced usage
- Workflow examples
- API documentation
- Troubleshooting

## Files Created

```
comfyui-lora-manager/
├── py/nodes/
│   ├── modify_string.py              # Main node logic
│   └── modify_string_presets.py      # 50+ preset tags
├── web/comfyui/
│   └── modify_string.js              # Frontend UI
├── tests/nodes/
│   └── test_modify_string.py         # Unit tests
└── docs/
    └── MODIFY_STRING_NODE.md         # Full documentation
```

## Testing

To run tests:
```bash
cd comfyui-lora-manager
pip install -r requirements-dev.txt
pytest tests/nodes/test_modify_string.py -v
```

## Performance

- Optimized O(N+M) tag merging (handles 500+ tags efficiently)
- Pre-compiled regex patterns
- Singleton event listeners (no memory leaks)
- Efficient string building

## Version

**v1.0.0** - Initial release with full feature set

---

**Created**: December 2024  
**Optimized for**: SDXL Illustrious models  
**Compatible with**: ComfyUI + Lora Manager extension
