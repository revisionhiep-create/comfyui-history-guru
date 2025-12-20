# History Guru 🧘‍♂️ v4.0 (The Manager Update)

> **The 100% Offline, Single-File File Manager & Metadata Viewer for AI Images.**

**History Guru** has evolved. It is no longer just a viewer—it is a full-fledged **Local File Manager** for your ComfyUI and A1111 output folders.

You can now **organize, sort, move, and fix** your AI generations without ever leaving the metadata view. It runs entirely in your browser using the modern *File System Access API*.


## ✨ What's New in v4.0?

* **📂 True File Management:** You can now **create real folders** and **move files** on your hard drive directly from the interface.
* **Drag-and-drop Sorting:** Simply drag an image from the grid into a folder in the sidebar to move it. Perfect for separating "Keepers" from "Trash."
* **🚀 Virtual Scrolling:** Handles **650+ images** smoothly with virtual scrolling. Only visible items are rendered, ensuring smooth performance even with thousands of images.
* **🎬 Cinema Mode:** A new split-screen "Detail View." Click an image to see it full-height on the left while editing metadata on the right. Supports keyboard navigation (Arrow Keys) for fast review.
* **🎥 Video Support:** Now supports playing and organizing `.mp4` and `.webm` files (Sora/AnimateDiff workflows) alongside your images.
* **💾 Instant Fix & Save:** The "Fix Metadata" button no longer downloads a file to your "Downloads" folder. It now **writes the fixed image directly to your disk** (next to the original), injecting the missing metadata losslessly.
* **⭐ Favorites System:** Star your favorite images for quick access. Filter to show only favorites with one click. Favorite button available in detail view for easy access.
* **🔍 Enhanced Metadata Parsing:** Now supports Civitai metadata formats, including "prompt" and "workflow" chunks. Handles both ComfyUI workflow formats (direct nodes and nodes array).
* **📊 Clickable Column Sorting:** Click any column header (Name, Model, Date Modified, Date Created) in list view to sort ascending/descending. Visual indicators show current sort direction.
* **📋 Improved List View:** List view is now the default and primary view mode. Shows Model, Date Modified, and Date Created columns. Images are slightly larger for better visibility.
* **🔎 Enhanced Search:** Search now works across file names, prompts, models, samplers, seeds, steps, CFG, size, and LoRA resources. Empty search restores folder view.
* **⌨️ Keyboard Shortcuts:** Comprehensive keyboard navigation and shortcuts (press `?` for help).
* **❓ Help System:** Built-in help overlay showing all functions and keyboard shortcuts.
* **🗑️ Context Menu:** Right-click files and folders for quick actions (delete, etc.).

## 🆕 Latest Updates (December 2024)

* **🖱️ Clickable Column Sorting:** Click any column header (Name, Model, Date Modified, Date Created) in list view to sort. Click again to reverse direction. Visual indicators (↑/↓) show current sort state.
* **📋 List View Improvements:** List view is now the default and primary view mode. Images are 10-15% larger for better visibility. Grid view removed for optimal performance.
* **⭐ Favorite Button in Detail View:** Added favorite star button in the corner of full-size image view for easy favoriting while reviewing images.
* **🔎 Enhanced Search:** Search now works across file names, positive/negative prompts, model names, samplers, seeds, steps, CFG scale, size, and LoRA resources. Empty search restores folder view.
* **📊 Updated List Columns:** Changed from "Model, Sampler, Seed" to "Model, Date Modified, Date Created" for more useful file information.
* **🎨 UI Refinements:** Removed unnecessary view toggle buttons. Streamlined interface for better focus on content.

## 🆕 Previous Improvements (EXIF & Parsing Enhancements)

* **📸 EXIF UserComment Extraction:** Full support for extracting metadata from EXIF UserComment fields in both PNG (`eXIf` chunks) and JPEG (APP1 segments). This enables parsing of Civitai images that store metadata in EXIF format.
* **🌐 UTF-16 Encoding Support:** Properly decodes UTF-16LE and UTF-16BE encoded EXIF UserComment fields, handling the encoding format commonly used by Civitai and other platforms.
* **🧹 Enhanced Text Cleaning:** Improved text cleaning function removes null bytes, control characters, and encoding artifacts that can break metadata parsing, ensuring reliable extraction from various sources.
* **🔤 Case-Insensitive Parsing:** The A1111 parser now uses case-insensitive marker matching, handling variations like "Negative prompt:", "Negative Prompt:", and "negative prompt:" automatically.
* **🎯 Flexible Parameter Extraction:** Enhanced regex patterns for extracting Steps, Sampler, CFG Scale, Seed, Size, and Model parameters with flexible spacing and formatting variations.
* **🔄 Fallback Decoding:** Multiple fallback methods for extracting metadata from JPEG files, including direct UTF-16 decoding when EXIF structure parsing fails.

