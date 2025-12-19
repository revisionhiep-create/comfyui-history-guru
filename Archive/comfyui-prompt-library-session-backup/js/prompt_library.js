/**
 * Prompt Library Widget for ComfyUI
 * Displays prompt history with thumbnails, search, and filtering
 */

import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";
import { api } from "../../scripts/api.js";

const WIDGET_WIDTH = 1080;
const WIDGET_HEIGHT = 1080;
const THUMBNAIL_SIZE = 120;

class PromptLibraryWidget {
    constructor(node) {
        this.node = node;
        this.prompts = [];
        this.currentPage = 0;
        this.pageSize = 20;
        this.totalCount = 0;
        this.searchLora = "";
        this.sortBy = "date";
        this.favoritesOnly = false;
        
        this.container = null;
        this.isExpanded = false;
    }
    
    async loadPrompts() {
        try {
            const params = new URLSearchParams({
                limit: this.pageSize,
                offset: this.currentPage * this.pageSize,
                sort_by: this.sortBy,
                favorites_only: this.favoritesOnly ? '1' : '0'
            });
            
            if (this.searchLora) {
                params.append('search_lora', this.searchLora);
            }
            
            const response = await fetch(`/prompt_library/api/prompts?${params}`);
            const data = await response.json();
            
            this.prompts = data.prompts || [];
            this.totalCount = data.total || 0;
            
            // Debug: Check what data we're receiving
            if (this.prompts.length > 0) {
                console.log('[Prompt Library] Sample prompt data:', this.prompts[0]);
            }
            
            this.render();
        } catch (error) {
            console.error('[Prompt Library] Error loading prompts:', error);
        }
    }
    
    async toggleFavorite(promptId) {
        try {
            const response = await fetch(`/prompt_library/api/favorite/${promptId}`, {
                method: 'POST'
            });
            
            if (response.ok) {
                await this.loadPrompts();
            }
        } catch (error) {
            console.error('[Prompt Library] Error toggling favorite:', error);
        }
    }
    
