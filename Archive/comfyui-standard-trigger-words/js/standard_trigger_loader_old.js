import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

// Helper function to get node from graph
function getNodeFromGraph(graphId, nodeId) {
    const graph = app.graph;
    if (!graph) return null;
    return graph.getNodeById(nodeId);
}

// Setting ID for wheel sensitivity
const TRIGGER_WORD_WHEEL_SENSITIVITY_ID = "standard_trigger.wheel_sensitivity";
const TRIGGER_WORD_WHEEL_SENSITIVITY_DEFAULT = 0.02;

// Get the wheel sensitivity setting value
const getWheelSensitivity = (() => {
    let wheelSettingCache = null;
    let wheelSettingCacheTime = 0;
    const CACHE_DURATION = 5000; // 5 seconds

    return () => {
        const now = Date.now();
        if (wheelSettingCache !== null && now - wheelSettingCacheTime < CACHE_DURATION) {
            return wheelSettingCache;
        }

        const settingManager = app?.extensionManager?.setting;
        if (!settingManager?.get) {
            return TRIGGER_WORD_WHEEL_SENSITIVITY_DEFAULT;
        }

        try {
            wheelSettingCache = settingManager.get(TRIGGER_WORD_WHEEL_SENSITIVITY_ID) ?? TRIGGER_WORD_WHEEL_SENSITIVITY_DEFAULT;
            wheelSettingCacheTime = now;
            return wheelSettingCache;
        } catch {
            return TRIGGER_WORD_WHEEL_SENSITIVITY_DEFAULT;
        }
    };
})();

// Simple tags widget implementation
function createTagsWidget(node, name, options = {}) {
    const widget = node.addCustomWidget({
        name: name,
        type: "tags",
        value: [],
        options: options,
        
        draw(ctx, node, width, y) {
            try {
                const value = this.value || [];
                const margin = 10;
                const tagHeight = 30;
                const tagMargin = 5;
                let currentX = margin;
                let currentY = y;
                const maxWidth = width - margin * 2;
                
                ctx.font = "14px Arial";
            
            value.forEach((tag, index) => {
                const text = tag.text || "";
                const isActive = tag.active !== false;
                const isHighlighted = tag.highlighted === true;
                
                // Measure text
                const textWidth = ctx.measureText(text).width;
                const tagWidth = textWidth + 20;
                
                // Wrap to next line if needed
                if (currentX + tagWidth > maxWidth && currentX > margin) {
                    currentX = margin;
                    currentY += tagHeight + tagMargin;
                }
                
                // Draw tag background
                ctx.fillStyle = isActive ? (isHighlighted ? "#4a7c59" : "#2a4a3a") : "#3a3a3a";
                ctx.fillRect(currentX, currentY, tagWidth, tagHeight);
                
                // Draw border for highlighted
                if (isHighlighted) {
                    ctx.strokeStyle = "#6fa866";
                    ctx.lineWidth = 2;
                    ctx.strokeRect(currentX, currentY, tagWidth, tagHeight);
                }
                
                // Draw text
                ctx.fillStyle = isActive ? "#ffffff" : "#888888";
                ctx.fillText(text, currentX + 10, currentY + 20);
                
                currentX += tagWidth + tagMargin;
            });
            
            return currentY + tagHeight + tagMargin - y;
            } catch (e) {
                console.error("Error drawing tags widget:", e);
                // Draw error state
                ctx.fillStyle = "#ff0000";
                ctx.fillText("Error rendering tags", 10, y + 20);
                return 40;
            }
        },
        
        computeSize(width) {
            const value = this.value || [];
            if (value.length === 0) return [width, 40];
            
            // Estimate height based on number of tags
            const estimatedRows = Math.ceil(value.length / 5);
            return [width, Math.max(40, estimatedRows * 40)];
        },
        
        mouse(event, pos, node) {
            if (event.type === "pointerdown") {
                const value = this.value || [];
                const margin = 10;
                const tagHeight = 30;
                const tagMargin = 5;
                let currentX = margin;
                let currentY = 0;
                const maxWidth = node.size[0] - margin * 2;
                
                const ctx = app.canvas.getContext("2d");
                ctx.font = "14px Arial";
                
                for (let i = 0; i < value.length; i++) {
                    const tag = value[i];
                    const text = tag.text || "";
                    const textWidth = ctx.measureText(text).width;
                    const tagWidth = textWidth + 20;
                    
                    if (currentX + tagWidth > maxWidth && currentX > margin) {
                        currentX = margin;
                        currentY += tagHeight + tagMargin;
                    }
                    
                    // Check if click is within this tag
                    if (pos[0] >= currentX && pos[0] <= currentX + tagWidth &&
                        pos[1] >= currentY && pos[1] <= currentY + tagHeight) {
                        // Toggle active state
                        tag.active = !tag.active;
                        this.value = [...value]; // Trigger update
                        node.setDirtyCanvas(true, true);
                        return true;
                    }
                    
                    currentX += tagWidth + tagMargin;
                }
            }
            return false;
        },
        
        serializeValue() {
            try {
                const value = this.value || [];
                // Ensure we return a valid array
                if (!Array.isArray(value)) {
                    console.warn("Widget value is not an array, resetting to empty array");
                    return [];
                }
                return value;
            } catch (e) {
                console.error("Error serializing widget value:", e);
                return [];
            }
        }
    });
    
    return { widget };
}

