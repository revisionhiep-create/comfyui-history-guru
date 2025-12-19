"""Image processing utilities for thumbnails."""
import os
from PIL import Image
from typing import Tuple
import numpy as np

from .config import PromptLibraryConfig


class ImageProcessor:
    """Handles image thumbnail generation with aspect ratio preservation."""
    
    @staticmethod
    def tensor_to_pil(image_tensor) -> Image.Image:
        """Convert ComfyUI image tensor to PIL Image."""
        # ComfyUI images are in format [B, H, W, C] with values 0-1
        if isinstance(image_tensor, np.ndarray):
            img_array = image_tensor
        else:
            # Convert torch tensor to numpy
            img_array = image_tensor.cpu().numpy()
        
        # Get first image if batch
        if len(img_array.shape) == 4:
            img_array = img_array[0]
        
        # Convert from 0-1 to 0-255
        img_array = (img_array * 255).astype(np.uint8)
        
        # Convert to PIL
        return Image.fromarray(img_array)
    
    @staticmethod
    def calculate_thumbnail_size(width: int, height: int, target_size: int = 512) -> Tuple[int, int]:
        """
        Calculate thumbnail dimensions preserving aspect ratio.
        
        Args:
            width: Original image width
            height: Original image height
            target_size: Target size for longest dimension
        
        Returns:
            Tuple of (new_width, new_height)
        """
        aspect_ratio = width / height
        
        if width > height:
            # Landscape
            new_width = target_size
            new_height = int(target_size / aspect_ratio)
        else:
            # Portrait or square
            new_height = target_size
            new_width = int(target_size * aspect_ratio)
        
        return (new_width, new_height)
    
    @staticmethod
    def create_thumbnail(image_tensor, 
                        filename: str,
                        target_size: int = None) -> Tuple[str, int, int]:
        """
        Create and save thumbnail from image tensor.
        
        Args:
            image_tensor: ComfyUI image tensor
            filename: Base filename for thumbnail
            target_size: Target size for longest dimension
        
        Returns:
            Tuple of (thumbnail_path, original_width, original_height)
        """
        if target_size is None:
            target_size = PromptLibraryConfig.THUMBNAIL_SIZE
        
        pil_image = None
        thumbnail = None
        try:
            # Convert to PIL
            pil_image = ImageProcessor.tensor_to_pil(image_tensor)
            original_width, original_height = pil_image.size
            
            # Calculate thumbnail size
            thumb_width, thumb_height = ImageProcessor.calculate_thumbnail_size(
                original_width, original_height, target_size
            )
            
            # Resize with high-quality resampling
            thumbnail = pil_image.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
            
            # Generate thumbnail path
            thumbnails_dir = PromptLibraryConfig.get_thumbnails_dir()
            thumbnail_path = os.path.join(thumbnails_dir, f"{filename}.webp")
            
            # Save as WebP
            thumbnail.save(
                thumbnail_path,
                format=PromptLibraryConfig.THUMBNAIL_FORMAT,
                quality=PromptLibraryConfig.THUMBNAIL_QUALITY
            )
            
            print(f"[Prompt Library] Thumbnail saved: {thumbnail_path}")
            return thumbnail_path, original_width, original_height
            
        except Exception as e:
            print(f"[Prompt Library] Error creating thumbnail: {e}")
            return None, None, None
        finally:
            # Cleanup PIL images to free memory
            if thumbnail:
                try:
                    thumbnail.close()
                except:
                    pass
            if pil_image:
                try:
                    pil_image.close()
                except:
                    pass
    
    @staticmethod
    def cleanup_thumbnail(thumbnail_path: str):
        """Delete a thumbnail file."""
        try:
            if thumbnail_path and os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
                print(f"[Prompt Library] Deleted thumbnail: {thumbnail_path}")
        except Exception as e:
            print(f"[Prompt Library] Error deleting thumbnail: {e}")
