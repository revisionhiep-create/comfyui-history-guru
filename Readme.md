# History Guru 🧘‍♂️

> **The 100% Offline, Serverless Metadata Viewer for ComfyUI Images.**

**History Guru** is a single-file HTML5 application that lets you browse, search, and inspect the hidden metadata (Prompts, LoRAs, Seeds, Models) inside your AI-generated images.

![How History Guru Works](infograph.png)

It runs entirely in your browser. No data is ever uploaded. No internet connection is required.

## ✨ Features

* **⚡ Instant Search:** Filter thousands of images by Prompt, Model Name, Seed, or LoRA Name in milliseconds.
* **🔒 100% Private:** Zero server uploads. Your images never leave your hard drive.
* **♾️ Infinite Scroll:** Capable of handling folders with 5,000+ images without crashing your browser.
* **🛠️ Deep Inspection:** Reads hidden data from complex workflows, including **LoRA Manager** stacker lists and compressed `zTXt` chunks.
* **📱 Modern UI:** Dark mode interface with transparency support and a "focus mode" sidebar.

## 🚀 Quick Start

1.  **Download** the `guru.html` file from this repository.
2.  **Open** `guru.html` in any modern web browser (Chrome, Edge, Firefox).
3.  Click **"Load Folder"** and select your output directory (e.g., `ComfyUI/output`).
4.  **Grant Permission:** Your browser will ask to view the files. Click "View Files" or "Upload" (don't worry, nothing is actually uploading to the internet; it's a local permission request).

## ⚠️ Important Requirements

### 1. The "Save Image" Node
For History Guru to detect your metadata, the data must actually exist in the file.
* **Recommended:** Use the **`Save Image (LoraManager)`** node. This tool is heavily optimized to read the specific `widgets_values` structure used by the LoRA Manager extension.
* **Standard:** The standard `Save Image` node works for basic prompts, but might miss complex LoRA names hidden in custom nodes.

### 2. Do Not "Modify" the PNG
Metadata is fragile. It lives in the binary chunks of the PNG file.
* ❌ **Do NOT** open and re-save the image in Photoshop, Paint, or generic photo editors. This often strips the metadata permanently.
* ✅ You can rename or move the files, but do not re-encode them.

## 🔧 Technical Details

History Guru uses a custom **"Scorched Earth"** parsing engine written in vanilla JavaScript:
* **Native Decompression:** Uses the browser's `DecompressionStream` API to unzip compressed metadata chunks (`zTXt`) without external libraries.
* **Hybrid Regex:** Uses a combination of JSON object scanning and regex pattern matching to find `<lora:name:1.0>` tags even in broken or non-standard metadata formats.
* **No Dependencies:** Zero external CSS or JS links. Works on air-gapped machines.

## 🤝 Contributing

Feel free to fork this repository and submit Pull Requests.

**License:** MIT
