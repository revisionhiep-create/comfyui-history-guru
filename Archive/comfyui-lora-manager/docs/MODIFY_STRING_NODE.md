# Modify String Node - Documentation

## Overview

The **Modify String** node is an advanced trigger word management system for ComfyUI that allows you to:
- Load preset trigger words organized by category (Quality, Lighting, Composition, Style, Detail, Aesthetic, Motion)
- Toggle trigger words on/off individually
- Edit trigger word text inline
- Adjust trigger word strength (optional)
- Merge trigger words from Lora Loader
- Combine trigger words with your input text in various modes

## Features

### ✨ Core Capabilities

1. **Preset Management**
   - 50+ built-in SDXL Illustrious trigger words
   - 7 categories: Quality, Lighting, Composition, Style, Detail, Aesthetic, Motion
   - One-click category loading

2. **Interactive Editing**
   - Toggle individual trigger words on/off
   - Inline text editing (double-click tags)
   - Strength adjustment with mouse wheel
   - Batch operations (toggle all on/off, clear all)

3. **Lora Integration**
   - Automatically receives trigger words from Lora Loader
   - Highlights Lora-provided trigger words
   - Intelligent merging strategies

4. **Flexible Output**
   - Append, Prepend, Replace, or Tagged Only modes
   - Custom separators
   - Automatic deduplication
   - Two outputs: full string and active triggers list

## Usage Guide

### Basic Setup

1. **Add the Node**: Search for "Modify String (LoraManager)" in ComfyUI's node menu
2. **Choose Preset Category**: Select from dropdown (All, Quality, Lighting, etc.)
3. **Configure Mode**: Choose how to combine with input text
   - **Append**: Add tags after input text
   - **Prepend**: Add tags before input text
   - **Replace**: Use only tags, ignore input
   - **Tagged Only**: Same as Replace

### Connecting to Lora Loader

```
Lora Loader → trigger_words output → Modify String → trigger_words input
```

The node will automatically:
- Receive trigger words from the Lora Loader
- Highlight them in the UI
- Merge them with your presets based on merge strategy

### Parameters

#### Required

- **preset_category**: Category to load (All, Quality, Lighting, Composition, Style, Detail, Aesthetic, Motion)
- **mode**: How to combine tags with input
  - Append: `input_text, tag1, tag2`
  - Prepend: `tag1, tag2, input_text`
  - Replace: `tag1, tag2` (ignores input)
  - Tagged Only: Same as Replace
- **separator**: String between tags (default: `", "`)
- **merge_strategy**: How to handle Lora duplicates
  - Keep Both: Show both preset and Lora versions
  - Prefer Preset: Keep preset, discard Lora duplicate
  - Prefer Incoming: Keep Lora, discard preset duplicate
- **deduplicate**: Remove duplicate tags (case-insensitive)
- **default_active**: Default state for new tags
- **allow_strength_adjustment**: Enable `(tag:strength)` formatting

#### Optional Inputs

- **input_string** (STRING): Text to combine with tags
- **trigger_words** (STRING): Connect from Lora Loader's trigger_words output

### UI Controls

#### Tags Widget
- **Click**: Toggle tag on/off
- **Double-click**: Edit tag text
- **Mouse wheel**: Adjust strength (if enabled)
- **Drag**: Reorder tags

#### Buttons
- **Load Presets**: Reload current category
- **Toggle All ON**: Activate all tags
- **Toggle All OFF**: Deactivate all tags
- **Clear All**: Remove all tags

## Examples

### Example 1: Basic Quality Tags

**Setup:**
- Preset Category: "Quality"
- Mode: "Append"
- Input: "a beautiful anime girl"

**Output:**
```
a beautiful anime girl, masterpiece, best quality, very aesthetic, absurdres, high quality
```

### Example 2: Lighting with Strength

**Setup:**
- Preset Category: "Lighting"
- Allow Strength Adjustment: True
- Adjust "volumetric lighting" to 1.3
- Mode: "Prepend"

**Output:**
```
(volumetric lighting:1.30), cinematic lighting, a cyberpunk cityscape
```

### Example 3: Lora Integration

**Workflow:**
```
Lora Loader (character lora) → trigger_words: "1girl, school uniform"
                              ↓
Modify String (preset: Quality) + merge with Lora tags
                              ↓
Output: "masterpiece, best quality, 1girl, school uniform, detailed eyes"
```

### Example 4: Tagged Only Mode

**Setup:**
- Mode: "Tagged Only"
- Select only: "masterpiece", "best quality", "8K"
- Input string: (ignored)

**Output:**
```
masterpiece, best quality, 8K
```

## Preset Categories

### Quality Tags (13 tags)
Essential quality modifiers for high-quality outputs:
- masterpiece, best quality, very aesthetic, absurdres, high quality, ultra high definition, extremely high detail, newest, year 2024, year 2025, highres, 8K, HDR

