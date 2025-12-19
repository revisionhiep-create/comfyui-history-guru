# ComfyUI Custom Node Development - Guru Best Practices (2023-2025)

## AI Assistant Coding Rules & Workflow

### AI Coding Tools Available

**Analysis Tools:**
- `ai_code_analyzer.py` - Analyze code structure, dependencies, complexity
- `ai_code_diff.py` - Compare code before/after changes
- `ai_pattern_matcher.py` - Find patterns and suggest improvements
- `ai_context_builder.py` - Build context about function relationships

**Reference Tools:**
- `load_coding_reference.py` - Search coding reference databases
- `coding_reference_js.json` - JavaScript patterns and APIs
- `coding_reference_python.json` - Python patterns and APIs
- `coding_reference_html5.json` - HTML5 patterns and APIs

**Quality Tools:**
- `test_guru_manager.py` - Validate code before changes
- `backup_file.py` - Create/restore backups

**Usage:**
```bash
# Before changes
python backup_file.py "file.html"
python ai_code_analyzer.py "file.html"
python load_coding_reference.py js "file system"

# After changes
python ai_code_diff.py "backup/file.html" "file.html"
python test_guru_manager.py
```

### When to Consult Coding References

**Always consult references when:**
1. **Using a new API for the first time** - Check `coding_reference_js.json`, `coding_reference_python.json`, or `coding_reference_html5.json` for correct syntax and patterns
2. **Encountering an error** - Before debugging, check reference for correct usage patterns
3. **Implementing a feature you haven't used recently** - Refresh memory on File System Access API, IndexedDB, etc.
4. **Writing code that interacts with browser APIs** - File System Access API, localStorage, IndexedDB patterns change, always verify
5. **Before making significant changes** - Review reference patterns to ensure you're using best practices

**Reference consultation frequency:**
- **Every 3-5 function implementations** - Quick check to ensure patterns are correct
- **Before any file system operation** - File System Access API has quirks, always verify
- **When switching between languages** - JS vs Python patterns differ significantly
- **When implementing error-prone features** - Context menus, drag-drop, async operations

**How to use references:**
```bash
# Search JavaScript reference
python load_coding_reference.py js "file system"

# Search Python reference  
python load_coding_reference.py python "metadata"

# Search HTML5 reference
python load_coding_reference.py html5 "context menu"
```

### Backup System Rules

**MANDATORY: Always create backup before making changes**

1. **Before ANY code modification:**
   - Create backup in `backup/` folder
   - Format: `backup/FILENAME_YYYYMMDD_HHMMSS.html` (or .py, .js, etc.)
   - Include timestamp for easy identification

2. **Backup naming convention:**
   - `Guru Manager.html` → `backup/Guru Manager_20251219_143022.html`
   - Include date and time for chronological sorting
   - Keep original filename for easy identification

3. **When to create backups:**
   - Before editing any file
   - Before adding new features
   - Before fixing bugs
   - Before refactoring code
   - Before testing changes

4. **Backup folder structure:**
   ```
   backup/
   ├── Guru Manager_20251219_140000.html  (before feature X)
   ├── Guru Manager_20251219_143000.html  (before feature Y)
   └── ...
   ```

5. **Restore from backup:**
   - If changes break functionality, restore from most recent working backup
   - Compare backups to see what changed
   - Use backup to understand what worked before

### When to Update coding_guru.md

**Update coding_guru.md when you learn:**

1. **New API limitations or quirks:**
   - Example: "File System Access API cannot rename directories"
   - Example: "Cut/paste is unreliable, use drag-drop instead"
   - **Update immediately** - Critical for future development

2. **Better patterns or solutions:**
   - Example: "Use toast notifications instead of alert()"
   - Example: "Always return consistent types for backward compatibility"
   - **Update after implementation** - Document what worked

3. **Common pitfalls discovered:**
   - Example: "Don't change function return types without updating callers"
   - Example: "Test before and after every change"
   - **Update when discovered** - Prevent future mistakes

4. **New testing strategies:**
   - Example: "Created test_guru_manager.py for validation"
   - Example: "Always run tests before asking user to test"
   - **Update when strategy is proven** - Document successful approaches

5. **Performance optimizations:**
   - Example: "Use Maps for O(1) lookups"
   - Example: "Virtual scrolling for large lists"
   - **Update when implemented** - Share optimization patterns

**Update frequency:**
- **After each significant feature** - Document what you learned
- **When you solve a difficult problem** - Others (or future you) will benefit
- **When you discover a limitation** - Critical to document immediately
- **At end of session** - Summarize key learnings

**What to include in updates:**
- **What you learned** - The new knowledge
- **Why it matters** - The problem it solves
- **Code examples** - Show the pattern
- **Common mistakes** - What to avoid
- **Best practices** - Recommended approach

**Update format:**
```markdown
## New Section Title (Date)

### What I Learned
[Description]

### Why It Matters
[Explanation]

### Code Pattern
```code
[Example]
```

### Common Pitfalls
- [Pitfall 1]
- [Pitfall 2]
```

## Python (ComfyUI Backend)

### 1. Advanced Tensor Lifecycle Management
Implement sophisticated tensor pooling and lifecycle management to prevent memory leaks in long-running workflows. Use `torch.cuda.memory_summary()` for debugging and implement custom tensor registries that track allocation/deallocation across node executions. Consider implementing weak references for intermediate tensors that can be garbage collected when not actively used in the execution chain.

