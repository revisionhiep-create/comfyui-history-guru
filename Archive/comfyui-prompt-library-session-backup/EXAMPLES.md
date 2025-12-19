# ComfyUI Prompt Library - Example Workflows

## Basic Usage

### Simple Image Generation with History
```
1. Add a basic text-to-image workflow
2. Add the Prompt Library node at the end
3. Connect the images output
4. Generate images - they'll be automatically recorded
5. Click "Show Library" button to browse your history
```

### Workflow Structure
```
Load Checkpoint → CLIP Text Encode (Positive) ┐
                                               ├→ KSampler → VAE Decode → Prompt Library
Load LoRA ────────→ CLIP Text Encode (Negative)┘
```

## Advanced Setup

### With Multiple LoRAs
The node automatically tracks all LoRAs used in your workflow, recording their names and strength values.

### With Different Checkpoints
Switch between models freely - the node records which checkpoint was used for each generation.

### Batch Generation
The node handles batch generations efficiently, creating separate entries for unique prompt combinations.

## Tips

1. **Connect After Save Image**: You can chain Prompt Library after Save Image to record AND save
2. **Use Explicit Inputs**: Override auto-detection by providing explicit prompt/seed/checkpoint inputs
3. **Search Your LoRAs**: Use the search bar to find all generations using specific LoRAs
4. **Star Your Favorites**: Mark your best results for easy retrieval
5. **Export for Analysis**: Export to CSV to analyze your prompt patterns in Excel/Google Sheets
