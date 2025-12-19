"""Metadata extraction from ComfyUI workflow."""
import json
from typing import Dict, List, Optional, Any


class MetadataExtractor:
    """Extract metadata from ComfyUI prompt and workflow data."""
    
    @staticmethod
    def extract_from_prompt_dict(prompt_dict: Dict) -> Dict[str, Any]:
        """
        Extract metadata from ComfyUI prompt dictionary.
        
        Args:
            prompt_dict: The prompt dictionary from ComfyUI execution
        
        Returns:
            Dictionary containing extracted metadata
        """
        metadata = {
            'prompt_text': '',
            'negative_prompt': '',
            'checkpoint': '',
            'seed': None,
            'loras': []
        }
        
        if not prompt_dict:
            return metadata
        
        try:
            # Iterate through nodes in the prompt
            for node_id, node_data in prompt_dict.items():
                class_type = node_data.get('class_type', '')
                inputs = node_data.get('inputs', {})
                
                # Extract prompts from CLIP text encode nodes
                if 'CLIPTextEncode' in class_type or 'PromptManager' in class_type:
                    text = inputs.get('text', '')
                    if text:
                        # Heuristic: longer text is usually positive prompt
                        if len(text) > len(metadata['prompt_text']):
                            if metadata['prompt_text']:
                                # Move shorter text to negative
                                metadata['negative_prompt'] = metadata['prompt_text']
                            metadata['prompt_text'] = text
                        else:
                            metadata['negative_prompt'] = text
                
                # Extract LoRAs
                if 'LoraLoader' in class_type or 'LoRA' in class_type:
                    lora_name = inputs.get('lora_name', '')
                    strength_model = inputs.get('strength_model', 1.0)
                    
                    if lora_name:
                        metadata['loras'].append({
                            'name': lora_name,
                            'strength': float(strength_model)
                        })
                
                # Extract checkpoint
                if 'CheckpointLoader' in class_type or 'Checkpoint' in class_type:
                    ckpt_name = inputs.get('ckpt_name', '') or inputs.get('checkpoint_name', '')
                    if ckpt_name:
                        metadata['checkpoint'] = ckpt_name
                
                # Extract seed from KSampler
                if 'KSampler' in class_type or 'Sampler' in class_type:
                    seed = inputs.get('seed', None)
                    if seed is not None:
                        try:
                            metadata['seed'] = int(seed)
                        except:
                            pass
            
        except Exception as e:
            print(f"[Prompt Library] Error extracting metadata: {e}")
        
        return metadata
    
    @staticmethod
    def extract_loras_from_text(text: str) -> List[Dict[str, Any]]:
        """
        Extract LoRA information from prompt text with <lora:name:strength> format.
        
        Args:
            text: Prompt text potentially containing LoRA tags
        
        Returns:
            List of LoRA dictionaries
        """
        loras = []
        
        # Common LoRA tag formats
        # <lora:name:strength>
        # (lora:name:strength)
        import re
        patterns = [
            r'<lora:([^:>]+):([0-9.]+)>',
            r'\(lora:([^:)]+):([0-9.]+)\)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    loras.append({
                        'name': match[0].strip(),
                        'strength': float(match[1])
                    })
                except:
                    pass
        
        return loras
    
    @staticmethod
    def merge_lora_data(workflow_loras: List[Dict], text_loras: List[Dict]) -> List[Dict]:
        """
        Merge LoRA data from workflow and text extraction.
        
        Args:
            workflow_loras: LoRAs extracted from workflow nodes
            text_loras: LoRAs extracted from text
        
        Returns:
            Combined list of unique LoRAs
        """
        # Use dict to deduplicate by name
        lora_dict = {}
        
        for lora in workflow_loras:
            lora_dict[lora['name']] = lora
        
        for lora in text_loras:
            # Prefer text LoRAs if not in workflow
            if lora['name'] not in lora_dict:
                lora_dict[lora['name']] = lora
        
        return list(lora_dict.values())