### 2. Dynamic Graph Optimization with Caching
Build intelligent caching layers that adapt to workflow patterns. Implement hash-based caching of node outputs using content-addressable storage, combined with metadata tracking for cache invalidation. Use bloom filters for fast cache lookups and implement progressive caching where expensive computations are cached at multiple granularity levels.

### 3. Advanced Input Validation with Type Coercion
Create robust input validation systems that can handle partial inputs and implement smart type coercion. Use dataclasses with custom validators for node configurations, implementing progressive validation where basic checks happen early and complex validations occur during execution preparation. Include metadata-driven validation rules that can be dynamically updated based on model capabilities.

## JavaScript (LiteGraph/UI)

### 1. Reactive State Synchronization Patterns
Implement reactive state management using proxies and observers for seamless UI-model synchronization. Use mutation observers combined with custom event buses to create declarative UI updates that automatically propagate changes across nested node configurations. Implement optimistic updates with rollback mechanisms for complex multi-property interactions.

### 2. Performance-Optimized Graph Rendering
Leverage WebGL-accelerated rendering for large graphs with thousands of nodes. Implement level-of-detail (LOD) rendering where node complexity decreases with zoom level, combined with virtual scrolling for graph canvases. Use worker threads for layout calculations and implement incremental rendering that only updates changed subgraphs.

### 3. Advanced Node Configuration DSL
Build domain-specific languages for node configuration that support conditional logic and dynamic property generation. Implement fluent APIs for complex node setups with validation at the DSL level, combined with visual configuration builders that generate optimized execution graphs. Include support for node composition patterns where complex nodes can be built from simpler reusable components.

## Python Coding Standards & Best Practices

### Core Language Patterns for ComfyUI Backend

#### Do's ✅
- **Use type hints extensively**: Leverage `typing` module for all function signatures, class attributes, and return types
- **Implement proper async patterns**: Use `asyncio` for I/O operations, `concurrent.futures` for CPU-bound tasks
- **Structure with dataclasses**: Use `@dataclass` for configuration objects and simple data containers
- **Leverage context managers**: Implement `__enter__`/`__exit__` for resource management (GPU memory, file handles)
- **Use pathlib over os.path**: For all file system operations
- **Implement proper logging**: Use `logging` module with structured logging and log levels
- **Document with docstrings**: Use Google/NumPy style docstrings for all public APIs
- **Handle exceptions granularly**: Catch specific exceptions, avoid bare `except:` clauses

#### Don'ts ❌
- **Avoid global state**: Use dependency injection and configuration objects instead
- **Don't use mutable default arguments**: Use `None` defaults with conditional assignment
- **Avoid import * **: Always use explicit imports for better code clarity
- **Don't ignore return values**: Always handle or explicitly ignore function returns
- **Avoid deep inheritance**: Prefer composition over inheritance for complex hierarchies
- **Don't hardcode paths**: Use configuration-driven path resolution
- **Avoid magic numbers**: Define constants with descriptive names
- **Don't block event loops**: Never use `time.sleep()` in async contexts

#### Essential Libraries & Patterns
- **torch** (1.13+): Core tensor operations with `torch.compile()` for optimization
- **numpy** (1.24+): Array operations with `np.einsum()` for complex tensor manipulations
- **PIL/Pillow** (10.0+): Image processing with lazy loading patterns
- **psutil**: System resource monitoring for memory/CPU usage tracking
- **pydantic** (2.0+): Data validation and parsing with automatic type coercion
- **structlog**: Structured logging for debugging complex workflows
- **aiofiles**: Async file operations for non-blocking I/O

#### AI-Friendly Code Structure
```python
# Preferred: Clear, descriptive naming with type hints
class TensorProcessorNode:
    """Processes tensor inputs with GPU acceleration."""

    def __init__(self, config: ProcessingConfig) -> None:
        self.config = config
        self._tensor_cache: dict[str, torch.Tensor] = {}

    async def process_batch(
        self,
        inputs: list[torch.Tensor],
        device: torch.device
    ) -> list[torch.Tensor]:
        """Process a batch of tensors with memory optimization."""
        # Implementation with clear variable names
        # and comprehensive error handling
```

## JavaScript Coding Standards & Best Practices

### Core Language Patterns for ComfyUI Frontend

#### Do's ✅
- **Use ES6+ features extensively**: Arrow functions, destructuring, template literals, async/await
- **Implement proper error boundaries**: Use try/catch with specific error types and user-friendly messages
- **Leverage TypeScript interfaces**: Define clear contracts for node properties and configurations
- **Use functional programming patterns**: Pure functions, immutable updates, composition over inheritance
- **Implement proper event delegation**: Use event bubbling and delegation for dynamic elements
- **Structure with modules**: Use ES6 modules with clear export/import patterns
- **Document with JSDoc**: Use comprehensive JSDoc comments for all public APIs
- **Handle async operations properly**: Use Promise.all() for concurrent operations, proper error propagation

#### Don'ts ❌
- **Avoid var declarations**: Always use const/let with block scoping
- **Don't use == comparison**: Always use === for strict equality
- **Avoid global variables**: Use module scope or proper state management
- **Don't manipulate DOM directly**: Use virtual DOM patterns or React-like reconciliation
- **Avoid memory leaks**: Always clean up event listeners and timers
- **Don't block the main thread**: Use Web Workers for heavy computations
- **Avoid deep nesting**: Extract functions or use early returns
- **Don't ignore Promise rejections**: Always handle or explicitly catch async errors

