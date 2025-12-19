# 📚 ComfyUI Prompt Library

A powerful ComfyUI custom node for automatically recording and browsing your prompt generation history with thumbnail previews, LoRA tracking, and advanced search capabilities.

## ✨ Features

- **📸 Automatic Recording**: Captures every generation with thumbnail, prompt, and metadata
- **🖼️ Visual History**: Browse your prompt history with thumbnail previews
- **🏷️ LoRA Tracking**: Automatically tracks LoRAs used with their strength values
- **🔍 Smart Search**: Search prompts by LoRA name
- **⭐ Favorites**: Mark your best prompts for quick access
- **📊 Sort & Filter**: Sort by date or alphabetically, filter by favorites
- **📋 Copy to Clipboard**: One-click copy for any prompt text
- **💾 Export**: Export your entire library to CSV
- **🔄 Smart Deduplication**: Automatically skips duplicate prompts
- **⚙️ Configurable History**: Auto-maintains last 500 prompts (configurable)
- **📐 Aspect Ratio Preservation**: Thumbnails maintain original image proportions
- **🎯 Metadata Extraction**: Captures checkpoint, seed, resolution automatically

## 📦 Installation

### Method 1: ComfyUI Manager (Recommended)

1. Open ComfyUI Manager
2. Search for "Prompt Library"
3. Click Install
4. Restart ComfyUI

### Method 2: Manual Installation

1. Navigate to your ComfyUI custom nodes directory:
   ```bash
   cd ComfyUI/custom_nodes/
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/comfyui-prompt-library.git
   ```

3. Install dependencies:
   ```bash
   cd comfyui-prompt-library
   pip install -r requirements.txt
   ```

4. Restart ComfyUI

## 🚀 Usage

### Basic Setup

1. **Add the Node**: Find "📚 Prompt Library" in the node menu under "Prompt Library" category

2. **Connect It**: Add it to your workflow after image generation:
   ```
   [Your Workflow] → [Save Image / Preview Image] → [📚 Prompt Library]
   ```

3. **Feed It Images**: Connect the `images` output from your workflow to the Prompt Library node

4. **View Your History**: Click the "📚 Show/Hide Library" button on the node to open the browser

### Workflow Connection Options

**Option 1: After Save Image** (Recommended)
```
KSampler → VAE Decode → Save Image → Prompt Library
                                 ↓
                              (connect images)
```

**Option 2: After Preview Image**
```
KSampler → VAE Decode → Preview Image → Prompt Library
                                    ↓
                                (connect images)
```

**Option 3: Parallel Recording**
```
                    → Save Image
                    ↓
KSampler → VAE Decode → Prompt Library
                    ↓
                    → Preview Image
```

### Node Inputs

#### Required:
- **images**: Image tensor from your workflow (connect from VAE Decode, Save Image, etc.)

#### Optional:
- **prompt_text**: Explicit prompt text (auto-extracted if not provided)
- **negative_prompt**: Explicit negative prompt (auto-extracted if not provided)
- **checkpoint**: Model/checkpoint name (auto-extracted if not provided)
- **seed**: Generation seed (auto-extracted if not provided)

> **Note**: The node automatically extracts metadata from your workflow, so optional inputs are only needed if auto-extraction fails or you want to override values.

## 🎨 Interface Features

### Library Browser

Click "📚 Show/Hide Library" button to open an interactive browser showing:

- **Thumbnail Preview**: 512px thumbnails with preserved aspect ratios
- **Prompt Text**: Click any prompt to copy to clipboard
- **Generation Date**: Timestamp for each generation
- **Metadata Display**: Model, seed, resolution for each prompt
- **LoRA Information**: All LoRAs used with their strength values

### Controls

- **Search Bar**: Filter prompts by LoRA name
- **Sort Options**:
  - Sort by Date (newest first)
  - Sort Alphabetically
- **Favorites Filter**: Toggle to show only starred prompts
- **Export Button**: Download entire library as CSV

### Actions

- **⭐ Toggle Favorite**: Star/unstar prompts for quick access
- **🗑️ Delete**: Remove individual prompts from history
- **📋 Copy**: Click any prompt text to copy to clipboard
- **🖼️ View Full Size**: Click thumbnails to open full resolution

## 📁 File Storage

All data is stored in your ComfyUI output directory:

```
ComfyUI/output/Prompt History/
├── prompt_library.db          # SQLite database
├── thumbnails/                # WebP thumbnails
│   ├── prompt_1702843821000_a1b2c3d4.webp
│   ├── prompt_1702843822000_e5f6g7h8.webp
│   └── ...
└── prompt_library_export.csv  # Export file (when generated)
```

