"""ComfyUI Prompt Library - Record and browse prompt history."""

try:
    from .prompt_library import NODE_CLASS_MAPPINGS as RECORDER_MAPPINGS
    from .prompt_library import NODE_DISPLAY_NAME_MAPPINGS as RECORDER_DISPLAY_MAPPINGS
    from .prompt_library_viewer import NODE_CLASS_MAPPINGS as VIEWER_MAPPINGS
    from .prompt_library_viewer import NODE_DISPLAY_NAME_MAPPINGS as VIEWER_DISPLAY_MAPPINGS
    from .py.api_routes import PromptLibraryAPI
except ImportError as e:
    print(f"[Prompt Library] Import error: {e}")
    import sys
    import pathlib
    
    # Add package root to path for development
    package_root = pathlib.Path(__file__).resolve().parent
    if str(package_root) not in sys.path:
        sys.path.append(str(package_root))
    
    from prompt_library import NODE_CLASS_MAPPINGS as RECORDER_MAPPINGS
    from prompt_library import NODE_DISPLAY_NAME_MAPPINGS as RECORDER_DISPLAY_MAPPINGS
    from prompt_library_viewer import NODE_CLASS_MAPPINGS as VIEWER_MAPPINGS
    from prompt_library_viewer import NODE_DISPLAY_NAME_MAPPINGS as VIEWER_DISPLAY_MAPPINGS
    from py.api_routes import PromptLibraryAPI

# Combine node mappings
NODE_CLASS_MAPPINGS = {**RECORDER_MAPPINGS, **VIEWER_MAPPINGS}
NODE_DISPLAY_NAME_MAPPINGS = {**RECORDER_DISPLAY_MAPPINGS, **VIEWER_DISPLAY_MAPPINGS}

# Web directory for JavaScript files
WEB_DIRECTORY = "./js"

# Try to register routes immediately if server is available
try:
    import server
    if hasattr(server, 'PromptServer'):
        prompt_server = server.PromptServer.instance
        if prompt_server and hasattr(prompt_server, 'app'):
            PromptLibraryAPI.add_routes(prompt_server.app)
except Exception as e:
    print(f"[Prompt Library] Error registering routes: {e}")

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

print("[Prompt Library] Extension loaded successfully!")
print("[Prompt Library] Two nodes available:")
print("[Prompt Library]   - 📚 Prompt Library: Auto-records prompts (connect to images)")
print("[Prompt Library]   - 📚 Prompt Library Viewer: Browse library (standalone)")
print("[Prompt Library] Web UI available at: http://127.0.0.1:8188/prompt_library")
