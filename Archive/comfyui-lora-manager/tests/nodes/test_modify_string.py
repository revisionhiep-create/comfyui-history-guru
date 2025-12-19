"""
Tests for the ModifyString node.
"""

import pytest
from py.nodes.modify_string import ModifyString
from py.nodes.modify_string_presets import get_preset_tags, get_category_names, merge_tags, deduplicate_tags


class TestModifyStringPresets:
    """Test preset management functions."""
    
    def test_get_category_names(self):
        """Test getting list of category names."""
        categories = get_category_names()
        assert "All" in categories
        assert "Quality" in categories
        assert "Lighting" in categories
        assert len(categories) > 5
    
    def test_get_preset_tags_all(self):
        """Test loading all preset tags."""
        tags = get_preset_tags("All", default_active=True)
        assert len(tags) > 50  # Should have many presets
        assert all(tag["active"] is True for tag in tags)
        assert all("text" in tag for tag in tags)
        assert all("category" in tag for tag in tags)
    
    def test_get_preset_tags_category(self):
        """Test loading specific category."""
        tags = get_preset_tags("Quality", default_active=False)
        assert len(tags) > 10
        assert all(tag["category"] == "Quality" for tag in tags)
        assert all(tag["active"] is False for tag in tags)
        assert "masterpiece" in [tag["text"] for tag in tags]
    
    def test_get_preset_tags_with_strength(self):
        """Test loading presets with default strength."""
        tags = get_preset_tags("Lighting", default_strength=1.2)
        assert all(tag["strength"] == 1.2 for tag in tags)
    
    def test_merge_tags_keep_both(self):
        """Test merging with keep_both strategy."""
        preset_tags = [
            {"text": "masterpiece", "active": True, "strength": None, "category": "Quality", "highlighted": False}
        ]
        incoming_tags = [
            {"text": "masterpiece", "active": True, "strength": None, "category": "Lora", "highlighted": True},
            {"text": "detailed", "active": True, "strength": None, "category": "Lora", "highlighted": True}
        ]
        
        result = merge_tags(preset_tags, incoming_tags, "keep_both")
        assert len(result) == 3  # preset + both incoming (duplicate kept)
        assert sum(1 for tag in result if tag["text"].lower() == "masterpiece") == 2
    
    def test_merge_tags_prefer_preset(self):
        """Test merging with prefer_preset strategy."""
        preset_tags = [
            {"text": "masterpiece", "active": False, "strength": 1.5, "category": "Quality", "highlighted": False}
        ]
        incoming_tags = [
            {"text": "masterpiece", "active": True, "strength": None, "category": "Lora", "highlighted": True}
        ]
        
        result = merge_tags(preset_tags, incoming_tags, "prefer_preset")
        assert len(result) == 1
        assert result[0]["active"] is False  # Preset value kept
        assert result[0]["strength"] == 1.5
    
    def test_merge_tags_prefer_incoming(self):
        """Test merging with prefer_incoming strategy."""
        preset_tags = [
            {"text": "masterpiece", "active": False, "strength": 1.5, "category": "Quality", "highlighted": False}
        ]
        incoming_tags = [
            {"text": "masterpiece", "active": True, "strength": None, "category": "Lora", "highlighted": True}
        ]
        
        result = merge_tags(preset_tags, incoming_tags, "prefer_incoming")
        assert len(result) == 1
        assert result[0]["active"] is True  # Incoming value kept
        assert result[0]["category"] == "Lora"
    
    def test_deduplicate_tags(self):
        """Test deduplication of tags."""
        tags = [
            {"text": "masterpiece", "active": True},
            {"text": "Masterpiece", "active": False},  # Duplicate with different case
            {"text": "detailed", "active": True},
            {"text": "masterpiece", "active": True},  # Exact duplicate
        ]
        
        result = deduplicate_tags(tags, case_sensitive=False)
        assert len(result) == 2
        assert result[0]["text"] == "masterpiece"
        assert result[1]["text"] == "detailed"