## 🧠 Core Features (Retained)

* **⚡ Instant Search:** Filter thousands of images by Prompt, Model Name, Seed, or LoRA Name in milliseconds.
* **✏️ Metadata Editor:** Manually edit missing or broken metadata fields (Prompt, Seed, Steps, etc.) directly in the sidebar.
* **🕸️ Deep Recursive Tracing:** The "Brain" of the operation. It recursively traces upstream nodes to find prompts hidden behind `SeedVarianceEnhancers`, `Logic Gates`, or complex `Lora Stackers` that standard viewers miss.
* **🔒 100% Private:** Zero server uploads. Your images never leave your hard drive.
* **📱 List View (Primary):** Optimized list view with clickable column sorting. Shows Model, Date Modified, and Date Created. Larger thumbnails for better visibility.
* **🌓 Theme Toggle:** Switch between dark and light themes with persistent preference storage.
* **📈 Statistics Dashboard:** View comprehensive metadata analytics including model usage, LoRA popularity, and more.

## 🚀 Quick Start

### For Chrome/Edge/Opera Users (Full Features)

1.  **Download** the `Guru Manager ChromeEdge Edition.html` file from the root directory of this repository.
2.  **Open** the file in **Chrome, Edge, or Opera**.
3.  Click **"Open Folder"** and select your ComfyUI/Output directory.
4.  **Grant Permission:** Your browser will ask if the site can "View and Edit" files. You **must click "Edit"** (or Allow) for the file manager features to work.
5.  **Organize:** Right-click the sidebar to create folders. Drag and drop images to move them. Click images to view metadata.
6.  **Explore:** Use keyboard shortcuts (press `?` for help), star favorites, sort by different criteria, and view statistics.

### For Firefox Users (View-Only Mode)

1.  **Download** the `Guru Manager Firefox Edition.html` file from the root directory of this repository.
2.  **Open** the file in **Firefox**.
3.  Click **"Load Folder"** and select your ComfyUI/Output directory.
4.  **Browse:** Click images to view metadata in full-screen detail view. Use arrow keys to navigate between images.
5.  **Explore:** Use keyboard shortcuts (press `?` for help), star favorites, sort by different criteria, and view statistics.

**Note:** The Firefox edition provides all viewing and metadata features, but does not support file operations (create, move, delete) due to browser API limitations.

## ⌨️ Keyboard Shortcuts

* `S` or `3` - Switch to Statistics view
* `T` - Toggle theme (dark/light)
* `?` - Show help overlay
* `F` - Focus search box
* `R` - Refresh folder
* `Arrow Keys` - Navigate in detail view
* `Enter` - Open selected image
* `Delete` - Delete selected item
* `Esc` - Close overlays / Exit detail view

**Note:** List view is now the default and primary view mode. Grid view has been removed for better performance.

Press `?` anytime to see the full list of shortcuts and features.

## ⚠️ Browser Compatibility

**Version 4.0 requires a browser that supports the *File System Access API*.**

| Browser | Status | Notes |
| :--- | :--- | :--- |
| **Google Chrome** | ✅ **Supported** | Recommended - Full file management features |
| **Microsoft Edge** | ✅ **Supported** | Recommended - Full file management features |
| **Opera** | ✅ **Supported** | Works out of the box - Full file management features |
| **Firefox** | ✅ **Supported** | Use `Guru Manager Firefox Edition.html` - View-only mode (no file operations) |
| **Safari** | ❌ **Not Supported** | Missing API support. |

### Firefox Edition

