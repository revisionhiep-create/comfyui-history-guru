#!/usr/bin/env python3
"""
Analyze Civitai image metadata to understand their format.
Helps add support for Civitai metadata without breaking existing methods.
"""

from PIL import Image
from pathlib import Path
import json
import re

def analyze_png_metadata(image_path):
    """Analyze PNG metadata chunks."""
    try:
        with Image.open(image_path) as img:
            if img.format != 'PNG':
                return None
            
            metadata = {
                'file': image_path.name,
                'format': 'PNG',
                'size': img.size,
                'info_keys': list(img.info.keys()) if hasattr(img, 'info') else [],
                'text_chunks': {},
                'workflow_detected': False,
                'parameters_detected': False,
                'civitai_detected': False
            }
            
            # Extract all text chunks
            if hasattr(img, 'info') and img.info:
                for key, value in img.info.items():
                    metadata['text_chunks'][key] = str(value)[:500]  # First 500 chars
                    
                    # Check for ComfyUI workflow
                    if 'workflow' in key.lower() or (isinstance(value, str) and '"class_type"' in value):
                        metadata['workflow_detected'] = True
                    
                    # Check for parameters
                    if 'parameters' in key.lower() or (isinstance(value, str) and 'Steps:' in value):
                        metadata['parameters_detected'] = True
                    
                    # Check for Civitai
                    if 'civitai' in str(value).lower() or 'prompt' in key.lower():
                        metadata['civitai_detected'] = True
            
            return metadata
    except Exception as e:
        return {'file': image_path.name, 'error': str(e)}

def analyze_raw_png_chunks(image_path):
    """Read PNG file as binary to analyze all chunks."""
    try:
        with open(image_path, 'rb') as f:
            data = f.read()
        
        chunks = []
        offset = 8  # Skip PNG signature
        
        while offset < len(data) - 8:
            # Read chunk length
            if offset + 4 > len(data):
                break
            chunk_len = int.from_bytes(data[offset:offset+4], 'big')
            
            # Read chunk type
            if offset + 8 > len(data):
                break
            chunk_type = data[offset+4:offset+8].decode('ascii', errors='ignore')
            
            # Read chunk data
            if offset + 8 + chunk_len > len(data):
                break
            chunk_data = data[offset+8:offset+8+chunk_len]
            
            # Check if it's a text chunk
            if chunk_type in ['tEXt', 'iTXt', 'zTXt']:
                try:
                    # Try to decode as text
                    if chunk_type == 'zTXt':
                        # Compressed - would need decompression
                        text = f"[Compressed {chunk_len} bytes]"
                    else:
                        text = chunk_data.decode('utf-8', errors='ignore').replace('\0', ' ')
                    
                    # Extract keyword (first part before null byte)
                    if '\0' in text or chunk_type == 'tEXt':
                        parts = text.split('\0', 1) if '\0' in text else [text, '']
                        keyword = parts[0]
                        content = parts[1] if len(parts) > 1 else text
                    else:
                        keyword = chunk_type
                        content = text
                    
                    chunks.append({
                        'type': chunk_type,
                        'keyword': keyword[:50],
                        'content_preview': content[:200],
                        'full_length': len(content)
                    })
                except:
                    chunks.append({
                        'type': chunk_type,
                        'keyword': '[Binary]',
                        'content_preview': f'[Binary data: {chunk_len} bytes]'
                    })
            
            offset += 8 + chunk_len + 4  # length + type + data + CRC
            
            if chunk_type == 'IEND':
                break
        
        return chunks
    except Exception as e:
        return [{'error': str(e)}]

def analyze_all_images(folder_path):
    """Analyze all images in folder."""
    folder = Path(folder_path)
    results = []
    
    for img_file in folder.glob('*.png'):
        print(f"\nAnalyzing: {img_file.name}")
        
        # Method 1: PIL analysis
        pil_meta = analyze_png_metadata(img_file)
        if pil_meta:
            results.append(pil_meta)
            print(f"  Format: {pil_meta.get('format')}")
            print(f"  Info keys: {', '.join(pil_meta.get('info_keys', []))}")
            print(f"  Workflow: {pil_meta.get('workflow_detected')}")
            print(f"  Parameters: {pil_meta.get('parameters_detected')}")
            print(f"  Civitai: {pil_meta.get('civitai_detected')}")
        
        # Method 2: Raw chunk analysis
        chunks = analyze_raw_png_chunks(img_file)
        if chunks:
            print(f"  Text chunks found: {len(chunks)}")
            for chunk in chunks[:5]:  # Show first 5
                print(f"    - {chunk.get('type')}: {chunk.get('keyword')}")
                if chunk.get('content_preview'):
                    preview = chunk['content_preview'][:100]
                    print(f"      Preview: {preview}...")
    
    return results

if __name__ == '__main__':
    import sys
    
    folder = sys.argv[1] if len(sys.argv) > 1 else 'Comfyui'
    print(f"Analyzing images in: {folder}")
    print("=" * 60)
    
    results = analyze_all_images(folder)
    
    print("\n" + "=" * 60)
    print(f"\nSummary: Analyzed {len(results)} images")
    
    # Count metadata types
    workflow_count = sum(1 for r in results if r.get('workflow_detected'))
    params_count = sum(1 for r in results if r.get('parameters_detected'))
    civitai_count = sum(1 for r in results if r.get('civitai_detected'))
    
    print(f"  Workflow detected: {workflow_count}")
    print(f"  Parameters detected: {params_count}")
    print(f"  Civitai detected: {civitai_count}")
    
    # Save detailed report
    with open('civitai_metadata_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed report saved to: civitai_metadata_analysis.json")
