/**
 * Prompt Library Viewer - WebFrame Pattern
 * Displays the web UI in an iframe
 */

import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "comfyui.promptlibraryviewer",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "PromptLibraryViewer") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated?.apply(this, arguments);
                
                // Set node size
                this.setSize([1100, 850]);
                
                // Add URL widget (hidden, but stores the URL)
                const urlWidget = this.addWidget("text", "url", "http://127.0.0.1:8188/prompt_library", () => {});
                urlWidget.hidden = true;
                
                // Add reload button
                const reloadBtn = this.addWidget("button", "🔄 Reload", "reload", () => {
                    if (this.iframeWidget) {
                        const iframe = this.iframeWidget.element;
                        if (iframe && iframe.contentWindow) {
                            iframe.contentWindow.location.reload();
                        }
                    }
                });
                
                // Create iframe widget
                const iframeElement = document.createElement("iframe");
                iframeElement.src = urlWidget.value;
                iframeElement.style.cssText = `
                    width: 100%;
                    height: 800px;
                    border: none;
                    border-radius: 5px;
                    background: #1a1a1a;
                `;
                
                // Security sandbox
                iframeElement.sandbox = "allow-scripts allow-same-origin allow-forms";
                
                // Handle iframe load errors
                iframeElement.onerror = () => {
                    console.error("[Prompt Library Viewer] Failed to load web UI");
                };
                
                // Add iframe as DOM widget
                this.iframeWidget = this.addDOMWidget("prompt_library_iframe", "iframe", iframeElement, {
                    serialize: false,
                    hideOnZoom: false
                });
                
                // Store reference for cleanup
                this.iframeElement = iframeElement;
                
                return result;
            };
            
            // Cleanup on node removal
            const onRemoved = nodeType.prototype.onRemoved;
            nodeType.prototype.onRemoved = function() {
                if (this.iframeElement) {
                    this.iframeElement.remove();
                    this.iframeElement = null;
                }
                return onRemoved?.apply(this, arguments);
            };
        }
    }
});