The **Firefox Edition** (`Guru Manager Firefox Edition.html`) provides the same UI/UX experience as v4.0, but without file management features (since Firefox doesn't support the File System Access API).

**✅ Available in Firefox Edition:**
- ⭐ Favorites system with filter (favorite button in detail view)
- 🔍 Enhanced search across file names, prompts, models, and all metadata fields
- 📊 Clickable column sorting (Name, Model, Date Modified, Date Created) with ascending/descending toggle
- 📋 Improved list view (default view) with larger images and better column layout
- 🌓 Theme toggle (dark/light)
- ⌨️ Keyboard shortcuts (press `?` for help)
- 🖼️ Full-screen detail view with arrow key navigation
- ❓ Help system overlay
- 🚀 Enhanced metadata parsing (ComfyUI, Civitai, A1111, EXIF UserComment)
- 📸 EXIF extraction support (PNG eXIf chunks, JPEG APP1 segments, UTF-16 decoding)
- 📈 Statistics dashboard
- 📱 List and Statistics view modes (Grid view removed for better performance)

**❌ Not Available in Firefox Edition:**
- File/folder creation
- Drag-and-drop file moving
- Direct file deletion
- Metadata fixing/saving (requires File System Access API)

**Usage:** Open `Guru Manager Firefox Edition.html` in Firefox, click "Load Folder" to select your image directory.

## 🔧 Technical Details

History Guru v4 uses a hybrid engine:
* **File System Access API:** Gives the browser direct read/write access to a specific folder on your user's command. This allows for real file operations (Move/Rename/Create) without a backend server.
* **IndexedDB Caching:** To handle folders with thousands of images, metadata is parsed once and stored in the browser's internal database. Subsequent loads are instant.
* **Virtual Scrolling:** For collections with 100+ images, only visible items are rendered, dramatically improving performance and memory usage.
* **Recursive Node Tracing:** Traces `positive` -> `conditioning` -> `node` links upwards endlessly until it finds the original text prompt.
* **CRC32 Binary Injection:** Calculates valid checksums to insert new `tEXt` chunks into existing PNG binaries without re-encoding the image pixel data (lossless patching).
* **Enhanced Metadata Parsing:** Supports multiple ComfyUI workflow formats (direct node objects and nodes array), Civitai "prompt" chunks, EXIF UserComment fields, and A1111 parameters format.
* **EXIF Extraction Engine:** Parses EXIF structure to locate UserComment tags (37510/0x927C), handles encoding indicators (UNICODE/ASCII), and decodes UTF-16 text properly.
* **Text Cleaning Pipeline:** Removes null bytes, control characters, and encoding artifacts before parsing to ensure reliable metadata extraction.
* **Debounced Scroll Events:** Optimized scroll handling with 16ms throttling for smooth virtual scrolling performance.

## 📋 Supported Metadata Formats

* **ComfyUI Workflows:** Full support for ComfyUI workflow JSON in "workflow" and "prompt" chunks
* **Civitai Format:** Supports Civitai's metadata format with "prompt" chunks and EXIF UserComment fields
* **A1111 Parameters:** Automatic1111-style text parameters with enhanced parsing (case-insensitive markers, flexible patterns)
* **PNG Text Chunks:** tEXt, iTXt, zTXt (compressed), and eXIf (EXIF) chunks
* **JPEG/EXIF:** Full EXIF UserComment extraction with UTF-16LE/BE decoding support
* **WebP:** WebP image format support
* **MP4/WebM:** Video file support for Sora/AnimateDiff workflows

### EXIF Metadata Support

History Guru now fully supports extracting metadata from EXIF UserComment fields, which is the format used by many Civitai images:

* **PNG Files:** Extracts metadata from `eXIf` chunks containing EXIF data
* **JPEG Files:** Extracts metadata from APP1 segments containing EXIF data
* **Encoding Support:** Handles UTF-16LE, UTF-16BE, ASCII, and UTF-8 encoded UserComment fields
* **Fallback Methods:** Multiple fallback decoding strategies ensure maximum compatibility

## 🎯 Performance Features

* **Virtual Scrolling:** Automatically activates for folders with 100+ images
* **IndexedDB Caching:** Metadata is cached for instant subsequent loads
* **Debounced Events:** Scroll and resize events are optimized for performance
* **Lazy Image Loading:** Images load on-demand as you scroll

## 📁 Project Structure

Files are organized into folders:
- Root directory - Main HTML applications (`Guru Manager ChromeEdge Edition.html`, `Guru Manager Firefox Edition.html`)
- `apps/` - Development copies and additional HTML files
- `tools/` - AI development tools (Python scripts)
- `docs/` - Documentation files
- `data/` - Reference databases (JSON)
- `test-data/` - Test images
- `backup/` - Automatic backups

See `INDEX.md` for a complete file index.

## 🤝 Contributing

Feel free to fork this repository and submit Pull Requests.

**License:** MIT
**Created by:** The Community & The AI Assistant
