# Standard Trigger Words Loader - Quick Reference V2

## **New Interactive Button Interface**

### **How It Works**

Your trigger words appear as **clickable button tags** (similar to Lora Manager's Trigger Word Toggle):

- **Blue buttons** = Active (will be included in output)
- **Gray buttons** = Inactive (will be excluded)

### **Basic Operations**

| Action | How To | Result |
|--------|--------|--------|
| **Toggle ON/OFF** | Left-click a button | Toggles between active (blue) and inactive (gray) |
| **Edit Text** | Right-click a button | Opens prompt to edit the trigger word |
| **Adjust Strength** | Scroll mouse wheel over button | Increases/decreases strength (if enabled) |
| **Load Presets** | Change `preset_category` dropdown | Loads new set of trigger words |
| **Toggle All ON** | Click "Toggle All ON" button | Activates all trigger words |
| **Toggle All OFF** | Click "Toggle All OFF" button | Deactivates all trigger words |
| **Clear All** | Click "Clear All" button | Removes all trigger words (with confirmation) |

### **Settings**

**preset_category**: Choose which preset to load
- Quality (default quality tags like "masterpiece", "best quality")
- Lighting (lighting-related tags)
- Composition (camera angles and composition)
- Style (art style tags)
- Detail (detail enhancement tags)
- Aesthetic (beauty/aesthetic tags)
- Motion (movement and action tags)
- All (loads all categories combined)

**default_active**: Whether new trigger words start enabled (blue) or disabled (gray)

**allow_strength_adjustment**: Enable (word:1.2) strength syntax
- When enabled, scroll wheel over buttons adjusts strength
- Strength badge appears on each button

### **Output**

**Single Output: `trigger_words`**
- Contains only the **active** (blue) trigger words
- Formatted as comma-separated string: `"masterpiece, best quality, 8K"`
- Connect directly to **Trigger Word Toggle** node

### **Connection Example**

```
Standard Trigger Words → Trigger Word Toggle → CLIP Text Encode
     (trigger_words)
```

The output is specifically formatted to work with the Trigger Word Toggle node from Lora Manager.

### **Tips**

1. **Start with Quality preset** - Contains the most useful general-purpose tags
2. **Click individual buttons** - Toggle only the tags you want for this specific image
3. **Right-click to customize** - Edit any tag to match your specific needs
4. **Use "Toggle All OFF"** - Start with everything off, then click to enable only what you need
5. **Preset categories are starting points** - Feel free to edit tags to match your workflow

### **Visual Guide**

```
┌────────────────────────────────────────────┐
│ Standard Trigger Words 📝                  │
├────────────────────────────────────────────┤
│ preset_category: [Quality      ▼]         │
│ default_active:  [✓]                       │
│ allow_strength:  [ ]                       │
├────────────────────────────────────────────┤
│ ┌────────────────────────────────────────┐ │
│ │ [masterpiece] [best quality] [8K]      │ │ ← Click buttons
│ │ [HDR] [absurdres] [high quality]       │ │   to toggle
│ │ [ultra high definition] [newest]       │ │   ON/OFF
│ └────────────────────────────────────────┘ │
│                                            │
│ [ Toggle All ON  ]  [ Toggle All OFF ]    │
│ [ Clear All ]                              │
├────────────────────────────────────────────┤
│ → trigger_words                            │
└────────────────────────────────────────────┘
```

---

## **Differences from V1**

### **What Changed:**

- ❌ No more text area with line-by-line editing
- ✅ Interactive clickable button tags instead
- ❌ Removed multiple outputs (output_string, active_triggers)
- ✅ Single output: trigger_words (for Trigger Word Toggle)
- ❌ Removed mode selector (Append/Prepend/Replace)
- ✅ Direct connection to Trigger Word Toggle node
- ❌ Removed merge_strategy and deduplicate options
- ✅ Simpler, cleaner interface focused on tag management

### **Why This is Better:**

1. **Visual Feedback** - See which tags are active at a glance (blue = ON, gray = OFF)
2. **Faster Workflow** - Click to toggle, no typing required
3. **Compatible** - Works directly with existing Trigger Word Toggle nodes
4. **Less Complex** - Removed options that weren't needed for basic usage
5. **Mouse-Driven** - Left-click toggle, right-click edit, scroll for strength

---

## **Troubleshooting**

**Q: Buttons don't appear**  
A: Select a preset_category from the dropdown to load trigger words

**Q: Right-click doesn't open edit menu**  
A: Make sure you're clicking directly on a button tag, not empty space

**Q: Strength doesn't adjust with scroll wheel**  
A: Enable `allow_strength_adjustment` checkbox first

**Q: Tags don't connect to Trigger Word Toggle**  
A: Connect the `trigger_words` output (only output) to Trigger Word Toggle's input

**Q: All tags are gray (inactive)**  
A: Uncheck `default_active` was probably disabled. Click individual tags to enable them or use "Toggle All ON"