#### Essential Libraries & Patterns
- **LiteGraph.js**: Core graph framework with extension patterns
- **TensorFlow.js** (4.0+): Client-side ML computations with WebGL acceleration
- **RxJS** (7.0+): Reactive programming for complex event streams
- **Lodash** (4.17+): Utility functions with tree-shaking support
- **Zustand** (4.0+): Lightweight state management with immer integration
- **Fabric.js** (6.0+): Canvas manipulation for node visualization
- **D3.js** (7.0+): Advanced data visualization and graph layouts
- **Three.js** (0.150+): 3D rendering for advanced node previews

#### AI-Friendly Code Structure
```javascript
// Preferred: Clear component structure with JSDoc
/**
 * Advanced node configuration widget with reactive updates
 * @extends {LiteGraph.LGraphNode}
 */
class AdvancedConfigNode extends LiteGraph.LGraphNode {
    /**
     * Initialize node with typed properties
     * @param {Object} config - Node configuration object
     */
    constructor(config = {}) {
        super();

        /** @type {string} */
        this.title = config.title || "Advanced Config";

        /** @type {Object.<string, any>} */
        this.properties = { ...config.properties };

        this.setupProperties();
        this.createWidgets();
    }

    /**
     * Setup node properties with validation
     */
    setupProperties() {
        // Implementation with clear method separation
    }
}
```

## AI Model Context Optimization

### Code Patterns for Composer1 Understanding

#### Semantic Naming Conventions
- **Descriptive class/function names**: `ImageUpscaleProcessor` vs `Processor`
- **Clear variable prefixes**: `inputTensor`, `outputBuffer`, `configOptions`
- **Consistent naming patterns**: `camelCase` for JS, `snake_case` for Python
- **Domain-specific terminology**: Use ML/AI terms consistently (`latent_space`, `attention_weights`)

#### Structural Patterns
- **Clear file organization**: Separate concerns into focused modules
- **Progressive complexity**: Start simple, build complexity gradually
- **Comprehensive documentation**: Explain "why" not just "what"
- **Type-driven development**: Explicit types help AI understand data flow

#### Documentation Standards
- **Purpose statements**: Explain node/component purpose in first comment
- **Parameter descriptions**: Document all inputs/outputs with examples
- **Usage examples**: Include code samples in docstrings
- **Architecture decisions**: Explain design choices and trade-offs

#### Error Handling Patterns
- **Descriptive error messages**: Explain what went wrong and potential fixes
- **Recovery suggestions**: Provide actionable guidance for error resolution
- **Logging context**: Include relevant state information in error logs

### Library Integration Guidelines

#### Python Library Stack
```python
# requirements.txt pattern
torch>=2.0.0
torchvision>=0.15.0
numpy>=1.24.0
pillow>=10.0.0
pydantic>=2.0.0
psutil>=5.9.0
aiofiles>=23.0.0
structlog>=23.0.0
```

#### JavaScript Library Stack
```json
{
  "dependencies": {
    "litegraph.js": "^0.7.0",
    "@tensorflow/tfjs": "^4.15.0",
    "rxjs": "^7.8.0",
    "lodash": "^4.17.0",
    "zustand": "^4.4.0",
    "fabric": "^6.0.0",
    "d3": "^7.8.0",
    "three": "^0.158.0"
  }
}
```

## File System Monitoring & PNG Metadata Extraction

### Research Findings: ComfyUI Metadata Formats (2023-2025)

#### Save Image (LoraManager) PNG Metadata Structure
**Primary Format**: JSON embedded in PNG text chunks

- **`parameters` chunk**: Contains generation parameters as JSON string
  ```json
  {
    "prompt": "masterpiece, best quality, <lora:character_v1:0.8>, detailed background...",
    "negative_prompt": "blur, deformed, ugly, low quality",
    "steps": 20,
    "sampler": "euler",
    "cfg_scale": 7.0,
    "seed": 1234567890,
    "size": "512x512"
  }
  ```

- **`workflow` chunk**: Complete ComfyUI workflow as JSON
  ```json
  {
    "nodes": {
      "1": {
        "class_type": "CLIPTextEncode",
        "inputs": {
          "text": "masterpiece, best quality, <lora:character_v1:0.8>"
        }
      },
      "2": {
        "class_type": "LoraLoader",
        "inputs": {
          "lora_name": "character_v1.safetensors",
          "strength_model": 0.8,
          "strength_clip": 1.0
        }
      }
    }
  }
  ```

- **LoRA Storage Format**:
  - Text tags: `<lora:name:strength>` or `<lora:name:model_strength:clip_strength>`
  - Workflow nodes: Separate `strength_model` and `strength_clip` floats
  - Strengths stored as floats: `0.8`, `1.0`, `0.6`, etc.

#### ComfyUI_PromptManager Metadata Patterns
**Dual Extraction Strategy**: Workflow nodes + Text parsing

- **Workflow Node Extraction**:
  - `CLIPTextEncode`: Extracts positive/negative prompts
  - `LoraLoader`: Extracts `lora_name`, `strength_model`, `strength_clip`
  - `CheckpointLoader`: Extracts `ckpt_name`
  - `KSampler`: Extracts `seed`, `steps`, `cfg`, etc.

