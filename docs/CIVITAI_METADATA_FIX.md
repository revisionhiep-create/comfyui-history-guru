# Civitai Metadata Parsing Fix

## Problem Identified

The two Civitai image files (`113830838.png` and `113717999.jpeg`) contain metadata stored in **EXIF UserComment** field, encoded as **UTF-16 (UNICODE format)**. 

### Root Cause

1. **Metadata Location**: Metadata is stored in EXIF UserComment (tag 37510), not in PNG text chunks
2. **Encoding Issue**: EXIF UserComment uses UTF-16 encoding with "UNICODE\0\0" header, which creates null bytes between characters when decoded incorrectly
3. **Parser Limitation**: The HTML parser was only checking PNG text chunks (`tEXt`, `iTXt`, `zTXt`) and not extracting EXIF data
4. **Text Cleaning**: Even when text was extracted, null bytes between characters broke the string matching in `parseA1111()`

## Solution Implemented

### 1. Enhanced Text Extraction (`extractText` function)

- **Added EXIF extraction** for both PNG (`eXIf` chunk) and JPEG (APP1 segment)
- **Added `extractEXIFUserComment` function** to properly decode UTF-16 encoded UserComment
- **Added `extractEXIFUserCommentFromJPEG` function** to extract EXIF from JPEG files
- **Added `cleanTextForParsing` function** to remove null bytes and normalize text

### 2. Improved A1111 Parser (`parseA1111` function)

- **Enhanced text cleaning** - removes control characters before parsing
- **Multiple marker variations** - handles case variations of "Negative prompt:" and "Steps:"
- **Improved regex patterns** - more flexible parameter extraction with multiple pattern attempts
- **Better error handling** - handles edge cases where markers might be missing

### 3. Key Features

- **Backward Compatible**: Existing PNG text chunk parsing still works
- **UTF-16 Support**: Properly decodes UTF-16 encoded EXIF UserComment
- **Robust Parsing**: Handles text with null bytes, control characters, and encoding issues
- **Multiple Format Support**: Works with both PNG and JPEG files

## Testing

The fix has been tested with:
- `113830838.png` - PNG file with EXIF UserComment
- `113717999.jpeg` - JPEG file with EXIF UserComment

Both files should now correctly parse:
- ✅ Positive prompt
- ✅ Negative prompt  
- ✅ Steps
- ✅ Sampler
- ✅ CFG scale
- ✅ Seed
- ✅ Size
- ✅ Model
- ✅ LoRA resources

## Technical Details

### EXIF UserComment Format

```
[8 bytes: encoding indicator] "UNICODE\0\0" or "ASCII\0\0\0"
[remaining bytes: actual text data]
```

For UTF-16 encoding:
- First 8 bytes: "UNICODE\0\0" 
- Remaining bytes: UTF-16LE encoded text
- When decoded incorrectly as UTF-8, creates null bytes between characters

### Parsing Flow

1. **Extract text** from PNG chunks OR EXIF UserComment
2. **Clean text** - remove null bytes and control characters
3. **Parse metadata** using improved `parseA1111()` function
4. **Extract parameters** using flexible regex patterns

## Files Modified

- `Guru Universal Node Version 3.3.html`
  - Enhanced `extractText()` function
  - Added `cleanTextForParsing()` function
  - Added `extractEXIFUserComment()` function
  - Added `extractEXIFUserCommentFromJPEG()` function
  - Improved `parseA1111()` function

- `Guru Manager.html` (v6.10+)
  - **Fixed cache issue**: Updated `scD()` function to reprocess files with empty/missing metadata
  - **Aligned extraction logic**: Simplified `extractEXIFUserCommentFromJPEG()` fallback to match working 3.3 implementation
  - **Simplified validation**: Removed overly complex UTF-16BE fallback checks that could cause false matches
  - **Cache reprocessing**: Files with empty metadata (`model === "?"` or missing `pos`) are now reprocessed on scan

## Tools Created

- `tools/analyze_civitai_parse_issue.py` - Comprehensive analysis tool
- `tools/extract_exif_metadata.py` - EXIF extraction tool
- `tools/civitai_exif_parser.py` - Civitai metadata parser (Python reference)

## Critical Fix (December 2024)

### Issue: Guru Manager Not Showing Metadata for Some Files

**Problem**: Files like `113717999.jpeg` and `113830838.png` showed metadata in v3.3 but not in Guru Manager.

**Root Causes Identified**:
1. **Cache preventing reprocessing**: Files were cached with empty metadata and never reprocessed
2. **Overly complex fallback logic**: Manager had extra UTF-16BE fallback checks that could interfere with extraction
3. **Validation mismatch**: Different validation patterns between versions caused inconsistent results

**Solution Applied**:
- Updated cache check: `if(!cached||!cached.m||!cached.m.pos&&!cached.m.meta||cached.m.meta&&cached.m.meta.model==="?")`
- Simplified `extractEXIFUserCommentFromJPEG()` to match 3.3's working implementation
- Removed complex UTF-16BE fallback in UNICODE marker search
- Aligned fallback validation checks to match 3.3 exactly

**Result**: Guru Manager now correctly extracts and displays metadata for all Civitai images, matching v3.3's behavior.

## Notes

- The fix maintains backward compatibility with existing metadata formats
- EXIF parsing is complex, so the implementation includes fallbacks
- Text cleaning is crucial for handling UTF-16 encoding issues
- The parser now handles multiple variations of metadata markers
- **Cache management is critical**: Files must be reprocessed if metadata extraction improves
