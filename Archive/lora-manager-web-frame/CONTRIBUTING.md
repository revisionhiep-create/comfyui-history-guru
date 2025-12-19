### 2. `CONTRIBUTING.md`
This is a standard template suitable for a small custom node project.

```markdown
# Contributing to ComfyUI Lora Manager Web Frame

Thank you for your interest in contributing! This project is a simple wrapper to improve the UI experience of ComfyUI, and we welcome help to make it better.

## How to Contribute

### Reporting Bugs
If you find a bug (e.g., the frame remains blank, resizing is jittery), please open an issue on GitHub.
* **Check existing issues** to see if it has already been reported.
* **Include logs:** Share any errors from your browser console (`F12` > Console) or ComfyUI terminal.
* **Describe your setup:** Are you using the Portable Version, Desktop App (Electron), or a standard Python install?

### Suggesting Enhancements
Have an idea to make the frame smarter? Open an issue using the "Feature Request" label.

### Pull Requests
1.  **Fork** the repository.
2.  **Clone** your fork locally.
3.  Create a new **branch** for your feature or fix (`git checkout -b feature/amazing-feature`).
4.  Commit your changes (`git commit -m 'Add some amazing feature'`).
5.  **Push** to the branch (`git push origin feature/amazing-feature`).
6.  Open a **Pull Request**.

## Coding Guidelines
* **JavaScript:** This node relies heavily on the ComfyUI frontend API. Please ensure any JS changes are tested on both Chrome and the ComfyUI Desktop App (Electron) if possible.
* **Clean Code:** Keep the iframe resizing logic debounced to avoid performance hits.

## Code of Conduct
Please be respectful and kind to other contributors. We are all here to learn and create cool AI art tools.
