# History Guru 🧘‍♂️ v4.0 (The Manager Update)

> **The 100% Offline, Single-File File Manager & Metadata Viewer for AI Images.**

**History Guru** has evolved. It is no longer just a viewer—it is a full-fledged **Local File Manager** for your ComfyUI and A1111 output folders. 

You can now **organize, sort, move, and fix** your AI generations without ever leaving the metadata view. It runs entirely in your browser using the modern _File System Access API_.

## ✨ What's New in v4.0?

* **📂 True File Management:** Create real folders and move files on your hard drive directly from the interface.
* **🚀 Massive Scaling Engine:** Reworked thumbnail math. The new slider provides **3x larger previews** than previous versions, allowing for clear visual impact during scaling.
* **📋 Enhanced List View:** List view is now the default mode. It features clickable column headers (Name, Model, Date Modified, Date Created) with ascending/descending toggles and visual sort indicators.
* **🔲 Integrated Grid View:** A dedicated button (🔲/☰) allows for instant switching between Grid and List modes. Both modes are linked to the same dynamic scaling engine.
* **🧠 Advanced Memory Management:** Implemented systematic `URL Lifecycle Management`. The app now revokes Object URLs when clearing the gallery or switching folders, preventing memory leaks even with 1000+ images.
* **🖼️ Pro-Grade EXIF Engine:** Enhanced metadata extraction for JPEG and WebP. Full support for UNICODE (UTF-16 LE/BE), ASCII, and UTF-8 encoded `UserComment` fields (Civitai standard).
* **🖱️ Infinite Scroll Fix:** Added a `checkScroll` mechanism that ensures content loads smoothly even when thumbnails are OFF (small row heights).
* **⚡ Ultra-Fast Duplicate Finder:** Now uses `Blob.slice()` to hash only the first 50KB of files, making duplicate scans near-instant without high memory overhead.
* **🎬 Cinema Mode:** A split-screen "Detail View" allows you to view images at full height while editing metadata on the right. Supports full keyboard navigation.
* **🎥 Video Support:** Organizes and plays `.mp4` and `.webm` files alongside your generations.
* **💾 Lossless Metadata Injection:** The "Fix & Save" button writes corrected metadata directly back to the PNG binary using CRC32 checksum injection—no re-encoding required.
* **🌗 High-Contrast Daylight Mode:** Reworked Light Mode with theme-aware CSS variables. Resource chips (LoRA, Model) and strength badges now feature significantly higher contrast for better legibility in bright environments.

## 🚀 Version History

### [4.0.0] - 2025-12-22
- **Advanced Memory Management**: URL Lifecycle Management to prevent leaks.
- **Improved EXIF Engine**: Support for UNICODE (UTF-16 LE/BE), ASCII, and UTF-8 encodings.
- **Infinite Scroll Fix**: checkScroll() mechanism for small row heights.
- **Duplicate Finder Optimization**: Partial file hashing (first 50KB) for near-instant scans.
- **Scanning Robustness**: Promise.allSettled() for folder loading.

### [1.1.0] - 2025-12-21
- **Substantial Thumbnail Scaling**: Reworked math for 3x larger thumbnails.
- **Increased Default Thumbnail Size**: Base size increased by 40%.
- **Enhanced Slider Range**: 20% increments (5 steps).
- **Context-Aware Grid Toggle**: Button automatically hides when thumbnails are disabled.
- **Grid View Mode (ChromeEdge)**: Implemented card-based browsing.
- **Grid/List Toggle**: Dedicated button (🔲/☰) linked to dynamic scaling.
- **LoRA Visibility Improvements (Daylight Mode)**: High-contrast labels for Light Mode.
- **Metadata Stats Toggle**: Statistics button now toggles view.
- **Thumbnail Toggle**: Added button with visual status indicator.

## 🚀 Quick Start

### For Chrome/Edge/Opera Users (Full Features)

1. **Download** the `Guru Manager ChromeEdge Edition.html` file.
2. **Open** the file in **Chrome, Edge, or Opera**.
3. Click **"Open Folder"** and select your output directory.
4. **Grant Permission:** Click **"Edit"** (or Allow) for the file manager features to work.
5. **Organize:** Use the sidebar to create folders and drag-and-drop to organize.

### For Firefox Users (View-Only Mode)

1. **Download** the `Guru Manager Firefox Edition.html` file.
2. **Open** it in **Firefox**.
3. Click **"Load Folder"** and select your directory.
4. **Browse:** Use arrow keys to navigate and view metadata in full-screen Cinema mode.

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

## 🔧 Technical Details

* **File System Access API**: Direct read/write access for real file operations.
* **IndexedDB Caching**: Instant subsequent loads for thousands of images.
* **Virtual Scrolling**: Smooth performance for large collections (650+ images).
* **CRC32 Binary Injection**: Lossless metadata patching without re-encoding.
* **Recursive Node Tracing**: Endlessly traces prompt links in ComfyUI workflows.

## 📄 License

MIT License - Free to use, modify, and distribute.

---
**Made with ❤️ for the AI art community**