    async deletePrompt(promptId) {
        if (!confirm('Delete this prompt from history?')) {
            return;
        }
        
        try {
            const response = await fetch(`/prompt_library/api/prompt/${promptId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                await this.loadPrompts();
            }
        } catch (error) {
            console.error('[Prompt Library] Error deleting prompt:', error);
        }
    }
    
    async exportCSV() {
        try {
            window.open('/prompt_library/api/export', '_blank');
        } catch (error) {
            console.error('[Prompt Library] Error exporting CSV:', error);
        }
    }
    
    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            console.log('[Prompt Library] Copied to clipboard');
        }).catch(err => {
            console.error('[Prompt Library] Failed to copy:', err);
        });
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString();
    }
    
    createPromptCard(prompt) {
        const card = document.createElement('div');
        card.className = 'prompt-library-card';
        card.dataset.expanded = 'false';
        card.dataset.promptId = prompt.id;
        
        card.style.cssText = `
            margin: 5px 0;
            padding: 8px;
            background: #2a2a2a;
            border-radius: 5px;
            border-left: 3px solid ${prompt.is_favorite ? '#ffd700' : '#555'};
            cursor: pointer;
            transition: background 0.2s;
        `;
        
        card.onmouseenter = () => {
            if (card.dataset.expanded === 'false') {
                card.style.background = '#333';
            }
        };
        card.onmouseleave = () => {
            if (card.dataset.expanded === 'false') {
                card.style.background = '#2a2a2a';
            }
        };
        
        // Header with date and actions
        const header = document.createElement('div');
        header.style.cssText = 'display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;';
        
        const dateEl = document.createElement('span');
        dateEl.textContent = this.formatDate(prompt.created_at);
        dateEl.style.cssText = 'color: #888; font-size: 11px;';
        
        const actions = document.createElement('div');
        actions.style.cssText = 'display: flex; gap: 5px;';
        
        // Favorite button
        const favBtn = document.createElement('button');
        favBtn.textContent = prompt.is_favorite ? '⭐' : '☆';
        favBtn.title = 'Toggle Favorite';
        favBtn.style.cssText = 'cursor: pointer; background: none; border: none; font-size: 14px; padding: 2px;';
        favBtn.onclick = (e) => {
            e.stopPropagation();
            this.toggleFavorite(prompt.id);
        };
        
        // Delete button
        const delBtn = document.createElement('button');
        delBtn.textContent = '🗑️';
        delBtn.title = 'Delete';
        delBtn.style.cssText = 'cursor: pointer; background: none; border: none; font-size: 12px; padding: 2px;';
        delBtn.onclick = (e) => {
            e.stopPropagation();
            this.deletePrompt(prompt.id);
        };
        
        actions.appendChild(favBtn);
        actions.appendChild(delBtn);
        
        header.appendChild(dateEl);
        header.appendChild(actions);
        
        // Compact preview (always visible)
        const preview = document.createElement('div');
        preview.style.cssText = 'font-size: 12px; color: #ddd;';
        const previewText = prompt.prompt_text.substring(0, 80) + (prompt.prompt_text.length > 80 ? '...' : '');
        preview.textContent = previewText;
        
        // Quick info (always visible)
        const quickInfo = document.createElement('div');
        quickInfo.style.cssText = 'font-size: 10px; color: #888; margin-top: 2px;';
        let info = [];
        if (prompt.width && prompt.height) info.push(`${prompt.width}×${prompt.height}`);
        if (prompt.seed !== null) info.push(`Seed: ${prompt.seed}`);
        if (prompt.loras && prompt.loras.length > 0) info.push(`${prompt.loras.length} LoRA(s)`);
        quickInfo.textContent = info.join(' • ');
        
        // Expanded details (hidden by default)
        const details = document.createElement('div');
        details.style.cssText = 'display: none; margin-top: 10px; padding-top: 10px; border-top: 1px solid #444;';
        
        // Thumbnail (in details)
        const thumbnailContainer = document.createElement('div');
        thumbnailContainer.style.cssText = 'margin-bottom: 10px; text-align: center; position: relative;';
        
        const thumbnail = document.createElement('img');
        const filename = prompt.thumbnail_path ? prompt.thumbnail_path.split('/').pop().split('\\').pop() : '';
        if (filename) {
            thumbnail.src = `/prompt_library/thumbnail/${filename}`;
            thumbnail.onerror = () => {
                console.error('[Prompt Library] Failed to load thumbnail:', thumbnail.src);
                thumbnail.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300"><rect fill="%23333" width="300" height="300"/><text x="50%" y="50%" fill="%23888" text-anchor="middle" dy=".3em">Image not found</text></svg>';
            };
        }
        thumbnail.style.cssText = `
            max-width: 100%;
            max-height: 500px;
            object-fit: contain;
            border-radius: 3px;
            cursor: pointer;
            display: block;
            margin: 0 auto;
        `;
        thumbnail.onclick = (e) => {
            e.stopPropagation();
            if (filename) {
                window.open(`/prompt_library/thumbnail/${filename}`, '_blank');
            }
        };
        thumbnailContainer.appendChild(thumbnail);
        
        // Metadata info below image
        const metaInfo = document.createElement('div');
        metaInfo.style.cssText = 'margin-top: 10px; padding: 8px; background: #252525; border-radius: 3px; font-size: 11px; color: #aaa; line-height: 1.6;';
        
        const metaLines = [];
        
        if (prompt.checkpoint) {
            metaLines.push(`<span style="color: #7af;">Checkpoint:</span> ${prompt.checkpoint}`);
        }
        
        if (prompt.loras && prompt.loras.length > 0) {
            const lorasList = prompt.loras.map(l => `${l.name} (${l.strength.toFixed(2)})`).join(', ');
            metaLines.push(`<span style="color: #fa7;">LoRAs:</span> ${lorasList}`);
        }
        
        if (metaLines.length > 0) {
            metaInfo.innerHTML = metaLines.join('<br>');
        } else {
            metaInfo.textContent = 'No metadata available';
        }
        
        // Single copy button for prompt
        const copyBtnContainer = document.createElement('div');
        copyBtnContainer.style.cssText = 'text-align: center; margin-top: 10px;';
        
        const copyBtn = document.createElement('button');
        copyBtn.textContent = '📋 Copy Prompt';
        copyBtn.title = 'Copy full prompt to clipboard';
        copyBtn.style.cssText = `
            font-size: 14px;
            padding: 8px 20px;
            background: #4a4a4a;
            border: 1px solid #666;
            color: #ddd;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        `;
        copyBtn.onmouseenter = () => {
            copyBtn.style.background = '#555';
        };
        copyBtn.onmouseleave = () => {
            copyBtn.style.background = '#4a4a4a';
        };
        copyBtn.onclick = (e) => {
            e.stopPropagation();
            this.copyToClipboard(prompt.prompt_text);
            copyBtn.textContent = '✓ Copied!';
            copyBtn.style.background = '#4a7c59';
            setTimeout(() => {
                copyBtn.textContent = '📋 Copy Prompt';
                copyBtn.style.background = '#4a4a4a';
            }, 2000);
        };
        copyBtnContainer.appendChild(copyBtn);
        
        // Build details - image, metadata, and copy button
        details.appendChild(thumbnailContainer);
        details.appendChild(metaInfo);
        details.appendChild(copyBtnContainer);
        
        // Assemble card
        card.appendChild(header);
        card.appendChild(preview);
        card.appendChild(quickInfo);
        card.appendChild(details);
        
        // Click to expand/collapse
        card.onclick = () => {
            const isExpanded = card.dataset.expanded === 'true';
            if (isExpanded) {
                details.style.display = 'none';
                card.dataset.expanded = 'false';
                card.style.background = '#2a2a2a';
            } else {
                details.style.display = 'block';
                card.dataset.expanded = 'true';
                card.style.background = '#333';
            }
        };
        
        return card;
    }
    

    
    render() {
        if (!this.container) return;
        
        this.container.innerHTML = '';
        
        // Controls
        const controls = document.createElement('div');
        controls.style.cssText = 'padding: 10px; background: #1a1a1a; border-radius: 5px; margin-bottom: 10px;';
        
        // Search
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Search by LoRA name...';
        searchInput.value = this.searchLora;
        searchInput.style.cssText = 'width: 200px; margin-right: 10px; padding: 5px; background: #2a2a2a; border: 1px solid #444; color: #ddd; border-radius: 3px;';
        searchInput.onchange = () => {
            this.searchLora = searchInput.value;
            this.currentPage = 0;
            this.loadPrompts();
        };
        
        // Sort
        const sortSelect = document.createElement('select');
        sortSelect.style.cssText = 'margin-right: 10px; padding: 5px; background: #2a2a2a; border: 1px solid #444; color: #ddd; border-radius: 3px;';
        sortSelect.innerHTML = `
            <option value="date">Sort by Date</option>
            <option value="alphabetical">Sort Alphabetically</option>
        `;
        sortSelect.value = this.sortBy;
        sortSelect.onchange = () => {
            this.sortBy = sortSelect.value;
            this.currentPage = 0;
            this.loadPrompts();
        };
        
        // Favorites filter
        const favCheckbox = document.createElement('input');
        favCheckbox.type = 'checkbox';
        favCheckbox.checked = this.favoritesOnly;
        favCheckbox.id = 'fav-filter';
        favCheckbox.style.cssText = 'margin-right: 5px;';
        favCheckbox.onchange = () => {
            this.favoritesOnly = favCheckbox.checked;
            this.currentPage = 0;
            this.loadPrompts();
        };
        
        const favLabel = document.createElement('label');
        favLabel.htmlFor = 'fav-filter';
        favLabel.textContent = 'Favorites Only';
        favLabel.style.cssText = 'color: #ddd; margin-right: 10px; font-size: 12px;';
        
        // Export button
        const exportBtn = document.createElement('button');
        exportBtn.textContent = '📥 Export CSV';
        exportBtn.style.cssText = 'padding: 5px 10px; background: #4a4a4a; border: 1px solid #666; color: #ddd; border-radius: 3px; cursor: pointer;';
        exportBtn.onclick = () => this.exportCSV();
        
        controls.appendChild(searchInput);
        controls.appendChild(sortSelect);
        controls.appendChild(favCheckbox);
        controls.appendChild(favLabel);
        controls.appendChild(exportBtn);
        
        // Stats
        const stats = document.createElement('div');
        stats.style.cssText = 'margin-top: 5px; font-size: 11px; color: #888;';
        stats.textContent = `Showing ${this.prompts.length} of ${this.totalCount} prompts`;
        controls.appendChild(stats);
        
        this.container.appendChild(controls);
        
        // Prompts list
        const listContainer = document.createElement('div');
        listContainer.style.cssText = 'height: 400px; max-height: 60vh; overflow-y: auto; padding: 5px;';
        
        if (this.prompts.length === 0) {
            const empty = document.createElement('div');
            empty.textContent = 'No prompts found. Generate some images to start building your library!';
            empty.style.cssText = 'text-align: center; color: #888; padding: 40px;';
            listContainer.appendChild(empty);
        } else {
            this.prompts.forEach(prompt => {
                listContainer.appendChild(this.createPromptCard(prompt));
            });
        }
        
        this.container.appendChild(listContainer);
        
        // Pagination
        if (this.totalCount > this.pageSize) {
            const pagination = document.createElement('div');
            pagination.style.cssText = 'display: flex; justify-content: center; margin-top: 10px; gap: 5px;';
            
            const totalPages = Math.ceil(this.totalCount / this.pageSize);
            
            const prevBtn = document.createElement('button');
            prevBtn.textContent = '← Previous';
            prevBtn.disabled = this.currentPage === 0;
            prevBtn.style.cssText = `padding: 5px 10px; background: ${this.currentPage === 0 ? '#2a2a2a' : '#4a4a4a'}; border: 1px solid #666; color: #ddd; border-radius: 3px; cursor: ${this.currentPage === 0 ? 'not-allowed' : 'pointer'};`;
            prevBtn.onclick = () => {
                if (this.currentPage > 0) {
                    this.currentPage--;
                    this.loadPrompts();
                }
            };
            
            const pageInfo = document.createElement('span');
            pageInfo.textContent = `Page ${this.currentPage + 1} of ${totalPages}`;
            pageInfo.style.cssText = 'padding: 5px 10px; color: #ddd; line-height: 30px;';
            
            const nextBtn = document.createElement('button');
            nextBtn.textContent = 'Next →';
            nextBtn.disabled = this.currentPage >= totalPages - 1;
            nextBtn.style.cssText = `padding: 5px 10px; background: ${this.currentPage >= totalPages - 1 ? '#2a2a2a' : '#4a4a4a'}; border: 1px solid #666; color: #ddd; border-radius: 3px; cursor: ${this.currentPage >= totalPages - 1 ? 'not-allowed' : 'pointer'};`;
            nextBtn.onclick = () => {
                if (this.currentPage < totalPages - 1) {
                    this.currentPage++;
                    this.loadPrompts();
                }
            };
            
            pagination.appendChild(prevBtn);
            pagination.appendChild(pageInfo);
            pagination.appendChild(nextBtn);
            
            this.container.appendChild(pagination);
        }
    }
}

// Register the extension
// No UI or widgets for PromptLibrary node. Pure backend node.