## ⚙️ Configuration

Edit `py/config.py` to customize:

```python
# History limit (number of prompts to keep)
DEFAULT_HISTORY_LIMIT = 500

# Thumbnail settings
THUMBNAIL_SIZE = 512          # Max dimension in pixels
THUMBNAIL_FORMAT = "WEBP"     # Image format
THUMBNAIL_QUALITY = 85        # Quality (1-100)

# Performance
MAX_SEARCH_RESULTS = 1000     # Maximum search results
DEFAULT_PAGE_SIZE = 50        # Prompts per page
```

## 🔧 Advanced Features

### Automatic Metadata Extraction

The node automatically detects and extracts:

- **Prompts**: From CLIPTextEncode nodes
- **LoRAs**: From LoraLoader nodes and `<lora:name:strength>` tags
- **Checkpoints**: From CheckpointLoader nodes
- **Seeds**: From KSampler nodes
- **Resolution**: From generated images

### Deduplication

Prompts are hashed based on:
- Prompt text
- Negative prompt
- Checkpoint name
- LoRA list with strengths

Duplicate prompts are automatically skipped to keep your library clean.

### Auto-Cleanup

When history exceeds the configured limit (default 500):
- Oldest prompts are automatically deleted
- Associated thumbnails are removed
- Database is optimized

## 📊 Database Schema

### Prompts Table
- `id`: Unique identifier
- `prompt_text`: Main prompt text
- `negative_prompt`: Negative prompt (optional)
- `checkpoint`: Model/checkpoint name
- `seed`: Generation seed
- `width`, `height`: Image dimensions
- `thumbnail_path`: Path to thumbnail
- `created_at`: Timestamp
- `is_favorite`: Favorite flag
- `hash`: Deduplication hash

### LoRAs Table
- `id`: Unique identifier
- `prompt_id`: Foreign key to prompts
- `lora_name`: LoRA filename
- `strength`: LoRA strength value

## 🐛 Troubleshooting

### Library Not Showing Prompts

1. Ensure you've connected the `images` input
2. Generate at least one image
3. Check ComfyUI console for errors
4. Verify database was created in `output/Prompt History/`

### Thumbnails Not Loading

1. Check thumbnails directory exists: `output/Prompt History/thumbnails/`
2. Verify write permissions
3. Check browser console for 404 errors

### Metadata Not Extracting

1. The node tries to auto-extract from workflow
2. Use explicit inputs if auto-extraction fails
3. Check that you're using standard ComfyUI nodes

### Performance Issues

1. Reduce `DEFAULT_PAGE_SIZE` in config
2. Export and archive old prompts
3. Manually delete old entries
4. Run database vacuum (future feature)

## 🔄 API Endpoints

The node provides REST API endpoints:

- `GET /prompt_library/api/prompts` - Get prompts with filtering
- `POST /prompt_library/api/favorite/{id}` - Toggle favorite
- `DELETE /prompt_library/api/prompt/{id}` - Delete prompt
- `GET /prompt_library/api/export` - Export to CSV
- `GET /prompt_library/api/stats` - Get statistics
- `GET /prompt_library/thumbnail/{filename}` - Serve thumbnail

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

### Development Setup

1. Clone the repository
2. Install development dependencies
3. Make your changes
4. Test thoroughly with ComfyUI
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by [ComfyUI_PromptManager](https://github.com/ComfyAssets/ComfyUI_PromptManager)
- Built for the ComfyUI community
- Thanks to all contributors and testers

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/comfyui-prompt-library/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/comfyui-prompt-library/discussions)

## 🗺️ Roadmap

### Planned Features

- [ ] Batch import from existing images
- [ ] Advanced filtering (by checkpoint, seed range, date range)
- [ ] Prompt editing in library
- [ ] Tags/categories for organization
- [ ] Statistics dashboard
- [ ] Search by prompt text
- [ ] Workflow recreation from history
- [ ] Multi-select operations
- [ ] Dark/light theme toggle
- [ ] Customizable thumbnail sizes

### Version History

#### v1.0.0 (Initial Release)
- ✅ Automatic prompt recording with thumbnails
- ✅ LoRA tracking with strengths
- ✅ Search by LoRA name
- ✅ Favorites system
- ✅ Sort by date/alphabetical
- ✅ CSV export
- ✅ Smart deduplication
- ✅ Auto-cleanup of old entries
- ✅ Metadata extraction
- ✅ Aspect ratio preservation

---

**Made with ❤️ for the ComfyUI community**