// Standard Trigger Words Loader extension
app.registerExtension({
    name: "StandardTriggerWordsLoader",
    
    setup() {
        // Add message handler to listen for trigger word updates
        if (!this._triggerUpdateHandler) {
            this._triggerUpdateHandler = (event) => {
                const { id, graph_id: graphId, trigger_words } = event.detail;
                this.handleTriggerWordUpdate(id, graphId, trigger_words);
            };
            api.addEventListener("standard_trigger_update", this._triggerUpdateHandler);
        }
    },
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "StandardTriggerWordsLoader") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // Add connection validation
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                const result = onConnectionsChange?.apply(this, arguments);
                
                if (type === 1 && connected && link_info) { // Input connection
                    const inputName = this.inputs[index]?.name;
                    if ((inputName === "trigger_words" || inputName === "input_string") && link_info) {
                        const originNode = this.graph?.getNodeById(link_info.origin_id);
                        const originType = originNode?.outputs[link_info.origin_slot]?.type;
                        
                        if (originType && originType !== "STRING" && originType !== "*") {
                            console.warn(`Warning: Expected STRING input for ${inputName}, got ${originType}`);
                        }
                    }
                }
                
                return result;
            };
            
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated?.apply(this, arguments);
                
                // Enable widget serialization
                this.serialize_widgets = true;
                
                requestAnimationFrame(() => {
                    // Get widgets
                    const presetCategoryWidget = this.widgets.find(w => w.name === "preset_category");
                    const defaultActiveWidget = this.widgets.find(w => w.name === "default_active");
                    const strengthAdjustmentWidget = this.widgets.find(w => w.name === "allow_strength_adjustment");
                    
                    // Add tags widget
                    const tagsResult = createTagsWidget(this, "modify_tags", {
                        defaultVal: []
                    });
                    
                    this.tagWidget = tagsResult.widget;
                    
                    // Add hidden widgets
                    const hiddenTriggerWordsWidget = this.addWidget('text', 'original_trigger_words', '', () => {}, {
                        serialize: true
                    });
                    this.originalTriggerWordsWidget = hiddenTriggerWordsWidget;

                    const hiddenReloadWidget = this.addWidget('toggle', 'reload_presets', false, () => {}, {
                        serialize: true
                    });
                    this.reloadPresetsWidget = hiddenReloadWidget;

                    // Preset category callback
                    if (presetCategoryWidget) {
                        const originalCallback = presetCategoryWidget.callback;
                        presetCategoryWidget.callback = (value) => {
                            if (this.reloadPresetsWidget) {
                                this.reloadPresetsWidget.value = true;
                            }
                            this.setDirtyCanvas(true, true);
                            if (originalCallback) {
                                originalCallback.call(presetCategoryWidget, value);
                            }
                        };
                    }

                    // Default active callback
                    if (defaultActiveWidget) {
                        defaultActiveWidget.callback = (value) => {
                            if (this.tagWidget && this.tagWidget.value) {
                                const updatedTags = this.tagWidget.value.map(tag => ({
                                    ...tag,
                                    active: value
                                }));
                                this.tagWidget.value = updatedTags;
                                this.setDirtyCanvas(true, true);
                            }
                        };
                    }
                    
                    // Add batch operation buttons
                    this.addWidget("button", "Toggle All ON", null, () => {
                        if (this.tagWidget?.value) {
                            this.tagWidget.value.forEach(tag => tag.active = true);
                            this.tagWidget.value = [...this.tagWidget.value];
                            this.setDirtyCanvas(true, true);
                        }
                    });

                    this.addWidget("button", "Toggle All OFF", null, () => {
                        if (this.tagWidget?.value) {
                            this.tagWidget.value.forEach(tag => tag.active = false);
                            this.tagWidget.value = [...this.tagWidget.value];
                            this.setDirtyCanvas(true, true);
                        }
                    });

                    this.addWidget("button", "Clear All", null, () => {
                        if (this.tagWidget) {
                            this.tagWidget.value = [];
                            this.setDirtyCanvas(true, true);
                        }
                    });
                });
                
                return result;
            };
        }
    },

    handleTriggerWordUpdate(id, graphId, triggerWords) {
        const node = getNodeFromGraph(graphId, id);
        if (!node) {
            console.warn("Node not found:", id);
            return;
        }
        
        if (node.originalTriggerWordsWidget) {
            node.originalTriggerWordsWidget.value = triggerWords;
        }

        if (triggerWords && node.tagWidget) {
            const wordsArray = triggerWords.split(',,').map(w => w.trim()).filter(w => w);
            // Highlight new trigger words
            if (node.tagWidget.value) {
                node.tagWidget.value.forEach(tag => {
                    tag.highlighted = wordsArray.some(w => 
                        w.toLowerCase().includes(tag.text.toLowerCase())
                    );
                });
            }
        }
        
        node.setDirtyCanvas(true, true);
    },
});
