import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";
import { CONVERTED_TYPE, getNodeFromGraph } from "./utils.js";
import { addTagsWidget } from "./tags_widget.js";

// Setting ID for wheel sensitivity (reuse from trigger word toggle)
const MODIFY_STRING_WHEEL_SENSITIVITY_ID = "loramanager.trigger_word_wheel_sensitivity";
const MODIFY_STRING_WHEEL_SENSITIVITY_DEFAULT = 0.02;

// Get the wheel sensitivity setting value
const getWheelSensitivity = (() => {
    let settingsUnavailableLogged = false;

    return () => {
        const settingManager = app?.extensionManager?.setting;
        if (!settingManager || typeof settingManager.get !== "function") {
            if (!settingsUnavailableLogged) {
                console.warn("LoRA Manager: settings API unavailable, using default wheel sensitivity.");
                settingsUnavailableLogged = true;
            }
            return MODIFY_STRING_WHEEL_SENSITIVITY_DEFAULT;
        }

        try {
            const value = settingManager.get(MODIFY_STRING_WHEEL_SENSITIVITY_ID);
            return value ?? MODIFY_STRING_WHEEL_SENSITIVITY_DEFAULT;
        } catch (error) {
            if (!settingsUnavailableLogged) {
                console.warn("LoRA Manager: unable to read wheel sensitivity setting, using default.", error);
                settingsUnavailableLogged = true;
            }
            return MODIFY_STRING_WHEEL_SENSITIVITY_DEFAULT;
        }
    };
})();

// Preset categories from Python
const PRESET_CATEGORIES = [
    "All", "Quality", "Lighting", "Composition", "Style", "Detail", "Aesthetic", "Motion"
];