class TestModifyStringNode:
    """Test the ModifyString node functionality."""
    
    def test_node_initialization(self):
        """Test node can be initialized."""
        node = ModifyString()
        assert node.NAME == "Modify String (LoraManager)"
        assert node.CATEGORY == "Lora Manager/utils"
    
    def test_input_types(self):
        """Test input types are correctly defined."""
        inputs = ModifyString.INPUT_TYPES()
        assert "required" in inputs
        assert "optional" in inputs
        assert "hidden" in inputs
        assert "preset_category" in inputs["required"]
        assert "mode" in inputs["required"]
    
    def test_process_string_append_mode(self):
        """Test appending trigger words to input string."""
        node = ModifyString()
        
        modify_tags = [
            {"text": "masterpiece", "active": True, "strength": None},
            {"text": "best quality", "active": True, "strength": None},
        ]
        
        result = node.process_string(
            id="test",
            preset_category="All",
            mode="Append",
            separator=", ",
            merge_strategy="Keep Both",
            deduplicate=True,
            default_active=True,
            allow_strength_adjustment=False,
            input_string="a beautiful girl",
            modify_tags=modify_tags
        )
        
        output_string, active_triggers = result
        assert "a beautiful girl" in output_string
        assert "masterpiece" in output_string
        assert "best quality" in output_string
    
    def test_process_string_prepend_mode(self):
        """Test prepending trigger words to input string."""
        node = ModifyString()
        
        modify_tags = [
            {"text": "masterpiece", "active": True, "strength": None},
        ]
        
        result = node.process_string(
            id="test",
            preset_category="All",
            mode="Prepend",
            separator=", ",
            merge_strategy="Keep Both",
            deduplicate=True,
            default_active=True,
            allow_strength_adjustment=False,
            input_string="a beautiful girl",
            modify_tags=modify_tags
        )
        
        output_string, active_triggers = result
        assert output_string.startswith("masterpiece")
        assert "a beautiful girl" in output_string
    
    def test_process_string_replace_mode(self):
        """Test replacing input string with trigger words."""
        node = ModifyString()
        
        modify_tags = [
            {"text": "masterpiece", "active": True, "strength": None},
        ]
        
        result = node.process_string(
            id="test",
            preset_category="All",
            mode="Replace",
            separator=", ",
            merge_strategy="Keep Both",
            deduplicate=True,
            default_active=True,
            allow_strength_adjustment=False,
            input_string="a beautiful girl",
            modify_tags=modify_tags
        )
        
        output_string, active_triggers = result
        assert output_string == "masterpiece"
        assert "a beautiful girl" not in output_string
    
    def test_process_string_with_strength(self):
        """Test strength adjustment formatting."""
        node = ModifyString()
        
        modify_tags = [
            {"text": "masterpiece", "active": True, "strength": 1.2},
            {"text": "detailed", "active": True, "strength": 0.8},
        ]
        
        result = node.process_string(
            id="test",
            preset_category="All",
            mode="Tagged Only",
            separator=", ",
            merge_strategy="Keep Both",
            deduplicate=True,
            default_active=True,
            allow_strength_adjustment=True,
            modify_tags=modify_tags
        )
        
        output_string, active_triggers = result
        assert "(masterpiece:1.20)" in output_string
        assert "(detailed:0.80)" in output_string
    
    def test_process_string_inactive_tags(self):
        """Test that inactive tags are filtered out."""
        node = ModifyString()
        
        modify_tags = [
            {"text": "masterpiece", "active": True, "strength": None},
            {"text": "worst quality", "active": False, "strength": None},
        ]
        
        result = node.process_string(
            id="test",
            preset_category="All",
            mode="Tagged Only",
            separator=", ",
            merge_strategy="Keep Both",
            deduplicate=True,
            default_active=True,
            allow_strength_adjustment=False,
            modify_tags=modify_tags
        )
        
        output_string, active_triggers = result
        assert "masterpiece" in output_string
        assert "worst quality" not in output_string
    
    def test_parse_trigger_words_from_lora(self):
        """Test parsing trigger words from Lora Loader format."""
        node = ModifyString()
        
        # Lora Loader format: groups separated by ',, '
        trigger_words = "flat color, dark theme,, (sinozick style:0.94),, masterpiece"
        
        tags = node._parse_trigger_words_input(trigger_words)
        assert len(tags) == 3
        assert tags[0]["text"] == "flat color, dark theme"
        assert tags[1]["text"] == "(sinozick style:0.94)"
        assert tags[2]["text"] == "masterpiece"
        assert all(tag["category"] == "Lora" for tag in tags)
    
    def test_parse_strength_from_text(self):
        """Test extracting strength from formatted text."""
        node = ModifyString()
        
        text, strength = node._parse_strength_from_text("(masterpiece:1.2)")
        assert text == "masterpiece"
        assert strength == 1.2
        
        text, strength = node._parse_strength_from_text("masterpiece")
        assert text == "masterpiece"
        assert strength is None
    
    def test_deduplicate_option(self):
        """Test deduplication option."""
        node = ModifyString()
        
        modify_tags = [
            {"text": "masterpiece", "active": True, "strength": None},
            {"text": "Masterpiece", "active": True, "strength": None},  # Duplicate
        ]
        
        # With deduplication
        result = node.process_string(
            id="test",
            preset_category="All",
            mode="Tagged Only",
            separator=", ",
            merge_strategy="Keep Both",
            deduplicate=True,
            default_active=True,
            allow_strength_adjustment=False,
            modify_tags=modify_tags
        )
        
        output_string, active_triggers = result
        assert output_string.count("masterpiece") == 1  # Only one instance
    
    def test_empty_input(self):
        """Test handling empty inputs."""
        node = ModifyString()
        
        result = node.process_string(
            id="test",
            preset_category="All",
            mode="Append",
            separator=", ",
            merge_strategy="Keep Both",
            deduplicate=True,
            default_active=True,
            allow_strength_adjustment=False,
            input_string="",
            modify_tags=[]
        )
        
        output_string, active_triggers = result
        assert output_string == ""
        assert active_triggers == ""
    
    def test_custom_separator(self):
        """Test using custom separator."""
        node = ModifyString()
        
        modify_tags = [
            {"text": "masterpiece", "active": True, "strength": None},
            {"text": "detailed", "active": True, "strength": None},
        ]
        
        result = node.process_string(
            id="test",
            preset_category="All",
            mode="Tagged Only",
            separator=" | ",
            merge_strategy="Keep Both",
            deduplicate=True,
            default_active=True,
            allow_strength_adjustment=False,
            modify_tags=modify_tags
        )
        
        output_string, active_triggers = result
        assert " | " in output_string
        assert "masterpiece | detailed" in output_string
