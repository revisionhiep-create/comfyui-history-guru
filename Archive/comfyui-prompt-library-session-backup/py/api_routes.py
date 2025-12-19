"""API routes for Prompt Library web interface."""
import os
import json
from aiohttp import web
import mimetypes

from .database import PromptLibraryDatabase
from .config import PromptLibraryConfig


class PromptLibraryAPI:
    """API routes for the Prompt Library."""
    
    def __init__(self):
        self.db = PromptLibraryDatabase()
    
    @staticmethod
    def add_routes(app):
        """Add API routes to ComfyUI server."""
        api = PromptLibraryAPI()
        
        # API endpoints
        app.router.add_get('/prompt_library/api/prompts', api.get_prompts)
        app.router.add_post('/prompt_library/api/favorite/{prompt_id}', api.toggle_favorite)
        app.router.add_delete('/prompt_library/api/prompt/{prompt_id}', api.delete_prompt)
        app.router.add_get('/prompt_library/api/export', api.export_csv)
        app.router.add_get('/prompt_library/api/stats', api.get_stats)
        app.router.add_get('/prompt_library/thumbnail/{filename}', api.serve_thumbnail)
        
        # Web UI routes
        app.router.add_get('/prompt_library', api.serve_index)
        app.router.add_get('/prompt_library/', api.serve_index)
        app.router.add_get('/prompt_library/static/{filename}', api.serve_static)
        
        print("[Prompt Library] API and web routes registered")
    
    async def get_prompts(self, request):
        """Get prompts with filtering and pagination."""
        try:
            # Parse query parameters
            params = request.rel_url.query
            
            # Validate and sanitize inputs
            try:
                limit = min(max(int(params.get('limit', 50)), 1), 1000)
                offset = max(int(params.get('offset', 0)), 0)
            except ValueError:
                return web.json_response({'error': 'Invalid limit or offset'}, status=400)
            
            search_lora = params.get('search_lora', None)
            if search_lora:
                search_lora = search_lora[:200]  # Limit length
            
            sort_by = params.get('sort_by', 'date')
            if sort_by not in ['date', 'alphabetical']:
                sort_by = 'date'
            
            favorites_only = params.get('favorites_only', '0') == '1'
            
            # Get prompts from database
            prompts = self.db.get_prompts(
                limit=limit,
                offset=offset,
                search_lora=search_lora,
                sort_by=sort_by,
                favorites_only=favorites_only
            )
            
            # Get total count
            total = self.db.get_total_count(
                search_lora=search_lora,
                favorites_only=favorites_only
            )
            
            return web.json_response({
                'prompts': prompts,
                'total': total,
                'limit': limit,
                'offset': offset
            })
            
        except Exception as e:
            print(f"[Prompt Library API] Error in get_prompts: {e}")
            return web.json_response({'error': str(e)}, status=500)
    
    async def toggle_favorite(self, request):
        """Toggle favorite status for a prompt."""
        try:
            try:
                prompt_id = int(request.match_info['prompt_id'])
                if prompt_id < 1:
                    return web.json_response({'error': 'Invalid prompt ID'}, status=400)
            except (ValueError, KeyError):
                return web.json_response({'error': 'Invalid prompt ID'}, status=400)
            
            success = self.db.toggle_favorite(prompt_id)
            
            if success:
                return web.json_response({'success': True})
            else:
                return web.json_response({'error': 'Prompt not found'}, status=404)
                
        except Exception as e:
            print(f"[Prompt Library API] Error in toggle_favorite: {e}")
            return web.json_response({'error': str(e)}, status=500)
    
    async def delete_prompt(self, request):
        """Delete a prompt."""
        try:
            try:
                prompt_id = int(request.match_info['prompt_id'])
                if prompt_id < 1:
                    return web.json_response({'error': 'Invalid prompt ID'}, status=400)
            except (ValueError, KeyError):
                return web.json_response({'error': 'Invalid prompt ID'}, status=400)
            
            success = self.db.delete_prompt(prompt_id)
            
            if success:
                return web.json_response({'success': True})
            else:
                return web.json_response({'error': 'Prompt not found'}, status=404)
                
        except Exception as e:
            print(f"[Prompt Library API] Error in delete_prompt: {e}")
            return web.json_response({'error': str(e)}, status=500)
    
    async def export_csv(self, request):
        """Export prompts to CSV."""
        try:
            # Generate CSV file
            library_dir = PromptLibraryConfig.get_library_dir()
            csv_path = os.path.join(library_dir, 'prompt_library_export.csv')
            
            success = self.db.export_to_csv(csv_path)
            
            if success and os.path.exists(csv_path):
                # Serve the file
                return web.FileResponse(
                    csv_path,
                    headers={
                        'Content-Disposition': 'attachment; filename="prompt_library_export.csv"'
                    }
                )
            else:
                return web.json_response({'error': 'Export failed'}, status=500)
                
        except Exception as e:
            print(f"[Prompt Library API] Error in export_csv: {e}")
            return web.json_response({'error': str(e)}, status=500)
    
    async def get_stats(self, request):
        """Get library statistics."""
        try:
            total = self.db.get_total_count()
            favorites = self.db.get_total_count(favorites_only=True)
            
            return web.json_response({
                'total_prompts': total,
                'total_favorites': favorites,
                'history_limit': PromptLibraryConfig.DEFAULT_HISTORY_LIMIT
            })
            
        except Exception as e:
            print(f"[Prompt Library API] Error in get_stats: {e}")
            return web.json_response({'error': str(e)}, status=500)
    
    async def serve_thumbnail(self, request):
        """Serve thumbnail images."""
        try:
            filename = request.match_info['filename']
            
            # Security: Validate filename to prevent directory traversal
            if not filename or '..' in filename or '/' in filename or '\\' in filename:
                return web.Response(status=400, text='Invalid filename')
            
            # Only allow webp files
            if not filename.endswith('.webp'):
                return web.Response(status=400, text='Invalid file type')
            
            thumbnails_dir = PromptLibraryConfig.get_thumbnails_dir()
            file_path = os.path.join(thumbnails_dir, filename)
            
            # Security: Ensure resolved path is within thumbnails directory
            real_thumbnails_dir = os.path.realpath(thumbnails_dir)
            real_file_path = os.path.realpath(file_path)
            if not real_file_path.startswith(real_thumbnails_dir):
                return web.Response(status=403, text='Access denied')
            
            if os.path.exists(file_path):
                # Get MIME type
                mime_type, _ = mimetypes.guess_type(file_path)
                return web.FileResponse(file_path, headers={'Content-Type': mime_type or 'image/webp'})
            else:
                return web.Response(status=404, text='Thumbnail not found')
                
        except Exception as e:
            print(f"[Prompt Library API] Error serving thumbnail: {e}")
            return web.Response(status=500, text=str(e))
    
    async def serve_index(self, request):
        """Serve the main web UI HTML page."""
        try:
            # Get path to web directory
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            web_dir = os.path.join(current_dir, 'web')
            index_path = os.path.join(web_dir, 'index.html')
            
            if os.path.exists(index_path):
                return web.FileResponse(index_path, headers={'Content-Type': 'text/html'})
            else:
                return web.Response(status=404, text='Web UI not found')
                
        except Exception as e:
            print(f"[Prompt Library API] Error serving index: {e}")
            return web.Response(status=500, text=str(e))
    
    async def serve_static(self, request):
        """Serve static files (CSS, JS)."""
        try:
            filename = request.match_info['filename']
            
            # Security: Validate filename
            if not filename or '..' in filename or '/' in filename or '\\' in filename:
                return web.Response(status=400, text='Invalid filename')
            
            # Get path to web directory
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            web_dir = os.path.join(current_dir, 'web')
            file_path = os.path.join(web_dir, filename)
            
            # Security: Ensure path is within web directory
            real_web_dir = os.path.realpath(web_dir)
            real_file_path = os.path.realpath(file_path)
            if not real_file_path.startswith(real_web_dir):
                return web.Response(status=403, text='Access denied')
            
            if os.path.exists(file_path):
                mime_type, _ = mimetypes.guess_type(file_path)
                return web.FileResponse(file_path, headers={'Content-Type': mime_type or 'text/plain'})
            else:
                return web.Response(status=404, text='File not found')
                
        except Exception as e:
            print(f"[Prompt Library API] Error serving static file: {e}")
            return web.Response(status=500, text=str(e))