### Lighting Tags (14 tags)
Control lighting and atmosphere:
- volumetric lighting, ambient occlusion, dramatic lighting, cinematic lighting, rim light, soft lighting, studio lighting, golden hour lighting, natural lighting, sunlight, backlighting, sharp focus, glowing, luminescent background

### Composition Tags (17 tags)
Camera angles and framing:
- dynamic angle, dynamic pose, low-angle shot, low angle, looking at viewer, from above, from below, upper body focus, full body, portrait, close-up shot, mid shot, cowboy shot, wide angle, cinematic field of view, perfect composition, rule of thirds

### Style Tags (10 tags)
Art style and technique:
- anime illustration, semi-realistic anime illustration, digital painting, cel shading, clean linework, manga style lineart, detailed, highly detailed, intricate details, painterly

### Detail Tags (9 tags)
Fine detail enhancements:
- detailed eyes, beautiful eye details, detailed skin features, floating hair, flowing hair, intricate details, excellent depth of field, reflections, glossy

### Aesthetic Tags (11 tags)
Overall visual quality:
- eye-catching, beautiful, vivid colors, bright colors, vibrant, high contrast, extreme contrast, balanced colors, atmospheric, depth of field, atmospheric perspective

### Motion Tags (6 tags)
Dynamic elements:
- dynamic movement, motion lines, foreshortening, wind, floating, flowing

## Advanced Usage

### Custom Trigger Word Sets

You can create custom sets by:
1. Load a category
2. Edit tags as needed
3. Toggle unwanted tags off
4. The state is saved with your workflow

### Strength Adjustment Tips

- Default strength: 1.0
- Recommended range: 0.8 - 1.3
- Use higher values (1.2-1.5) for stronger emphasis
- Use lower values (0.7-0.9) for subtle effects
- Avoid extremes (<0.5 or >2.0) unless intentional

### Merge Strategy Guide

**When to use each:**
- **Keep Both**: See both versions, compare results
- **Prefer Preset**: Trust your curated presets over Lora metadata
- **Prefer Incoming**: Trust Lora metadata (recommended for trained trigger words)

### Performance Tips

- Use "Tagged Only" mode for pure tag management
- Enable deduplication to reduce token count
- Use presets for common setups, save time
- Batch toggle operations for quick experiments

## Integration with Workflows

### Typical Workflow Pattern

```
Checkpoint Loader → MODEL
                    ↓
Lora Loader (LoraManager) → MODEL, CLIP, trigger_words
                            ↓
Modify String ← trigger_words ← input_string (CLIP Text Encode)
                            ↓
                    output_string → CLIP Text Encode → Positive Prompt
```

### Multiple Loras

Connect multiple Lora Loaders via Lora Stacker, then connect stacker's trigger_words output to Modify String.

## Troubleshooting

### Tags Not Appearing
- Check if category is selected
- Click "Load Presets" button
- Verify default_active is True

### Duplicate Tags
- Enable "deduplicate" option
- Check merge_strategy setting
- Use "Prefer Incoming" or "Prefer Preset" to avoid duplicates

### Trigger Words Not Highlighted
- Verify connection from Lora Loader
- Check Lora has metadata with trigger words
- Ensure trigger_words output is connected

### Output String Empty
- Check if any tags are active (green)
- Verify mode is not "Replace" if you want input text
- Check separator is not causing issues

## API for Developers

### Python Node Interface

```python
from py.nodes.modify_string import ModifyString

node = ModifyString()
result = node.process_string(
    id="unique_id",
    preset_category="Quality",
    mode="Append",
    separator=", ",
    merge_strategy="Keep Both",
    deduplicate=True,
    default_active=True,
    allow_strength_adjustment=False,
    input_string="a beautiful scene",
    trigger_words="masterpiece,, best quality",
    modify_tags=[
        {"text": "masterpiece", "active": True, "strength": 1.2}
    ]
)
output_string, active_triggers = result
```

### JavaScript Extension

```javascript
// Listen for trigger word updates
api.addEventListener("modify_string_trigger_update", (event) => {
    const { id, graph_id, trigger_words } = event.detail;
    // Handle update
});
```

## Performance Characteristics

- **Tag Loading**: O(N) where N = number of presets
- **Tag Merging**: O(N+M) where N = presets, M = incoming tags
- **Tag Filtering**: O(N) where N = total tags
- **String Building**: O(N) where N = active tags
- **Memory**: ~1-2KB per 100 tags

Optimized for:
- Large preset sets (500+ tags)
- Real-time interaction
- Multiple node instances
- Frequent updates

## Version History

### v1.0.0 (Current)
- Initial release
- 50+ SDXL Illustrious presets
- 7 preset categories
- Lora integration
- Inline editing
- Strength adjustment
- Multiple merge strategies
- Batch operations
- Performance optimizations (O(N+M) merging, cached regex, singleton event listeners)

## Contributing

Found a bug or have a feature request? Please report in the issues section.

Want to add more presets? Edit `py/nodes/modify_string_presets.py` and submit a PR.

## License

Same as comfyui-lora-manager project license.
