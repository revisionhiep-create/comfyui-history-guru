# Changelog - Guru Manager

All notable changes to the Guru Manager project will be documented in this file.

## [4.0.0] - 2025-12-22

### Added
- **🧠 Advanced Memory Management**: Implemented `URL Lifecycle Management`. Automatically revokes Object URLs when clearing the gallery or switching folders, preventing memory leaks during long sessions.
- **🖼️ Pro-Grade EXIF Engine**: Enhanced metadata extraction for JPEG and WebP. Full support for UNICODE (UTF-16 LE/BE), ASCII, and UTF-8 encoded `UserComment` fields (Civitai standard).
- **🖱️ Infinite Scroll Fix**: Added a `checkScroll` mechanism that ensures content loads smoothly even when thumbnails are OFF (small row heights).
- **⚡ Ultra-Fast Duplicate Finder**: Now uses `Blob.slice()` to hash only the first 50KB of files, making duplicate scans near-instant.
- **🛠️ Robust Scanning**: Updated the folder loader to use `Promise.allSettled`, ensuring the scan continues even if individual files have corrupted metadata.

### Fixed
- Fixed broken `detailImage` reference in Firefox Edition.
- Restored missing `renderTree` function in Firefox Edition.
- Removed duplicate `applySort` function in Firefox Edition.
- Fixed infinite scroll bug in Firefox Edition where small rows failed to trigger next batch.

## [1.1.0] - 2025-12-21

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
- Comprehensive `.gitignore` file to prevent tracking of system-generated files, local environment artifacts, and development-only tools (Cursor rules, index files, backups, etc.).
- Root-level `CHANGELOG.md` to track workspace-wide architectural changes.
- **Mandatory Descriptive Commits**: Added a new rule to `docs/AI_CODING_RULES.md` requiring highly descriptive commit messages for all changes.

### Fixed
- **Dynamic Row Height**: Fixed an issue in both editions where list rows would maintain their large height even after turning thumbnails off. The rows now correctly snap back to a compact text-only height when images are disabled.
- **Light Mode UI Fixes**:
    - **ChromeEdge Edition**: Fixed invisible refresh symbol in header and black UI elements in the Metadata Inspector when in light mode.
    - **Firefox Edition**: Fixed Metadata Inspector and detail view background remaining black in light mode.
    - **General**: Improved button hover contrast across all themes by using theme-aware CSS variables.
- **Merge Conflict Resolution**: Resolved content conflict in `Guru Manager Firefox Edition.html` for PR #5 in the `comfyui-history-guru` repository, ensuring the new sidebar layout is preserved while integrating UI fixes.
