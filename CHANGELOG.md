# Changelog - Guru Manager

All notable changes to the Guru Manager project will be documented in this file.

## [4.2.0] - 2025-12-24

### Added
- **💾 Direct File Overwrite (Chrome/Edge)**: Optimized "Fix & Save" to overwrite original files directly via File System Access API instead of creating `fixed_` copies.
- **🖱️ Pro-Selection Engine**: Implemented full `Shift+Click` and `Ctrl+Click` multi-selection in both List and Grid views for the Chrome/Edge edition.
- **📦 Multi-File Operations (Chrome/Edge)**: Enabled bulk drag-and-drop moving for selected groups of files to new directories.
- **🪄 LoRA "Un-Baking"**: Intelligent parser now auto-imports "baked" ComfyUI/A1111 resources into editable LoRA tags, ensuring embedded models are never lost during metadata edits.
- **✏️ On-Disk Renaming (Chrome/Edge)**: Added a metadata-panel rename feature that updates file names directly on the filesystem.
- **🚀 Dual-Engine Export (Firefox)**: Implemented a hybrid "Save As" strategy using `showSaveFilePicker` for Chromium and `application/octet-stream` masking for Firefox to ensure system save prompts.
- **🏗️ Ergonomic UI Layout**: Relocated the LoRA Manager below the Negative Prompt to follow natural prompt-engineering hierarchy.
- **☀️ Daylight Parity**: Comprehensive Light Mode audit fixed invisible overlays (Help, Welcome, Resources) and boosted selection visibility with `--sel-bg` accents.
- **🧹 Debounced URL Revocation**: Optimized memory management to only flush Object URLs after 100 items, significantly smoothing out gallery scrolling.

### Fixed
- **📺 Fullscreen Integrity**: Fixed the "X" button in Fullscreen mode to correctly exit detail view and restore the previous UI state.
- **🖼️ Thumbnail Persistence**: Resolved a bug where thumbnails would unexpectedly turn back ON when exiting image detail mode.
- **⌨️ Keyboard Safeguards**: Updated `Esc` key behavior to blur active text inputs instead of closing the entire viewer.
- **🛡️ Renaming Sanitization**: Integrated strict filename sanitization to prevent illegal OS characters during rename operations.
- **📐 Z-Index Architecture**: Lifted all global overlays to `z-index: 5000` to prevent collision with the Metadata Inspector.

## [4.1.0] - 2025-12-21

### Added
- **Substantial Thumbnail Scaling**: Reworked the list view scaling math to provide much larger thumbnails when using the slider. The "Large" setting now results in thumbnails that are over 3x bigger than the original fixed size, ensuring a clear visual impact when scaling.
- **Increased Default Thumbnail Size**: Increased the base thumbnail size by 40% in both editions. The list view now automatically adjusts its row height and column widths to accommodate larger images without scaling the text.
- **Enhanced Slider Range**: Updated the thumbnail resizer slider to support 20% increments (5 steps) centered around the new larger default.
- **Context-Aware Grid Toggle**: The Grid/List toggle button now automatically hides when thumbnails are disabled, providing a cleaner UI when viewing metadata-only lists.
- **Grid View Mode (ChromeEdge)**: Implemented a proper Grid View for the ChromeEdge edition, allowing users to browse images as cards.
- **Grid/List Toggle**: Added a dedicated button (🔲/☰) in the header of both editions to easily switch between Grid and List views.
- **Responsive Thumbnails**: Linked the thumbnail resizer to both Grid cards and List images. Moving the slider now dynamically resizes images in both view modes.
- **Thumbnail Resizer**: Added a size slider to the grid toolbar in both editions. Users can now dynamically adjust the thumbnail size from 60% to 140% of the default size. The setting is saved persistently and automatically hides when thumbnails are disabled.
- **LoRA Visibility Improvements (Daylight Mode)**: Increased text contrast and added dedicated background variables for resource chips (LoRA, Model) and strength badges in both editions. Text is now significantly darker and more legible in Light Mode.
- **Metadata Stats Toggle (ChromeEdge)**: The Statistics button now acts as a toggle, allowing users to switch back to the main UI by clicking it again.
- **Thumbnail Toggle**: Added a "Thumbnails" button in the header of both ChromeEdge and Firefox editions to toggle image visibility in list view. Includes a visual status indicator (Green/Red dot) and persistent state via `localStorage`.
- **Comprehensive .gitignore**: Added a root-level file to prevent tracking of system-generated files and development-only tools.
- **Root-level CHANGELOG.md**: Documenting workspace-wide architectural changes.
- **Mandatory Descriptive Commits**: New coding rules for architectural transparency.

### Fixed
- **Dynamic Row Height**: Fixed an issue in both editions where list rows would maintain their large height even after turning thumbnails off.
- **Light Mode UI Fixes**: Fixed invisible refresh symbols and black background issues across both editions when in Light mode.
- **Merge Conflict Resolution**: Resolved sidebar layout conflicts in the Firefox Edition.

## [4.0.0] - 2025-12-22

### Added
- **🧠 Advanced Memory Management**: Implemented `URL Lifecycle Management` to prevent leaks.
- **🖼️ Pro-Grade EXIF Engine**: Enhanced metadata extraction for JPEG and WebP with full UNICODE support.
- **🖱️ Infinite Scroll Fix**: Smooth content loading even when thumbnails are disabled.
- **⚡ Ultra-Fast Duplicate Finder**: Near-instant scans using partial file hashing.
- **🛠️ Robust Scanning**: Folder loader now handles corrupted metadata gracefully.

### Fixed
- Fixed broken `detailImage` references and restored missing `renderTree` in Firefox Edition.
- Removed duplicate `applySort` logic.
