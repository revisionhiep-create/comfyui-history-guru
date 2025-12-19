# History Guru 🧘‍♂️ v3 (Universal Editor)

> **The 100% Offline, Serverless Metadata Viewer & Editor for ComfyUI Images.**

**History Guru** is a single-file HTML5 application that lets you browse, search, inspect, **and now EDIT** the hidden metadata (Prompts, LoRAs, Seeds, Models) inside your AI-generated images.

![How History Guru Works](infograph.png)

It runs entirely in your browser. No data is ever uploaded. No internet connection is required.

## ✨ Features

* **⚡ Instant Search:** Filter thousands of images by Prompt, Model Name, Seed, or LoRA Name in milliseconds.
* **✏️ Metadata Editor (New):** View missing or "screwed up" metadata? You can now manually edit the fields (Prompt, Seed, Steps, etc.) directly in the sidebar.
* **💾 Fix & Download (New):** The **"Fix & Download Image"** button takes your edited metadata, re-encodes it into a standard A1111-compatible PNG chunk, and saves a repaired copy of your image. Perfect for fixing images where Photoshop stripped the data.
* **🕸️ Deep Recursive Tracing:** Uses a new recursive engine to trace upstream nodes. It can find prompts hidden behind `SeedVarianceEnhancers`, `Logic Gates`, or complex `Lora Stackers`.
* **👁️ Preview Image Support:** Now fully supports images saved via the `PreviewImage` node, not just `SaveImage`.
* **🔒 100% Private:** Zero server uploads. Your images never leave your hard drive.
* **♾️ Infinite Scroll:** Capable of handling folders with 5,000+ images without crashing your browser.

## 🚀 Quick Start

1.  **Download** the `guru.html` file from this repository.
2.  **Open** `guru.html` in any modern web browser (Chrome, Edge, Firefox).
3.  Click **"Load Folder"** and select your output directory.
4.  **Edit & Fix:** Click any image to open the sidebar. If the metadata is wrong or missing, type in the correct values and click **"Fix & Download Image"** to save a corrected copy.

## ⚠️ Important Requirements

### 1. Browser Security (Why it downloads a copy)
Browsers (Chrome/Firefox) run in a secure sandbox. They **cannot** overwrite files on your hard drive directly.
* When you click "Fix & Download", History Guru generates a **new** PNG file with the corrected metadata injected and downloads it to your default downloads folder.

### 2. Supported Nodes
History Guru v3 is designed to be "Universal," but works best with:
* **Standard KSampler** workflows.
* **rgthree Power Lora Loader** (explicitly supported).
* **Lora Manager** stackers.
* **A1111 / Forge** generated images.

## 🔧 Technical Details

History Guru uses a custom **"Scorched Earth"** parsing engine written in vanilla JavaScript:
* **Recursive Node Tracing:** Traces `positive` -> `conditioning` -> `node` links upwards endlessly until it finds the original text prompt.
* **PNG Chunk Injection:** Calculates valid CRC32 checksums to insert new `tEXt` chunks into existing PNG binaries without re-encoding the image pixel data (lossless patching).
* **Native Decompression:** Uses the browser's `DecompressionStream` API to unzip compressed metadata chunks (`zTXt`).

## 🤝 Contributing

Feel free to fork this repository and submit Pull Requests.

**License:** MIT
