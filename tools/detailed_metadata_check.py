#!/usr/bin/env python3
"""
Detailed metadata analysis for all images to find what's missing.
"""

from PIL import Image
from pathlib import Path
import json
import re

def extract_all_png_chunks(image_path):
    """Extract all text chunks from PNG file."""
    try:
        with open(image_path, 'rb') as f:
            data = f.read()
        
        chunks = []
        offset = 8  # Skip PNG signature
        
        while offset < len(data) - 8:
            if offset + 4 > len(data):
                break
            chunk_len = int.from_bytes(data[offset:offset+4], 'big')
            
            if offset + 8 > len(data):
                break
            chunk_type = data[offset+4:offset+8].decode('ascii', errors='ignore')
            
            if offset + 8 + chunk_len > len(data):
                break
            chunk_data = data[offset+8:offset+8+chunk_len]
            
            # Extract text chunks
            if chunk_type in ['tEXt', 'iTXt', 'zTXt']:
                try:
                    if chunk_type == 'zTXt':
                        # Compressed - mark it
                        text = f"[Compressed {chunk_len} bytes]"
                        keyword = "[zTXt]"
                        content = ""
                    else:
                        # Decode text
                        text = chunk_data.decode('utf-8', errors='ignore')
                        # Split keyword and content (null byte separator)
                        if '\0' in text:
                            parts = text.split('\0', 1)
                            keyword = parts[0]
                            content = parts[1] if len(parts) > 1 else ""
                        else:
                            keyword = chunk_type
                            content = text
                    
                    chunks.append({
                        'type': chunk_type,
                        'keyword': keyword,
                        'content': content[:1000],  # First 1000 chars
                        'full_length': len(content)
                    })
                except Exception as e:
                    chunks.append({
                        'type': chunk_type,
                        'keyword': '[Error]',
                        'content': f'Error: {str(e)}',
                        'full_length': 0
                    })
            
            offset += 8 + chunk_len + 4  # length + type + data + CRC
            
            if chunk_type == 'IEND':
                break
        
        return chunks
    except Exception as e:
        return [{'error': str(e)}]

def analyze_image(image_path):
    """Full analysis of an image."""
    result = {
        'file': image_path.name,
        'chunks': extract_all_png_chunks(image_path),
        'pil_info': {}
    }
    
    # Also check PIL info
    try:
        with Image.open(image_path) as img:
            if hasattr(img, 'info') and img.info:
                result['pil_info'] = {k: str(v)[:200] for k, v in img.info.items()}
    except Exception as e:
        result['pil_error'] = str(e)
    
    return result

def main():
    folder = Path('Comfyui')
    results = []
    
    for img_file in sorted(folder.glob('*.png')):
        print(f"\n{'='*60}")
        print(f"Analyzing: {img_file.name}")
        print('='*60)
        
        result = analyze_image(img_file)
        results.append(result)
        
        print(f"\nPIL Info Keys: {list(result['pil_info'].keys())}")
        print(f"\nText Chunks Found: {len(result['chunks'])}")
        
        for chunk in result['chunks']:
            print(f"\n  Chunk Type: {chunk.get('type')}")
            print(f"  Keyword: {chunk.get('keyword')}")
            content = chunk.get('content', '')
            if content:
                preview = content[:200] if len(content) > 200 else content
                print(f"  Content Preview: {preview}...")
                print(f"  Full Length: {chunk.get('full_length', 0)} chars")
                
                # Check for metadata indicators
                if 'class_type' in content or 'inputs' in content:
                    print("  [DETECTED] ComfyUI workflow format")
                if 'Steps:' in content or 'Sampler:' in content:
                    print("  [DETECTED] A1111 parameters format")
                if 'prompt' in chunk.get('keyword', '').lower():
                    print("  [DETECTED] Prompt chunk")
                if 'workflow' in chunk.get('keyword', '').lower():
                    print("  [DETECTED] Workflow chunk")
                if 'parameters' in chunk.get('keyword', '').lower():
                    print("  [DETECTED] Parameters chunk")
    
    # Save detailed report
    with open('detailed_metadata_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    for r in results:
        has_metadata = len(r['chunks']) > 0 or len(r['pil_info']) > 0
        print(f"{r['file']}: {len(r['chunks'])} chunks, {len(r['pil_info'])} PIL keys - {'HAS METADATA' if has_metadata else 'NO METADATA'}")

if __name__ == '__main__':
    main()
