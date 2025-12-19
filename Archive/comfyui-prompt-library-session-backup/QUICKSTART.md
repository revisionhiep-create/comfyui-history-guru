# 🚀 Quick Start Guide

Get started with ComfyUI Prompt Library in 5 minutes!

## Step 1: Install (2 minutes)

```bash
# Navigate to ComfyUI custom nodes
cd ComfyUI/custom_nodes/

# Clone the repository
git clone https://github.com/yourusername/comfyui-prompt-library.git

# Install dependencies
cd comfyui-prompt-library
pip install -r requirements.txt

# Restart ComfyUI
```

## Step 2: Add the Node (30 seconds)

1. Open ComfyUI
2. Right-click in the workflow
3. Search for "Prompt Library"
4. Click **"📚 Prompt Library"** to add it

## Step 3: Connect It (30 seconds)

Connect your workflow like this:

```
[Your Generation] → [Save/Preview Image] → [📚 Prompt Library]
                                        ↓
                                   (connect images output)
```

## Step 4: Generate! (1 second)

Click "Queue Prompt" and generate an image. The node automatically records:
- ✅ Your prompt
- ✅ LoRAs used
- ✅ Model/checkpoint
- ✅ Seed & settings
- ✅ Thumbnail preview

## Step 5: Browse Your Library (2 minutes)

Click the **"📚 Show/Hide Library"** button on the node to see:
- 📸 All your generations with thumbnails
- 🔍 Search by LoRA name
- ⭐ Star your favorites
- 📋 Copy prompts to clipboard
- 🗑️ Delete unwanted entries

## That's It! 🎉

Your prompt history is now automatically tracked. Every time you generate an image, it's saved to your library with full metadata.

## Quick Tips

### Search by LoRA
Type a LoRA name in the search box to find all generations using it.

### Mark Favorites
Click the ⭐ icon to star your best prompts.

### Copy Prompts
Click any prompt text to copy it to your clipboard.

### Export Your Library
Click "📥 Export CSV" to download your entire history.

### Adjust History Size
Edit `py/config.py` and change `DEFAULT_HISTORY_LIMIT = 500` to keep more or fewer prompts.

## Need Help?

- **Full Documentation**: See [README.md](README.md)
- **Installation Issues**: See [INSTALLATION.md](INSTALLATION.md)
- **Examples**: See [EXAMPLES.md](EXAMPLES.md)
- **Problems**: Check [GitHub Issues](https://github.com/yourusername/comfyui-prompt-library/issues)

---

**Happy Generating! 🎨**
