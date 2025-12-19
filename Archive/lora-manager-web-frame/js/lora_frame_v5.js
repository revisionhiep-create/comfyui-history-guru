import { app } from "../../scripts/app.js";

app.registerExtension({
	name: "Comfy.LoraWebFrame",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "LoraWebFrame") {
			const onNodeCreated = nodeType.prototype.onNodeCreated;
			
			nodeType.prototype.onNodeCreated = function () {
				const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

				// Configuration
				const defaultUrl = "http://127.0.0.1:8000/loras";
				let resizeTimer;

				// Widget Setup - Load saved URL from workflow or use default
				const savedUrl = this.widgets_values?.[0] ?? defaultUrl;
				const urlWidget = this.addWidget("text", "URL", savedUrl, () => {}, {});
				
				this.addWidget("button", "Update / Go", null, () => {
					loadURL(urlWidget.value);
				});

				// Create iframe with security sandbox
				const iframe = document.createElement("iframe");
				iframe.setAttribute("sandbox", "allow-scripts allow-forms allow-same-origin allow-popups allow-presentation");
				iframe.setAttribute("loading", "lazy");
				
				Object.assign(iframe.style, {
					width: "100%",
					height: "100%",
					border: "none",
					display: "block",
					backgroundColor: "#222"
				});

				// Error handling for iframe load failures
				iframe.addEventListener("error", () => {
					console.error("LoraWebFrame: Failed to load URL", iframe.src);
				});

				// Wrapper container
				const wrapper = document.createElement("div");
				Object.assign(wrapper.style, {
					width: "100%",
					height: "200px",
					overflow: "hidden"
				});
				wrapper.appendChild(iframe);

				const domWidget = this.addDOMWidget("lora_iframe", "div", wrapper, {
					serialize: false,
					hideOnZoom: false
				});

				// Helper function with URL validation
				function loadURL(url) {
					if (!url || iframe.src === url) return;
					
					try {
						new URL(url);
						iframe.src = url;
					} catch (e) {
						console.error("LoraWebFrame: Invalid URL", url);
					}
				}

				// Efficient resizing with requestAnimationFrame
				this.onResize = function (size) {
					if (resizeTimer) cancelAnimationFrame(resizeTimer);
					
					resizeTimer = requestAnimationFrame(() => {
						const safeHeight = Math.max(size[1] - 90, 100);
						
						if (wrapper.style.height !== safeHeight + "px") {
							wrapper.style.height = safeHeight + "px";
							domWidget.element.style.height = safeHeight + "px";
						}
					});
				};

				// Cleanup handler
				this.onRemoved = function () {
					if (resizeTimer) cancelAnimationFrame(resizeTimer);
					if (iframe) iframe.src = "";
				};

				// Delayed startup to allow ComfyUI initialization
				setTimeout(() => {
					if (this.size[0] < 200) {
						this.setSize([1200, 900]);
					}
					loadURL(urlWidget.value);
					this.onResize(this.size);
				}, 1000);

				return r;
			};
		}
	},
});