- **Text Tag Parsing**:
  - `<lora:name:strength>` format detection
  - Regex patterns: `<lora:([^:>]+):([0-9.]+)>`
  - Fallback to workflow data when text parsing fails

- **Metadata Priority**:
  1. Workflow node data (most reliable)
  2. Text tag parsing (for compatibility)
  3. Parameter JSON (legacy fallback)

#### Key LoRA Strength Patterns Observed
```python
# Single strength (model = clip)
"<lora:character_v1:0.8>"

# Dual strengths (model, clip)
"<lora:character_v1:0.6:0.8>"

# Workflow node format
{
  "lora_name": "character_v1.safetensors",
  "strength_model": 0.8,
  "strength_clip": 1.0
}
```

#### Robust Parsing Strategy
```python
def parse_lora_strengths(text_or_node):
    """Parse LoRA strengths from various formats."""
    # Pattern 1: <lora:name:str> or <lora:name:str:str>
    pattern = r'<lora:([^:>]+):([^:>]+)(?::([^:>]+))?>'
    matches = re.findall(pattern, text_or_node, re.IGNORECASE)

    loras = []
    for match in matches:
        name = match[0]
        model_str = float(match[1])
        clip_str = float(match[2]) if match[2] else model_str
        loras.append({
            'name': name,
            'strength_model': model_str,
            'strength_clip': clip_str
        })

    return loras
```

### File System Monitoring Libraries

#### Primary Recommendations (2023-2025)

