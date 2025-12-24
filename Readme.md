# History Guru 🧘‍♂️ v4.2.1 (The Alignment Fix)

> **The 100% Offline, Single-File File Manager & Metadata Viewer for AI Images.**

**History Guru** has evolved into a precision instrument for AI creators. It is no longer just a viewer—it is a full-fledged **Local File Manager** and **Metadata Editor** for your ComfyUI and A1111 output folders. 

Organize, sort, move, rename, and "un-bake" your AI generations without ever leaving the metadata view. It runs entirely in your browser using the modern *File System Access API* (Chrome/Edge) or high-performance HTML5 inputs (Firefox).

---

## ✨ Core Feature Set

### 📂 Pro-Grade File Management (Chrome/Edge Only)
*   **True File Operations:** Create folders, rename files on disk, and move files between directories directly from the UI.
*   **Multi-Select Engine:** Full Windows-style `Shift+Click` (range) and `Ctrl+Click` (toggle) selection.
*   **Bulk Drag & Drop:** Select a group of images and drag them into the sidebar to organize your library in seconds.
*   **Direct Overwrite:** The "Fix & Save" engine writes updated metadata directly back to the original file—no more `fixed_` copies cluttering your folders.

### 🪄 Advanced Metadata & LoRA Engine
*   **LoRA "Un-Baking":** Intelligent parser auto-detects baked resources in ComfyUI/A1111 metadata and imports them into the editable LoRA manager.
*   **Universal LoRA Manager:** Add, remove, update strength, and reorder LoRA tags via a dedicated visual editor.
*   **Lossless Injection:** Writes corrected metadata directly back to the PNG binary using CRC32 checksum injection—no re-encoding or quality loss.
*   **Pro-Grade EXIF:** Deep support for UNICODE (UTF-16), ASCII, and UTF-8 encoded `UserComment` fields.

### 🖼️ High-Performance Gallery
*   **Massive Scaling:** Dynamic thumbnail engine provides **3x larger previews** via a smooth scaling slider.
*   **Hybrid View:** Instant toggle between a **Categorized List View** (with clickable sort headers) and a **Visual Grid View**.
*   **Cinema Mode:** A split-screen "Detail View" for full-height image inspection alongside live metadata editing.
*   **Memory Safety:** Systematic `URL Lifecycle Management` and debounced URL revocation ensure smooth performance even with 1000+ images.

### 🌗 Daylight & Night Modes
*   **Universal Parity:** Reworked Light Mode with theme-aware CSS variables. Overlays, labels, and selection highlights are high-contrast and perfectly legible in bright environments.

---

## 🚀 How to Use

### 🟢 Chrome / Edge / Opera (Recommended)
*Best for: Managing files, bulk organizing, and direct disk editing.*

1.  **Open** `Guru Manager ChromeEdge Edition.html` in your browser.
2.  **Grant Permission:** Click **"Open Folder"** and select your directory. When the browser asks, click **"Edit"** or **"Allow"** to enable file management features.
3.  **Organize:** Use the sidebar to create folders. Use `Shift+Click` to select groups and drag them into new locations.
4.  **Edit:** Click any image to open the Inspector. Edit prompts or LoRAs and hit **"Fix & Save"** to overwrite the file on disk.

### 🟠 Firefox Edition
*Best for: Fast metadata inspection and image conversion.*

1.  **Open** `Guru Manager Firefox Edition.html` in Firefox.
2.  **Load:** Click **"Load Folder"** and select your directory.
3.  **Export:** Edit metadata as needed. Hit **"Fix & Save"**. 
    *   *Tip:* Enable **"Always ask where to save files"** in Firefox Settings to use the download button as a "Save As" feature.
4.  **Parity:** Enjoy the same LoRA manager and metadata tools as the Chrome edition in a lightweight, read-only environment.

---

## ⌨️ Keyboard Shortcuts
*   `Arrow Keys` - Navigate images in detail view
*   `Esc` - Blur active input / Close overlays / Exit detail view
*   `T` - Toggle theme (Dark/Light)
*   `F` - Focus search box
*   `R` - Refresh folder
*   `?` or `/` - Show help & shortcuts
*   `S` - Toggle Statistics view

---

## 🔧 Technical Architecture
*   **File System Access API:** Direct disk I/O for file moves and renames.
*   **IndexedDB Caching:** Instant subsequent loads for thousands of images.
*   **Virtual Scrolling:** Near-zero lag when browsing massive collections.
*   **CRC32 Binary Injection:** Patches PNG chunks without re-encoding pixel data.

---

## 📄 License
MIT License - Free to use, modify, and distribute for the AI art community.

---

## 🚀 Version History

### [4.2.1] - 2025-12-24
- **US Date Format**: Switched to `MM/DD/YYYY` localization.
- **List Alignment**: Fixed "Header Shift" bug when thumbnails are off.
- **First-Seen Engine**: Cached initial scan dates to separate "Created" from "Modified".

### [4.2.0] - 2025-12-24
- **Direct Overwrite**: "Fix & Save" now overwrites original files in Chrome/Edge.
- **Multi-Selection**: Added `Shift+Click` and `Ctrl+Click` support.
- **Bulk Drag & Drop**: Move selected files in groups.
- **On-Disk Renaming**: Added rename feature to the metadata panel.
- **LoRA Un-baking**: Auto-import baked resources into editable tags.
- **Dual-Engine Export**: High-fidelity Save Picker for Chromium; Binary-masking for Firefox.
- **Ergonomic Layout**: LoRA Manager moved below Negative Prompt.

### [4.1.0] - 2025-12-21
- **Thumbnail Scaling**: Reworked math for 3x larger previews.
- **Grid/List Toggle**: Dedicated button for instant layout switching.
- **Thumbnail Toggle**: Status indicator (Green/Red) for visibility.
- **Light Mode Audit**: High-contrast variables for Daylight Mode.

### [4.0.0] - 2025-12-22
- **Advanced Memory Management**: URL Lifecycle Management to prevent leaks.
- **EXIF Engine**: Enhanced support for UNICODE and Civitai standards.
- **Duplicate Finder**: Ultra-fast hashing (first 50KB).

---
**Made with ❤️ for the AI art community**


