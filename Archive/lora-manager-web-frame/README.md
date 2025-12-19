# ✨ ComfyUI Lora Manager Web Frame

![Setup Guide](setup_guide.png)

A simple custom node that embeds the full [ComfyUI-Lora-Manager](https://github.com/willmiao/ComfyUI-Lora-Manager) web interface directly into your ComfyUI workflow graph. This eliminates the need to have a separate browser tab open for managing your LoRAs and recipes.

## Prerequisites

This node is a wrapper and requires the original extension to be installed and active.

1. Install ComfyUI-Lora-Manager: Use ComfyUI Manager or install manually from [willmiao/ComfyUI-Lora-Manager](https://github.com/willmiao/ComfyUI-Lora-Manager).
2. Verify it works: Ensure you can access the manager at `http://127.0.0.1:8000/loras` (or your specific port) in your browser before using this node.

## Installation

### Option 1: Via ComfyUI Manager (Recommended)
1. Open ComfyUI Manager
2. Search for "Lora Manager Web Frame"
3. Click Install
4. Restart ComfyUI

### Option 2: Manual Installation from ZIP
1. Download the repository as a ZIP file from GitHub
2. Extract the ZIP file
3. Rename the extracted folder from `LoraMangerWebFrame-main` to `LoraMangerWebFrame`
4. Move the renamed folder to your ComfyUI `custom_nodes` directory:
   ```
   ComfyUI/custom_nodes/LoraMangerWebFrame/
   ```
5. Restart ComfyUI

### Option 3: Git Clone
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/revisiontony/LoraMangerWebFrame.git
```

## Usage

1. Add the "✨ Lora Manager Web Frame" node to your workflow
2. The node will display the embedded Lora Manager interface
3. By default, it connects to `http://127.0.0.1:8000/loras`

### Changing the Address

If your ComfyUI instance is running on a different port or remote address, you can update the target URL directly on the node:

1. Click the Address Bar: Click the text input field at the top of the node displaying the URL
2. Edit: Type in your specific address (e.g., `http://127.0.0.1:8000/checkpoints`)
3. Refresh: Click the Update / Go button to reload the embedded frame

### URL Persistence

**The node automatically saves your custom URL!** When you change the URL and save your workflow (Ctrl+S), the custom URL is preserved. The next time you:
- Load the workflow
- Restart ComfyUI
- Share the workflow with others

...the custom URL will be automatically restored. Each node instance can remember its own URL, so you can have multiple nodes pointing to different pages (loras, checkpoints, embeddings, recipes, etc.).

## Example Workflows

Check out the example workflow files included in the repository to see the node in action.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