##### 1. **watchdog** (Most Popular & Cross-Platform)
- **Best for**: General file system monitoring with cross-platform support
- **Version**: `watchdog>=3.0.0`
- **Pros**: Mature, well-tested, comprehensive event types, good Windows support
- **Cons**: Synchronous by default, requires polling on some systems
- **Use case**: ComfyUI output folder monitoring

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ComfyUIWatcher(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.png', '.jpg', '.webp')):
            # Process new image
            pass
```

##### 2. **watchfiles** (High Performance & Async)
- **Best for**: High-performance async monitoring, especially on Linux
- **Version**: `watchfiles>=0.20.0`
- **Pros**: Async-native, better performance, Rust-based backend on Linux
- **Cons**: Newer library, less mature ecosystem
- **Use case**: Production ComfyUI scanners with high throughput

```python
import asyncio
from watchfiles import awatch

async def monitor_outputs():
    async for changes in awatch('/path/to/comfyui/output'):
        for change_type, file_path in changes:
            if str(file_path).endswith('.png'):
                await process_comfyui_image(file_path)
```

##### 3. **pyinotify** (Linux Native Performance)
- **Best for**: Linux-only deployments with maximum performance
- **Version**: `pyinotify>=0.9.6`
- **Pros**: Direct kernel interface, lowest latency, comprehensive events
- **Cons**: Linux-only, complex API
- **Use case**: Dedicated Linux ComfyUI servers

#### Selection Criteria for ComfyUI
- **Cross-platform**: Use `watchdog` for Windows/Mac/Linux compatibility
- **Performance**: Use `watchfiles` for high-throughput scanning
- **Production**: Start with `watchdog`, consider `watchfiles` for optimization

### PNG Metadata Extraction for ComfyUI

#### ComfyUI PNG Structure
ComfyUI embeds metadata in PNG files using multiple text chunks:
- `parameters`: JSON string with generation parameters
- `workflow`: Complete workflow JSON
- `prompt`: Legacy prompt data

#### Best Practices for Extraction

##### 1. **Robust Multi-Format Support**
```python
import json
from PIL import Image
from typing import Optional, Dict, Any

class ComfyUIPNGExtractor:
    """Extract ComfyUI metadata from PNG files with comprehensive error handling."""

    @staticmethod
    def extract_metadata(image_path: str) -> Optional[Dict[str, Any]]:
        """
        Extract ComfyUI metadata from PNG file.

        Args:
            image_path: Path to PNG file

        Returns:
            Dict containing extracted metadata or None if extraction fails
        """
        try:
            with Image.open(image_path) as img:
                if img.format != 'PNG':
                    return None

                metadata = {}

                # Extract from PNG text chunks
                if hasattr(img, 'info') and img.info:
                    # Try workflow first (most comprehensive)
                    if 'workflow' in img.info:
                        try:
                            workflow_data = json.loads(img.info['workflow'])
                            metadata['workflow'] = workflow_data
                        except json.JSONDecodeError:
                            pass

                    # Extract parameters
                    if 'parameters' in img.info:
                        try:
                            params_data = json.loads(img.info['parameters'])
                            metadata['parameters'] = params_data
                        except json.JSONDecodeError:
                            # Fallback: treat as raw text
                            metadata['parameters_raw'] = img.info['parameters']

                    # Legacy prompt support
                    if 'prompt' in img.info:
                        metadata['prompt_legacy'] = img.info['prompt']

                return metadata if metadata else None

        except Exception as e:
            logger.error(f"Failed to extract metadata from {image_path}: {e}")
            return None
```

##### 2. **Structured Data Parsing**
```python
    @staticmethod
    def parse_generation_params(metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Parse generation parameters into structured format."""
        params = {}

        # Handle different metadata sources
        workflow = metadata.get('workflow', {})
        parameters = metadata.get('parameters', {})

        # Extract from workflow nodes (most reliable)
        if 'nodes' in workflow:
            for node in workflow['nodes'].values():
                if node.get('class_type') == 'CLIPTextEncode':
                    # Extract positive prompt
                    if 'inputs' in node and 'text' in node['inputs']:
                        if 'positive' in node['inputs']['text'].lower():
                            params['positive_prompt'] = node['inputs']['text']
                        elif 'negative' in node['inputs']['text'].lower():
                            params['negative_prompt'] = node['inputs']['text']

                elif node.get('class_type') in ['KSampler', 'SamplerCustom']:
                    # Extract generation settings
                    if 'inputs' in node:
                        sampler_inputs = node['inputs']
                        params.update({
                            'steps': sampler_inputs.get('steps'),
                            'cfg_scale': sampler_inputs.get('cfg'),
                            'sampler': sampler_inputs.get('sampler_name'),
                            'scheduler': sampler_inputs.get('scheduler'),
                            'seed': sampler_inputs.get('seed')
                        })

        # Fallback to parameters if workflow parsing fails
        if not params and parameters:
            params.update({
                'positive_prompt': parameters.get('prompt'),
                'negative_prompt': parameters.get('negative_prompt'),
                'steps': parameters.get('steps'),
                'cfg_scale': parameters.get('cfg_scale'),
                'seed': parameters.get('seed')
            })

        return params
```

##### 3. **LoRA and Model Extraction**
```python
    @staticmethod
    def extract_loras_and_models(metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Extract LoRA and model information from ComfyUI metadata."""
        result = {'loras': [], 'models': {}}

        workflow = metadata.get('workflow', {})

        if 'nodes' in workflow:
            for node in workflow['nodes'].values():
                # Extract LoRA information
                if node.get('class_type') == 'LoraLoader':
                    if 'inputs' in node:
                        lora_name = node['inputs'].get('lora_name')
                        strength = node['inputs'].get('strength_model', 1.0)
                        if lora_name:
                            result['loras'].append({
                                'name': lora_name,
                                'strength': strength
                            })

                # Extract checkpoint/model information
                elif node.get('class_type') in ['CheckpointLoaderSimple', 'CheckpointLoader']:
                    if 'inputs' in node:
                        ckpt_name = node['inputs'].get('ckpt_name')
                        if ckpt_name:
                            result['models']['checkpoint'] = ckpt_name

        return result
```

#### Error Handling Best Practices
- **Validate file existence** before attempting extraction
- **Handle corrupted PNGs** gracefully with try/catch
- **Log extraction failures** with detailed error information
- **Provide fallback parsing** when primary methods fail
- **Validate JSON structure** before processing

#### Performance Optimizations
- **Cache extracted metadata** for repeated access
- **Use lazy loading** for large workflow JSON
- **Batch process** multiple files when possible
- **Memory management** for large image files

### Implementation Patterns

#### Async File Monitoring with Metadata Extraction
```python
import asyncio
import os
from pathlib import Path
from typing import Callable, Awaitable

class ComfyUIFileScanner:
    """Asynchronous file scanner for ComfyUI outputs."""

    def __init__(self, output_dir: str, callback: Callable[[str], Awaitable[None]]):
        self.output_dir = Path(output_dir)
        self.callback = callback
        self._watched_files = set()

    async def scan_existing_files(self) -> None:
        """Scan existing files on startup."""
        for file_path in self.output_dir.rglob('*.png'):
            if file_path.is_file():
                await self._process_file(str(file_path))

    async def _process_file(self, file_path: str) -> None:
        """Process a single file for metadata extraction."""
        try:
            metadata = ComfyUIPNGExtractor.extract_metadata(file_path)
            if metadata:
                # Add file path and timestamp to metadata
                metadata['file_path'] = file_path
                metadata['timestamp'] = os.path.getctime(file_path)

                # Call user callback with extracted data
                await self.callback(metadata)
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
```

### Settings Integration with ComfyUI UI

#### Frontend Settings Registration
**Pattern**: Register custom settings in ComfyUI's gear menu for user configuration.

```javascript
// In your web interface JavaScript
function registerSettings() {
    // Wait for ComfyUI app to be available
    const checkForApp = () => {
        if (window.app && window.app.ui && window.app.ui.settings) {
            // Register custom setting
            window.app.ui.settings.addSetting({
                id: "your_node.setting_name",
                name: "Display Name: Setting Label",
                type: "number", // "text", "boolean", "combo", etc.
                defaultValue: 500,
                min: 10,
                max: 10000,
                step: 10,
                tooltip: "Helpful description for users"
            });
        } else {
            setTimeout(checkForApp, 100); // Retry if not ready
        }
    };
    checkForApp();
}
```

#### Backend Settings Access
**Pattern**: Access user settings in Python backend through server integration.

```python
# In your custom node __init__.py
class YourAPIHandler:
    def _get_comfyui_setting(self, setting_id: str, default_value: str):
        """Access ComfyUI setting value through server integration."""
        try:
            # In actual ComfyUI integration:
            # import server
            # return server.PromptServer.instance.settings.get(setting_id, default_value)

            # For development/testing, return default
            return int(default_value)
        except:
            return 500

    async def your_endpoint(self, request):
        """Use setting value in your logic."""
        max_items = self._get_comfyui_setting("your_node.max_items", "500")
        # Use max_items in your processing...
```

#### Settings Types Supported
- **`number`**: Integer/float with min/max/step
- **`text`**: String input
- **`boolean`**: Checkbox toggle
- **`combo`**: Dropdown with options array
- **`slider`**: Visual slider for ranges

#### Best Practices
- **Prefix IDs**: Use `your_node.setting_name` to avoid conflicts
- **Sensible Defaults**: Choose reasonable defaults for all users
- **Validation**: Validate setting values in backend
- **Documentation**: Include helpful tooltips
- **Live Updates**: Consider if settings should apply immediately or require restart

#### Example Implementation
```javascript
// Register in web interface
window.app.ui.settings.addSetting({
    id: "history_guru.max_saved_items",
    name: "History Guru: Max Saved Items",
    type: "number",
    defaultValue: 500,
    min: 10,
    max: 10000,
    step: 10,
    tooltip: "Maximum number of prompt history entries to keep"
});
```

```python
# Use in backend API
async def scan_with_cleanup(self, request):
    max_entries = self._get_comfyui_setting("history_guru.max_saved_items", "500")
    result = self.scanner.scan_and_cleanup(max_entries)
    return web.json_response({"success": True, "data": result})
```

### Registering Custom Static Routes in ComfyUI

#### Why Use ComfyUI's Built-in Web Server

**Preferred Approach**: Use `server.PromptServer.instance.app.router.add_static()` to serve custom web interfaces instead of running separate servers.

```python
# In your custom node's __init__.py setup_routes function
def setup_routes(prompt_server, webapp):
    current_dir = Path(__file__).parent
    web_dir = current_dir / WEB_DIRECTORY

    # Register static routes with ComfyUI's server
    import server
    server.PromptServer.instance.app.router.add_static(
        '/your_extension/',
        path=str(web_dir),
        name='your_extension_static'
    )
```

#### Advantages Over Separate Server

##### 1. **Single Port Architecture**
- **Benefit**: All services run on ComfyUI's port (default 8188)
- **Problem Solved**: No port conflicts or firewall configuration issues
- **User Experience**: One URL to access everything

##### 2. **Unified Authentication & Sessions**
- **Benefit**: Inherits ComfyUI's authentication and session management
- **Security**: Consistent access control across all interfaces
- **Integration**: Seamless experience with existing ComfyUI workflows

##### 3. **Simplified Deployment**
- **No Extra Processes**: No additional server processes to manage
- **Easier Updates**: Custom node updates automatically include web assets
- **Dependency Management**: Leverages ComfyUI's existing web server stack

##### 4. **Better Resource Utilization**
- **Shared Resources**: Uses ComfyUI's existing thread pools and connection handling
- **Memory Efficiency**: No duplicate web server overhead
- **Performance**: Integrated with ComfyUI's async architecture

##### 5. **Consistent CORS & Security**
- **Benefit**: Automatic CORS handling for ComfyUI's domain
- **Security**: Inherits ComfyUI's security policies and headers
- **HTTPS Support**: Automatically supports ComfyUI's SSL configuration

#### Implementation Pattern

```python
# Correct: Use ComfyUI's server
def setup_routes(prompt_server, webapp):
    import server
    web_dir = Path(__file__).parent / './web'
    server.PromptServer.instance.app.router.add_static(
        '/my_extension/',
        path=str(web_dir)
    )
    print("My Extension available at http://127.0.0.1:8188/my_extension/")

# Avoid: Separate server approach
# DON'T DO THIS:
# import subprocess
# subprocess.Popen(['python', 'separate_server.py', '--port', '8189'])
```

#### Common Pitfalls

1. **Path Resolution**: Always use `Path(__file__).parent / WEB_DIRECTORY`
2. **Directory Creation**: Ensure web directory exists: `web_dir.mkdir(exist_ok=True)`
3. **Route Conflicts**: Use unique prefixes like `/your_extension_name/`
4. **File Permissions**: Ensure web assets are readable by ComfyUI process

#### Best Practices

- **Consistent Naming**: Use extension name in route prefix: `/history/`, `/lora_manager/`
- **Error Handling**: Check if web directory exists before registering routes
- **Documentation**: Include access URLs in setup print statements
- **Testing**: Verify routes work with different ComfyUI installations

#### Example Integration

```python
# __init__.py
WEB_DIRECTORY = './web'

def setup_routes(prompt_server, webapp):
    import server
    from pathlib import Path

    web_dir = Path(__file__).parent / WEB_DIRECTORY
    web_dir.mkdir(exist_ok=True)  # Ensure directory exists

    # Register static routes
    server.PromptServer.instance.app.router.add_static(
        '/history/',
        path=str(web_dir),
        name='history_static'
    )

    print("History Guru is live at http://127.0.0.1:8188/history/index.html")
```

This approach ensures seamless integration with ComfyUI's ecosystem while providing professional web interfaces for custom nodes.

## AI Assistant Workflow Rules

### Pre-Development Checklist

**Before making ANY code changes:**

1. ✓ **Create backup** - Run `python backup_file.py <filename>`
2. ✓ **Consult coding references** - Check relevant JSON files for patterns
3. ✓ **Review existing code** - Understand current implementation
4. ✓ **Plan the change** - Know what you're modifying and why
5. ✓ **Run tests** - Ensure current code passes tests before changes

### During Development

1. **Reference consultation:**
   - Check references every 3-5 function implementations
   - Always verify API usage patterns before implementing
   - Use `load_coding_reference.py` to search for patterns

2. **Incremental changes:**
   - Make small, testable changes
   - Test after each significant change
   - Create backups before major refactoring

3. **Error handling:**
   - If you encounter an error, check references first
   - Compare with working backup if needed
   - Document the solution in coding_guru.md

### Post-Development

1. **Testing:**
   - Run `test_guru_manager.py` (or equivalent) before asking user to test
   - Fix any test failures immediately
   - Don't ask user to test until all automated tests pass

2. **Documentation:**
   - Update coding_guru.md with new learnings
   - Document any limitations discovered
   - Note any patterns that worked well

3. **Backup management:**
   - Keep recent backups (last 10-20)
   - Remove very old backups (>30 days) to save space
   - Always keep at least one "known good" backup

### Coding Reference Usage Guidelines

**When to check references:**

| Situation | Reference to Check | Frequency |
|-----------|-------------------|-----------|
| File operations | `coding_reference_js.json` → `file_system_access_api` | Every time |
| Database operations | `coding_reference_js.json` → `indexeddb` | Every time |
| DOM manipulation | `coding_reference_js.json` → `dom_manipulation` | Every 3-5 uses |
| Context menus | `coding_reference_html5.json` → `context_menus` | Every time |
| Drag & drop | `coding_reference_html5.json` → `drag_and_drop` | Every time |
| Keyboard events | `coding_reference_html5.json` → `keyboard_events` | Every time |
| Python file ops | `coding_reference_python.json` → `file_operations` | Every time |
| Image metadata | `coding_reference_python.json` → `image_metadata` | Every time |

**Reference check workflow:**
1. Identify what API/pattern you need
2. Run: `python load_coding_reference.py <lang> <query>`
3. Review the pattern
4. Implement using the pattern
5. If it doesn't work, check backup and compare

### Backup Workflow

**Before every edit session:**
```bash
# Create backup
python backup_file.py "Guru Manager.html"

# List recent backups
python backup_file.py list "Guru Manager"

# Restore if needed
python backup_file.py restore "backup/Guru Manager_20251219_143022.html"
```

**Backup best practices:**
- Always backup before changes
- Keep backups organized by date
- Don't delete backups until changes are confirmed working
- Use backups to compare "before" and "after"

### Documentation Update Rules

**Update coding_guru.md when:**

1. **Immediately (critical learnings):**
   - API limitations discovered
   - Security issues found
   - Breaking changes identified
   - Critical bugs and their fixes

2. **After feature completion:**
   - New patterns that worked well
   - Performance optimizations
   - Better approaches discovered
   - User feedback incorporated

3. **End of session:**
   - Summarize key learnings
   - Document what worked
   - Note what didn't work and why
   - Update patterns section

**What to document:**
- ✅ What you learned (the knowledge)
- ✅ Why it matters (the problem it solves)
- ✅ Code examples (show the pattern)
- ✅ Common pitfalls (what to avoid)
- ✅ Best practices (recommended approach)

**Documentation format:**
```markdown
## [Feature/Pattern Name] (YYYY-MM-DD)

### What I Learned
[Clear description of the learning]

### Why It Matters
[Explanation of why this knowledge is important]

### Code Pattern
```language
[Working code example]
```

### Common Pitfalls
- [Pitfall 1 and how to avoid it]
- [Pitfall 2 and how to avoid it]

### Best Practice
[Recommended approach]
```

#### Updated Library Integration Guidelines

#### Python Library Stack for File Monitoring & PNG Processing
```python
# requirements.txt pattern for ComfyUI scanner
watchdog>=3.0.0              # Cross-platform file monitoring
watchfiles>=0.20.0           # High-performance async monitoring
pillow>=10.0.0               # PNG metadata extraction
pydantic>=2.0.0              # Data validation and parsing
structlog>=23.0.0            # Structured logging
aiofiles>=23.0.0             # Async file operations
psutil>=5.9.0                # System resource monitoring
numpy>=1.24.0                # Image processing support
```

## File System Access API & Single-File HTML Applications (2025)

### Key Learnings from Guru Manager Development

#### 1. **File System Access API Limitations**
**Critical Finding**: Chrome's File System Access API has significant limitations that affect common file operations:

- **Rename Not Supported**: Direct renaming of directories is not possible. The API requires:
  - Copying all contents to a new directory
  - Deleting the old directory
  - This fails with "Name is not allowed" errors in many cases
  - **Solution**: Use drag-and-drop for moving files/folders instead

- **Cut/Paste Complexity**: While technically possible, cut/paste operations require:
  - Maintaining state across context menu interactions
  - Complex path resolution for nested directories
  - Error-prone file handle management
  - **Solution**: Drag-and-drop is more reliable and user-friendly

- **Delete Works Reliably**: `removeEntry()` works well for both files and directories
  - Always requires confirmation for safety
  - Properly updates IndexedDB cache after deletion

#### 2. **Testing Single-File HTML Applications**
**Best Practice**: Create automated testing tools before making changes:

```python
# test_guru_manager.py pattern
def check_function_definitions(js_content):
    """Verify all required functions exist."""
    required_functions = [
        'initFileSystem', 'fullScan', 'setView', 'rend', 'proc',
        'extractText', 'parseMetadata', 'parseComfy', 'parseA1111'
    ]
    # Check each function exists in code
    
def check_syntax_errors(js_content):
    """Basic syntax validation."""
    # Count brackets, parentheses, check template literals
    # Remove strings before counting to avoid false positives
    
def check_dom_access(js_content, html_elements):
    """Verify DOM elements accessed in JS exist in HTML."""
    # Find getElementById calls and verify IDs exist
```

**Key Testing Principles**:
- Test before and after every change
- Check for syntax errors, missing functions, DOM mismatches
- Validate critical functions (initFileSystem, extractText return types)
- Run tests automatically to catch regressions

#### 3. **Metadata Extraction Best Practices**
**Enhanced PNG Metadata Parsing**:

```javascript
// Robust error handling with fallbacks
async function extractText(buffer) {
    try {
        // UTF-8 first
        fullText += new TextDecoder('utf-8').decode(data);
    } catch(e) {
        // Fallback to latin1 for corrupted data
        fullText += new TextDecoder('latin1').decode(data);
    }
    // Always return string for backward compatibility
    return fullText;
}
```

**Key Patterns**:
- Always return consistent types (string, not object) for backward compatibility
- Use try/catch with fallback encodings
- Handle compressed chunks (zTXt) separately
- Support multiple metadata formats (PNG, JPEG, WebP)

#### 4. **State Management in Single-File Apps**
**Effective Patterns**:

```javascript
// Use Maps for fast lookups
let cache = new Map(), fReg = new Map(), dReg = new Map();

// Use Sets for unique collections
let favorites = new Set();

// Persist to localStorage
localStorage.setItem('guru-favorites', JSON.stringify([...favorites]));
localStorage.setItem('guru-theme', theme);

// Restore on load
const savedFavorites = localStorage.getItem('guru-favorites');
if(savedFavorites) {
    favorites = new Set(JSON.parse(savedFavorites));
}
```

**Best Practices**:
- Use Maps for O(1) lookups by key
- Use Sets for unique collections
- Persist user preferences to localStorage
- Restore state on page load

#### 5. **Context Menu Implementation**
**HTML5 Right-Click Menus**:

```javascript
// Prevent default context menu
element.oncontextmenu = (e) => {
    e.preventDefault();
    showContextMenu(e, element, path, isFile);
};

// Position menu at cursor
menu.style.left = e.pageX + 'px';
menu.style.top = e.pageY + 'px';

// Close on outside click
document.addEventListener('click', hideContextMenu, {once: true});
```

**Key Points**:
- Use `oncontextmenu` event (not `contextmenu`)
- Always prevent default browser menu
- Position absolutely at cursor coordinates
- Close menu on outside clicks

#### 6. **Theme System Implementation**
**CSS Custom Properties for Theming**:

```css
:root {
    --bg: #09090b;
    --txt: #e4e4e7;
    /* ... */
}

[data-theme="light"] {
    --bg: #f8f9fa;
    --txt: #202124;
    /* ... */
}

body {
    transition: background-color 0.3s ease, color 0.3s ease;
}
```

**JavaScript Toggle**:
```javascript
function toggleTheme() {
    const currentTheme = body.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('guru-theme', newTheme);
}
```

**Benefits**:
- Single CSS variable change affects entire UI
- Smooth transitions between themes
- Persistent theme selection
- Easy to add new themes

#### 7. **Common Pitfalls to Avoid**

**❌ Don't Change Function Return Types**
```javascript
// BAD: Changing return type breaks existing code
async function extractText(buffer) {
    return {text: fullText, metadata: {...}}; // Breaks proc() function
}

// GOOD: Maintain backward compatibility
async function extractText(buffer) {
    // ... enhanced extraction ...
    return fullText; // Still returns string
}
```

**❌ Don't Override Event Handlers**
```javascript
// BAD: Replacing onclick can break functionality
button.onclick = newFunction; // Loses original handler

// GOOD: Use addEventListener or preserve original
button.addEventListener('click', newFunction);
```

**❌ Don't Assume API Features Work**
```javascript
// BAD: Assuming rename works
await parentHandle.removeEntry(oldName); // Fails in Chrome

// GOOD: Test first, provide alternatives
// Use drag-and-drop for moving/renaming
```

### Suggested Improvements for Guru Manager

#### UI Enhancements

1. **Keyboard Navigation**
   - Arrow keys to navigate grid
   - Enter to open detail view
   - Delete key to delete selected item
   - Tab to cycle through views

2. **Bulk Selection**
   - Ctrl+Click to select multiple images
   - Shift+Click for range selection
   - Bulk delete/favorite operations
   - Visual selection indicators

3. **Image Preview Improvements**
   - Thumbnail loading states (skeleton screens)
   - Lazy loading for large grids
   - Progressive image loading
   - Zoom on hover (lightbox preview)

4. **Search Enhancements**
   - Search history/autocomplete
   - Saved search filters
   - Search within favorites only
   - Regex search support

5. **Metadata Display**
   - Expandable metadata sections
   - Copy metadata to clipboard
   - Export single image metadata
   - Metadata comparison tool

#### Functional Improvements

1. **Performance Optimizations**
   - Virtual scrolling for large image lists
   - Image thumbnail caching
   - Debounced search input
   - Lazy metadata parsing

2. **File Operations**
   - Batch rename (if possible)
   - Duplicate detection by content hash
   - File size display
   - Last modified date sorting

3. **Metadata Features**
   - Metadata editing (update prompts in-place)
   - Metadata validation
   - Missing metadata detection
   - Metadata statistics per folder

4. **Export/Import**
   - Export favorites list
   - Import metadata from JSON
   - Batch export selected images
   - Metadata backup/restore

5. **User Experience**
   - Undo/redo for operations
   - Operation progress indicators
   - Toast notifications instead of alerts
   - Keyboard shortcuts help overlay
