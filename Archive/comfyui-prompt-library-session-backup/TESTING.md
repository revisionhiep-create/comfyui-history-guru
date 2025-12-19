# Testing Checklist for ComfyUI Prompt Library

## Pre-Testing Setup

- [ ] Ensure ComfyUI is installed and working
- [ ] Install dependencies: `pip install Pillow aiohttp`
- [ ] Copy node to `ComfyUI/custom_nodes/comfyui-prompt-library/`
- [ ] Restart ComfyUI
- [ ] Check console for successful load messages

## Basic Functionality Tests

### Node Installation
- [ ] Node appears in node menu under "📚 Prompt Library"
- [ ] Node can be added to workflow
- [ ] No errors in console on node creation

### Image Recording
- [ ] Connect IMAGE output to node
- [ ] Generate an image
- [ ] Check console for "Successfully recorded prompt" message
- [ ] Verify database created at `output/Prompt History/prompt_library.db`
- [ ] Verify thumbnail created in `output/Prompt History/thumbnails/`
- [ ] Thumbnail is WebP format
- [ ] Thumbnail preserves aspect ratio

### Widget Display
- [ ] Click "📚 Show/Hide Library" button
- [ ] Widget expands showing controls and list
- [ ] Empty state shows "No prompts found" message
- [ ] After recording, prompts appear in list
- [ ] Thumbnails load correctly
- [ ] Click toggle again hides widget

### Metadata Extraction
- [ ] Prompt text extracted correctly
- [ ] Negative prompt extracted (if present)
- [ ] Checkpoint name extracted
- [ ] Seed extracted
- [ ] LoRAs extracted with correct strengths
- [ ] Resolution captured correctly

## Search & Filter Tests

### Search by LoRA
- [ ] Enter LoRA name in search box
- [ ] Results filter correctly
- [ ] Clear search shows all prompts
- [ ] Partial name matching works
- [ ] Case-insensitive search

### Sorting
- [ ] Sort by Date (newest first)
- [ ] Sort Alphabetically
- [ ] Sorting persists across page loads

### Favorites
- [ ] Click star icon to favorite
- [ ] Star fills in when favorited
- [ ] Enable "Favorites Only" filter
- [ ] Only favorited prompts show
- [ ] Disable filter shows all prompts

## Actions Tests

### Copy to Clipboard
- [ ] Click prompt text
- [ ] Text copied to clipboard
- [ ] Can paste in text editor

### Delete Prompt
- [ ] Click delete (🗑️) button
- [ ] Confirmation dialog appears
- [ ] Confirm deletion
- [ ] Prompt removed from list
- [ ] Thumbnail file deleted from disk
- [ ] Database entry removed

### Export CSV
- [ ] Click "📥 Export CSV" button
- [ ] CSV file downloads
- [ ] Open in Excel/Google Sheets
- [ ] All fields present and correct
- [ ] LoRAs formatted properly

## Pagination Tests

- [ ] Generate more than 20 prompts
- [ ] Pagination controls appear
- [ ] "Next" button works
- [ ] "Previous" button works
- [ ] Page numbers display correctly
- [ ] Navigation updates results

## Deduplication Tests

- [ ] Generate same prompt twice
- [ ] Second generation not recorded
- [ ] Console shows "Skipped duplicate prompt"
- [ ] Change LoRA strength slightly
- [ ] New entry created (different hash)

## Auto-Cleanup Tests

- [ ] Set history limit to 10 (in config)
- [ ] Generate 15 prompts
- [ ] Verify only 10 most recent kept
- [ ] Old thumbnails deleted
- [ ] Old database entries removed

## Edge Cases

### Empty/Missing Data
- [ ] Node works without optional inputs
- [ ] Works with no LoRAs in workflow
- [ ] Works with no checkpoint loader
- [ ] Works with missing negative prompt
- [ ] Handles very long prompts (>1000 chars)

### Special Characters
- [ ] Prompts with emojis
- [ ] Prompts with quotes
- [ ] Prompts with newlines
- [ ] LoRA names with spaces
- [ ] LoRA names with special chars

### Large Datasets
- [ ] Generate 100+ prompts
- [ ] List loads without lag
- [ ] Search performs quickly
- [ ] Pagination smooth
- [ ] Export completes successfully

### Different Image Sizes
- [ ] Square images (512x512)
- [ ] Landscape images (1024x512)
- [ ] Portrait images (512x1024)
- [ ] Very wide images (2048x512)
- [ ] Very tall images (512x2048)
- [ ] All thumbnails maintain aspect ratio

## Error Handling

### Invalid Inputs
- [ ] Node handles corrupted image tensor
- [ ] Handles missing workflow data
- [ ] Handles invalid seed values
- [ ] Handles malformed LoRA tags

### File System Errors
- [ ] Read-only output directory
- [ ] Disk full scenario
- [ ] Missing thumbnails directory
- [ ] Database file locked

### API Errors
- [ ] Invalid prompt ID in delete request
- [ ] Negative offset in pagination
- [ ] Excessive limit value
- [ ] Malformed search query

## Performance Tests

### Memory Usage
- [ ] No memory leaks after 100 generations
- [ ] PIL images properly closed
- [ ] Database connections properly closed

### Database Performance
- [ ] Query performance with 1000 prompts
- [ ] Index usage verified
- [ ] No N+1 query problems

### UI Responsiveness
- [ ] Widget loads quickly
- [ ] Smooth scrolling in list
- [ ] No blocking operations
- [ ] Thumbnails lazy load properly

## Integration Tests

### With Standard Nodes
- [ ] Works after Save Image node
- [ ] Works after Preview Image node
- [ ] Works with VAE Decode
- [ ] Works in batch processing

### With Custom Nodes
- [ ] Compatible with custom LoRA loaders
- [ ] Compatible with custom samplers
- [ ] Compatible with custom CLIP encoders

### Multi-Node Scenarios
- [ ] Multiple Prompt Library nodes in workflow
- [ ] All nodes share same database
- [ ] No conflicts or race conditions

## Browser Compatibility

### Desktop Browsers
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari (if on Mac)

### Interface Elements
- [ ] Buttons clickable
- [ ] Inputs functional
- [ ] Thumbnails display
- [ ] Modals work properly

## Documentation Tests

- [ ] README instructions accurate
- [ ] Installation steps work
- [ ] Examples make sense
- [ ] API documentation correct
- [ ] Troubleshooting helps

## Final Checks

- [ ] No errors in ComfyUI console
- [ ] No errors in browser console
- [ ] No unclosed resources
- [ ] No orphaned files
- [ ] Database integrity intact
- [ ] Performance acceptable
- [ ] User experience smooth

## Known Limitations

Document any issues found:
- 
- 
- 

## Recommended Improvements

List any enhancement ideas:
- 
- 
-