// ModifyString extension for ComfyUI
app.registerExtension({
    name: "LoraManager.ModifyString",
    
    setup() {
        // Add message handler to listen for trigger word updates from Lora Loader
        // Use singleton pattern to prevent memory leaks from multiple listeners
        if (!this._triggerUpdateHandler) {
            this._triggerUpdateHandler = (event) => {
                const { id, graph_id: graphId, trigger_words } = event.detail;
                this.handleTriggerWordUpdate(id, graphId, trigger_words);
            };
            api.addEventListener("modify_string_trigger_update", this._triggerUpdateHandler);
        }
    },
    
    async nodeCreated(node) {
        if (node.comfyClass === "Modify String (LoraManager)") {
            // Enable widget serialization
            node.serialize_widgets = true;
            
            // Add optional inputs
            node.addInput("input_string", 'STRING', {
                "shape": 7  // 7 is the shape of the optional input
            });
            
            node.addInput("trigger_words", 'STRING', {
                "shape": 7  // Optional input from Lora Loader
            });

            // Wait for node to be properly initialized
            requestAnimationFrame(async () => {
                // Get the wheel sensitivity setting
                const wheelSensitivity = getWheelSensitivity();
                
                // Get widgets
                const presetCategoryWidget = node.widgets.find(w => w.name === "preset_category");
                const modeWidget = node.widgets.find(w => w.name === "mode");
                const separatorWidget = node.widgets.find(w => w.name === "separator");
                const mergeStrategyWidget = node.widgets.find(w => w.name === "merge_strategy");
                const deduplicateWidget = node.widgets.find(w => w.name === "deduplicate");
                const defaultActiveWidget = node.widgets.find(w => w.name === "default_active");
                const strengthAdjustmentWidget = node.widgets.find(w => w.name === "allow_strength_adjustment");
                
                const initialStrengthAdjustment = Boolean(strengthAdjustmentWidget?.value);
                
                // Add tags widget for managing trigger words
                const result = addTagsWidget(node, "modify_tags", {
                    defaultVal: []
                }, null, wheelSensitivity, {
                    allowStrengthAdjustment: initialStrengthAdjustment,
                    allowEditing: true  // Enable inline editing
                });
                
                node.tagWidget = result.widget;
                node.tagWidget.allowStrengthAdjustment = initialStrengthAdjustment;
                node.tagWidget.allowEditing = true;

                // Helper function to normalize text for comparison
                const normalizeTagText = (text) =>
                    (typeof text === 'string' ? text.trim().toLowerCase() : '');

                // Helper to collect highlight tokens
                const collectHighlightTokens = (wordsArray) => {
                    const tokens = new Set();

                    const addToken = (text) => {
                        const normalized = normalizeTagText(text);
                        if (normalized) {
                            tokens.add(normalized);
                        }
                    };

                    wordsArray.forEach((rawWord) => {
                        if (typeof rawWord !== 'string') {
                            return;
                        }

                        addToken(rawWord);

                        // Handle grouped words
                        const groupParts = rawWord.split(/,{2,}/);
                        groupParts.forEach((groupPart) => {
                            addToken(groupPart);
                            groupPart.split(',').forEach(addToken);
                        });

                        rawWord.split(',').forEach(addToken);
                    });

                    return tokens;
                };

                // Apply highlight state to tags
                const applyHighlightState = () => {
                    if (!node.tagWidget) return;
                    const highlightSet = node._highlightedTriggerWords || new Set();
                    const updatedTags = (node.tagWidget.value || []).map(tag => ({
                        ...tag,
                        highlighted: highlightSet.size > 0 && highlightSet.has(normalizeTagText(tag.text))
                    }));
                    node.tagWidget.value = updatedTags;
                };

                // Function to highlight trigger words from Lora
                node.highlightTriggerWords = (triggerWords) => {
                    const wordsArray = Array.isArray(triggerWords)
                        ? triggerWords
                        : triggerWords
                            ? [triggerWords]
                            : [];
                    node._highlightedTriggerWords = collectHighlightTokens(wordsArray);
                    applyHighlightState();
                };

                if (node.__pendingHighlightWords !== undefined) {
                    const pending = node.__pendingHighlightWords;
                    delete node.__pendingHighlightWords;
                    node.highlightTriggerWords(pending);
                }

                node.applyTriggerHighlightState = applyHighlightState;

                // Add hidden widget to store original trigger words from Lora Loader
                const hiddenTriggerWordsWidget = node.addWidget('text', 'original_trigger_words', '');
                hiddenTriggerWordsWidget.type = CONVERTED_TYPE;
                hiddenTriggerWordsWidget.hidden = true;
                hiddenTriggerWordsWidget.computeSize = () => [0, -4];
                node.originalTriggerWordsWidget = hiddenTriggerWordsWidget;

                // Add hidden widget to track if presets should be reloaded
                const hiddenReloadWidget = node.addWidget('BOOLEAN', 'reload_presets', false);
                hiddenReloadWidget.type = CONVERTED_TYPE;
                hiddenReloadWidget.hidden = true;
                hiddenReloadWidget.computeSize = () => [0, -4];
                node.reloadPresetsWidget = hiddenReloadWidget;

                // Restore saved values if they exist
                const tagWidgetIndex = node.widgets.indexOf(result.widget);
                const originalTriggerWordsIndex = node.widgets.indexOf(hiddenTriggerWordsWidget);
                const reloadPresetsIndex = node.widgets.indexOf(hiddenReloadWidget);
                
                if (node.widgets_values && node.widgets_values.length > 0) {
                    if (tagWidgetIndex >= 0) {
                        const savedValue = node.widgets_values[tagWidgetIndex];
                        if (savedValue) {
                            result.widget.value = Array.isArray(savedValue) ? savedValue : [];
                        }
                    }
                    if (originalTriggerWordsIndex >= 0) {
                        const originalTriggerWords = node.widgets_values[originalTriggerWordsIndex];
                        if (originalTriggerWords) {
                            hiddenTriggerWordsWidget.value = originalTriggerWords;
                        }
                    }
                    if (reloadPresetsIndex >= 0) {
                        const reloadPresets = node.widgets_values[reloadPresetsIndex];
                        if (reloadPresets !== undefined) {
                            hiddenReloadWidget.value = reloadPresets;
                        }
                    }
                }

                requestAnimationFrame(() => node.applyTriggerHighlightState?.());

                // Callback for preset category changes
                if (presetCategoryWidget) {
                    const originalCallback = presetCategoryWidget.callback;
                    presetCategoryWidget.callback = async (value) => {
                        // Set reload flag to trigger preset loading in Python
                        if (node.reloadPresetsWidget) {
                            node.reloadPresetsWidget.value = true;
                        }
                        // Mark canvas as dirty to trigger re-execution
                        node.setDirtyCanvas(true, true);
                        if (originalCallback) {
                            originalCallback.call(presetCategoryWidget, value);
                        }
                    };
                }

                // Callback for default_active widget
                if (defaultActiveWidget) {
                    defaultActiveWidget.callback = (value) => {
                        // Set all existing tags' active state to the new value
                        if (node.tagWidget && node.tagWidget.value) {
                            const updatedTags = node.tagWidget.value.map(tag => ({
                                ...tag,
                                active: value
                            }));
                            node.tagWidget.value = updatedTags;
                            node.applyTriggerHighlightState?.();
                        }
                    };
                }
                
                // Callback for strength adjustment toggle
                if (strengthAdjustmentWidget) {
                    strengthAdjustmentWidget.callback = (value) => {
                        const allowStrengthAdjustment = Boolean(value);
                        if (node.tagWidget) {
                            node.tagWidget.allowStrengthAdjustment = allowStrengthAdjustment;
                        }
                    };
                }
                
                // Override the serializeValue method to properly format trigger words with strength
                const originalSerializeValue = result.widget.serializeValue;
                result.widget.serializeValue = function() {
                    const value = this.value || [];
                    // Transform the values to include strength in the proper format if needed
                    const transformedValue = value.map(tag => {
                        // If strength is defined and strength adjustment is enabled
                        if (tag.strength !== undefined && tag.strength !== null && 
                            node.tagWidget.allowStrengthAdjustment) {
                            return {
                                ...tag,
                                // Keep text as-is, backend will format it
                                text: tag.text
                            };
                        }
                        return tag;
                    });
                    return transformedValue;
                };

                // Add custom button to load presets
                this.addLoadPresetButton(node);
                
                // Add batch operation buttons
                this.addBatchOperationButtons(node);
            });
        }
    },

    // Handle trigger word updates from Lora Loader
    handleTriggerWordUpdate(id, graphId, triggerWords) {
        const node = getNodeFromGraph(graphId, id);
        if (!node || node.comfyClass !== "Modify String (LoraManager)") {
            console.warn("Node not found or not a ModifyString:", id);
            return;
        }
        
        // Store the original trigger words
        if (node.originalTriggerWordsWidget) {
            node.originalTriggerWordsWidget.value = triggerWords;
        }

        // Highlight the new trigger words from Lora
        if (triggerWords) {
            const wordsArray = triggerWords.split(',,').map(w => w.trim()).filter(w => w);
            node.highlightTriggerWords(wordsArray);
        }
        
        // Mark canvas as dirty to trigger re-execution
        node.setDirtyCanvas(true, true);
    },

    // Load preset tags for a category
    async loadPresetCategory(node, category, defaultActive) {
        if (!node.tagWidget) return;
        
        // Set reload flag to trigger preset loading in Python
        if (node.reloadPresetsWidget) {
            node.reloadPresetsWidget.value = true;
        }
        
        // Trigger a node update to reload presets from Python
        node.setDirtyCanvas(true, true);
    },

    // Add a button to manually load presets
    addLoadPresetButton(node) {
        const loadButton = node.addWidget("button", "Load Presets", null, () => {
            const presetCategoryWidget = node.widgets.find(w => w.name === "preset_category");
            const defaultActiveWidget = node.widgets.find(w => w.name === "default_active");
            
            if (presetCategoryWidget) {
                this.loadPresetCategory(
                    node,
                    presetCategoryWidget.value,
                    defaultActiveWidget?.value ?? true
                );
            }
        });
        
        loadButton.serialize = false; // Don't save button state
    },

    // Add buttons for batch operations
    addBatchOperationButtons(node) {
        // Toggle all on
        const toggleAllOnButton = node.addWidget("button", "Toggle All ON", null, () => {
            if (node.tagWidget && node.tagWidget.value) {
                const updatedTags = node.tagWidget.value.map(tag => ({
                    ...tag,
                    active: true
                }));
                node.tagWidget.value = updatedTags;
                node.applyTriggerHighlightState?.();
                node.setDirtyCanvas(true);
            }
        });
        toggleAllOnButton.serialize = false;

        // Toggle all off
        const toggleAllOffButton = node.addWidget("button", "Toggle All OFF", null, () => {
            if (node.tagWidget && node.tagWidget.value) {
                const updatedTags = node.tagWidget.value.map(tag => ({
                    ...tag,
                    active: false
                }));
                node.tagWidget.value = updatedTags;
                node.applyTriggerHighlightState?.();
                node.setDirtyCanvas(true);
            }
        });
        toggleAllOffButton.serialize = false;

        // Clear all tags
        const clearAllButton = node.addWidget("button", "Clear All", null, () => {
            if (node.tagWidget) {
                node.tagWidget.value = [];
                node.applyTriggerHighlightState?.();
                node.setDirtyCanvas(true);
            }
        });
        clearAllButton.serialize = false;
    },
});
