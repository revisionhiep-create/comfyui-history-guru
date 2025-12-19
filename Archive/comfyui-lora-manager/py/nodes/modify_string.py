"""
Modify String Node - Advanced trigger word management with presets and editing.
Allows loading preset trigger words, toggling them on/off, editing text, and merging with Lora trigger words.
"""

import json
import re
import logging
from .utils import FlexibleOptionalInputType, any_type
from .modify_string_presets import get_preset_tags, get_category_names, merge_tags, deduplicate_tags

logger = logging.getLogger(__name__)

# Pre-compile regex pattern for performance (used in _parse_strength_from_text)
_STRENGTH_PATTERN = re.compile(r'\((.+?):([\d.]+)\)')


class ModifyString:
    NAME = "Modify String (LoraManager)"
    CATEGORY = "Lora Manager/utils"
    DESCRIPTION = "Modify text strings with toggleable trigger words, presets, and Lora trigger word integration"
    
    # Note: The following widgets are added dynamically by the JavaScript extension:
    # - modify_tags: Tags widget for displaying and editing trigger words
    # - original_trigger_words: Hidden widget to track incoming trigger words from Lora Loader
    # - reload_presets: Hidden widget to signal when presets should be reloaded
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "preset_category": (get_category_names(), {
                    "default": "All",
                    "tooltip": "Load preset trigger words from a specific category"
                }),
                "mode": (["Append", "Prepend", "Replace", "Tagged Only"], {
                    "default": "Append",
                    "tooltip": "How to combine trigger words with input text"
                }),
                "separator": ("STRING", {
                    "default": ", ",
                    "tooltip": "Separator between trigger words"
                }),
                "merge_strategy": (["Keep Both", "Prefer Preset", "Prefer Incoming"], {
                    "default": "Keep Both",
                    "tooltip": "How to handle duplicate trigger words from LoRA and presets"
                }),
                "deduplicate": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Remove duplicate trigger words from final output"
                }),
                "default_active": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Default active state for newly added trigger words"
                }),
                "allow_strength_adjustment": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Enable strength adjustment for trigger words (word:1.2 format)"
                }),
            },
            "optional": FlexibleOptionalInputType(any_type),
            "hidden": {
                "id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("output_string", "active_triggers")
    FUNCTION = "process_string"

    def _get_data(self, kwargs, key):
        """Helper to extract data from kwargs with support for both old and new formats."""
        if key not in kwargs:
            return None
            
        data = kwargs[key]
        # Handle new format: {'key': {'__value__': ...}}
        if isinstance(data, dict) and '__value__' in data:
            return data['__value__']
        # Handle old format: {'key': ...}
        else:
            return data

    def _parse_trigger_words_input(self, trigger_words_text):
        """
        Parse trigger words from Lora Loader format (groups separated by ',, ').
        
        Args:
            trigger_words_text: String with trigger words separated by ',, '
            
        Returns:
            List of tag dictionaries
        """
        if not trigger_words_text or not isinstance(trigger_words_text, str) or not trigger_words_text.strip():
            return []
        
        tags = []
        
        # Split by ',,' (group separator from Lora Loader)
        if ',,' in trigger_words_text:
            groups = trigger_words_text.split(',,')
            for group in groups:
                group = group.strip()
                if group:
                    tags.append({
                        "text": group,
                        "active": True,
                        "strength": None,
                        "category": "Lora",
                        "highlighted": True,
                    })
        else:
            # Single group or comma-separated
            words = [w.strip() for w in trigger_words_text.split(',') if w.strip()]
            for word in words:
                tags.append({
                    "text": word,
                    "active": True,
                    "strength": None,
                    "category": "Lora",
                    "highlighted": True,
                })
        
        return tags

    def _format_word_output(self, text, strength, allow_strength_adjustment):
        """Format a single trigger word with optional strength."""
        if allow_strength_adjustment and strength is not None:
            return f"({text}:{strength:.2f})"
        return text

    def _parse_strength_from_text(self, text):
        """
        Extract base text and strength from formatted string like '(word:1.2)'.
        
        Returns:
            Tuple of (base_text, strength) or (text, None)
        """
        strength_match = _STRENGTH_PATTERN.match(text.strip())
        if strength_match:
            base_text = strength_match.group(1).strip()
            strength = float(strength_match.group(2))
            # Clamp strength to ComfyUI typical range (0.0-2.0)
            strength = max(0.0, min(2.0, strength))
            return base_text, strength
        return text, None

    def process_string(
        self,
        id,
        preset_category,
        mode,
        separator,
        merge_strategy,
        deduplicate,
        default_active,
        allow_strength_adjustment,
        **kwargs,
    ):
        """
        Process the string with trigger words, presets, and user modifications.
        
        Args:
            id: Node unique ID
            preset_category: Category of preset tags to load
            mode: How to combine tags with input string (Append/Prepend/Replace/Tagged Only)
            separator: Separator between tags
            merge_strategy: How to handle duplicates
            deduplicate: Whether to remove duplicates
            default_active: Default active state for new tags
            allow_strength_adjustment: Enable strength formatting
            **kwargs: Additional inputs including optional inputs
            
        Returns:
            Tuple of (output_string, active_triggers)
        """
        
        # Get input string (optional)
        input_string_data = self._get_data(kwargs, 'input_string')
        input_string = input_string_data if isinstance(input_string_data, str) else ""
        
        # Get trigger words from Lora Loader (optional)
        trigger_words_data = self._get_data(kwargs, 'trigger_words')
        trigger_words_text = trigger_words_data if isinstance(trigger_words_data, str) else ""
        
        # Get user-modified tags from widget
        modify_tags_data = self._get_data(kwargs, 'modify_tags')
        
        # Check if presets should be reloaded (set by UI)
        reload_presets_data = self._get_data(kwargs, 'reload_presets')
        reload_presets = reload_presets_data if isinstance(reload_presets_data, bool) else False
        
        # Get original trigger words (for comparison)
        original_trigger_words_data = self._get_data(kwargs, 'original_trigger_words')
        original_trigger_words_text = original_trigger_words_data if isinstance(original_trigger_words_data, str) else ""
        
        # Initialize tags list
        all_tags = []
        
        # Determine if we need to reload/reinitialize tags
        # Reload if: 1) No existing tags, 2) Reload flag is set, 3) New trigger words from Lora
        should_reload = (
            not modify_tags_data or 
            reload_presets or
            (trigger_words_text and trigger_words_text != original_trigger_words_text)
        )
        
        # If we have user-modified tags from the widget and shouldn't reload, use them
        if modify_tags_data and not should_reload:
            try:
                if isinstance(modify_tags_data, str):
                    modify_tags_data = json.loads(modify_tags_data)
                
                if isinstance(modify_tags_data, list):
                    # Process each tag from widget
                    for item in modify_tags_data:
                        text = item.get('text', '').strip()
                        if not text:
                            continue
                        
                        # Parse strength if present in text
                        base_text, parsed_strength = self._parse_strength_from_text(text)
                        
                        # Use parsed strength if available, otherwise use stored strength
                        strength = parsed_strength if parsed_strength is not None else item.get('strength')
                        
                        all_tags.append({
                            "text": base_text,
                            "active": item.get('active', default_active),
                            "strength": strength,
                            "category": item.get('category', 'Custom'),
                            "highlighted": item.get('highlighted', False),
                        })
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in modify_tags: {e}")
                modify_tags_data = []  # Explicit fallback to empty list
            except Exception as e:
                logger.exception(f"Unexpected error processing modify_tags: {e}")
                modify_tags_data = []  # Explicit fallback
        else:
            # No user tags yet, initialize with presets and incoming trigger words
            
            # Load preset tags if category is selected
            preset_tags = get_preset_tags(preset_category, default_active, None)
            
            # Parse incoming trigger words from Lora Loader
            incoming_tags = self._parse_trigger_words_input(trigger_words_text)
            
            # Merge presets with incoming tags based on strategy
            merge_strategy_map = {
                "Keep Both": "keep_both",
                "Prefer Preset": "prefer_preset",
                "Prefer Incoming": "prefer_incoming",
            }
            all_tags = merge_tags(
                preset_tags,
                incoming_tags,
                merge_strategy_map.get(merge_strategy, "keep_both")
            )
        
        # Deduplicate if requested
        if deduplicate:
            all_tags = deduplicate_tags(all_tags, case_sensitive=False)
        
        # Filter active tags and format with strength
        active_tags = []
        for tag in all_tags:
            if tag.get('active', False):
                formatted = self._format_word_output(
                    tag['text'],
                    tag.get('strength'),
                    allow_strength_adjustment
                )
                active_tags.append(formatted)
        
        # Build output string based on mode (optimized string building)
        tags_string = separator.join(active_tags)
        
        if mode in ("Replace", "Tagged Only"):
            output_string = tags_string
        elif mode == "Append":
            # Use filter to remove empty strings, then join
            output_string = separator.join(filter(None, [input_string, tags_string]))
        elif mode == "Prepend":
            # Use filter to remove empty strings, then join
            output_string = separator.join(filter(None, [tags_string, input_string]))
        else:
            output_string = input_string
        
        # Return output string and list of active triggers (for debugging/inspection)
        active_triggers_list = separator.join(active_tags)
        
        return (output_string, active_triggers_list)
