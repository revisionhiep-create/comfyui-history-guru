# Changelog

All notable changes to ComfyUI Prompt Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-17

### Added
- Initial release of ComfyUI Prompt Library
- Automatic prompt recording with thumbnail generation
- SQLite database for efficient storage
- LoRA tracking with strength values
- Search functionality by LoRA name
- Favorites system with star/unstar
- Sort by date or alphabetically
- CSV export functionality
- Smart deduplication based on hash
- Automatic cleanup of old prompts
- Metadata extraction from workflows
- Aspect ratio preservation for thumbnails
- WebP format for efficient storage
- Interactive browser widget in node
- One-click copy to clipboard
- Individual prompt deletion
- Pagination for large libraries
- REST API endpoints for all operations
- Comprehensive documentation

### Technical Details
- Database: SQLite with indexed tables
- Thumbnails: WebP format at 512px max dimension
- Default history: 500 prompts (configurable)
- Automatic metadata extraction from ComfyUI workflows
- Support for CLIPTextEncode, LoraLoader, CheckpointLoader, KSampler nodes

[1.0.0]: https://github.com/yourusername/comfyui-prompt-library/releases/tag/v1.0.0
