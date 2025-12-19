/**
 * Prompt Library Web UI
 */

class PromptLibraryApp {
    constructor() {
        this.prompts = [];
        this.currentPage = 0;
        this.pageSize = 20;
        this.totalCount = 0;
        this.searchLora = '';
        this.sortBy = 'date';
        this.favoritesOnly = false;
        
        this.init();
        this.setupEventListeners();
        this.loadPrompts();
        
        // Auto-refresh every 30 seconds
        setInterval(() => this.loadPrompts(), 30000);
    }
    
    init() {
        this.promptsList = document.getElementById('promptsList');
        this.searchInput = document.getElementById('searchLora');
        this.sortSelect = document.getElementById('sortBy');
        this.favoritesCheckbox = document.getElementById('favoritesOnly');
    }
    
    setupEventListeners() {
        // Search
        document.getElementById('searchBtn').onclick = () => {
            this.searchLora = this.searchInput.value.trim();
            this.currentPage = 0;
            this.loadPrompts();
        };
        
        document.getElementById('clearSearchBtn').onclick = () => {
            this.searchInput.value = '';
            this.searchLora = '';
            this.currentPage = 0;
            this.loadPrompts();
        };
        
        this.searchInput.onkeypress = (e) => {
            if (e.key === 'Enter') {
                document.getElementById('searchBtn').click();
            }
        };
        
        // Sort
        this.sortSelect.onchange = () => {
            this.sortBy = this.sortSelect.value;
            this.currentPage = 0;
            this.loadPrompts();
        };
        
        // Favorites filter
        this.favoritesCheckbox.onchange = () => {
            this.favoritesOnly = this.favoritesCheckbox.checked;
            this.currentPage = 0;
            this.loadPrompts();
        };
        
        // Refresh
        document.getElementById('refreshBtn').onclick = () => {
            this.loadPrompts();
        };
        
        // Export
        document.getElementById('exportBtn').onclick = () => {
            this.exportCSV();
        };
        
        // Pagination
        document.getElementById('prevBtn').onclick = () => {
            if (this.currentPage > 0) {
                this.currentPage--;
                this.loadPrompts();
            }
        };
        
        document.getElementById('nextBtn').onclick = () => {
            const totalPages = Math.ceil(this.totalCount / this.pageSize);
            if (this.currentPage < totalPages - 1) {
                this.currentPage++;
                this.loadPrompts();
            }
        };
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
            
            this.render();
        } catch (error) {
            console.error('[Prompt Library] Error loading prompts:', error);
            this.promptsList.innerHTML = '<div class="empty-state">Error loading prompts. Please try again.</div>';
        }
    }
    
    render() {
        // Update header count
        document.getElementById('promptCount').textContent = 
            `${this.totalCount} prompt${this.totalCount !== 1 ? 's' : ''} in library`;
        
        // Render prompts list
        if (this.prompts.length === 0) {
            this.promptsList.innerHTML = '<div class="empty-state">No prompts found. Generate some images to start building your library!</div>';
            this.updatePagination();
            return;
        }
        
        this.promptsList.innerHTML = '';
        this.prompts.forEach(prompt => {
            const card = this.createPromptCard(prompt);
            this.promptsList.appendChild(card);
        });
        
        this.updatePagination();
    }
    
    createPromptCard(prompt) {
        const card = document.createElement('div');
        card.className = `prompt-card${prompt.is_favorite ? ' favorite' : ''}`;
        card.dataset.promptId = prompt.id;
        card.dataset.expanded = 'false';
        
        // Header
        const header = document.createElement('div');
        header.className = 'card-header';
        
        const date = document.createElement('div');
        date.className = 'card-date';
        date.textContent = this.formatDate(prompt.created_at);
        
        const actions = document.createElement('div');
        actions.className = 'card-actions';
        
        const favBtn = document.createElement('button');
        favBtn.className = 'icon-btn';
        favBtn.textContent = prompt.is_favorite ? '⭐' : '☆';
        favBtn.title = 'Toggle Favorite';
        favBtn.onclick = (e) => {
            e.stopPropagation();
            this.toggleFavorite(prompt.id);
        };
        
        const delBtn = document.createElement('button');
        delBtn.className = 'icon-btn';
        delBtn.textContent = '🗑️';
        delBtn.title = 'Delete';
        delBtn.onclick = (e) => {
            e.stopPropagation();
            this.deletePrompt(prompt.id);
        };
        
        actions.appendChild(favBtn);
        actions.appendChild(delBtn);
        
        header.appendChild(date);
        header.appendChild(actions);
        
        // Preview
        const preview = document.createElement('div');
        preview.className = 'card-preview';
        const previewText = prompt.prompt_text.substring(0, 100) + (prompt.prompt_text.length > 100 ? '...' : '');
        preview.textContent = previewText;
        
        // Quick info
        const quickInfo = document.createElement('div');
        quickInfo.className = 'card-quick-info';
        const info = [];
        if (prompt.width && prompt.height) info.push(`${prompt.width}×${prompt.height}`);
        if (prompt.seed !== null) info.push(`Seed: ${prompt.seed}`);
        if (prompt.checkpoint) info.push(`Model: ${prompt.checkpoint.split('/').pop().split('\\').pop()}`);
        if (prompt.loras && prompt.loras.length > 0) info.push(`${prompt.loras.length} LoRA(s)`);
        quickInfo.textContent = info.join(' • ');
        
        // Details (hidden by default)
        const details = document.createElement('div');
        details.className = 'card-details';
        
        // Thumbnail
        const thumbnailContainer = document.createElement('div');
        thumbnailContainer.className = 'thumbnail-container';
        
        const thumbnail = document.createElement('img');
        const filename = prompt.thumbnail_path ? prompt.thumbnail_path.split('/').pop().split('\\').pop() : '';
        if (filename) {
            thumbnail.src = `/prompt_library/thumbnail/${filename}`;
            thumbnail.onerror = () => {
                thumbnail.style.display = 'none';
            };
            thumbnail.onclick = (e) => {
                e.stopPropagation();
                window.open(`/prompt_library/thumbnail/${filename}`, '_blank');
            };
        }
        thumbnailContainer.appendChild(thumbnail);
        
        // Metadata
        const metadata = document.createElement('div');
        metadata.className = 'metadata-box';
        
        const metaLines = [];
        if (prompt.checkpoint) {
            metaLines.push(`<div><span class="metadata-label">Checkpoint:</span> ${prompt.checkpoint}</div>`);
        }
        if (prompt.loras && prompt.loras.length > 0) {
            const lorasList = prompt.loras.map(l => `${l.name} (${l.strength.toFixed(2)})`).join(', ');
            metaLines.push(`<div><span class="metadata-label">LoRAs:</span> ${lorasList}</div>`);
        }
        if (prompt.width && prompt.height) {
            metaLines.push(`<div><span class="metadata-label">Size:</span> ${prompt.width} × ${prompt.height}</div>`);
        }
        if (prompt.seed !== null) {
            metaLines.push(`<div><span class="metadata-label">Seed:</span> ${prompt.seed}</div>`);
        }
        
        metadata.innerHTML = metaLines.length > 0 ? metaLines.join('') : '<div style="color: #666;">No metadata available</div>';
        
        // Copy button
        const copyBtnContainer = document.createElement('div');
        copyBtnContainer.className = 'copy-btn-container';
        
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.textContent = '📋 Copy Prompt';
        copyBtn.onclick = (e) => {
            e.stopPropagation();
            this.copyToClipboard(prompt.prompt_text, copyBtn);
        };
        copyBtnContainer.appendChild(copyBtn);
        
        // Assemble details
        details.appendChild(thumbnailContainer);
        details.appendChild(metadata);
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
                details.classList.remove('visible');
                card.classList.remove('expanded');
                card.dataset.expanded = 'false';
            } else {
                details.classList.add('visible');
                card.classList.add('expanded');
                card.dataset.expanded = 'true';
            }
        };
        
        return card;
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
    
    copyToClipboard(text, button) {
        navigator.clipboard.writeText(text).then(() => {
            const originalText = button.textContent;
            button.textContent = '✓ Copied!';
            button.classList.add('copied');
            setTimeout(() => {
                button.textContent = originalText;
                button.classList.remove('copied');
            }, 2000);
        }).catch(err => {
            console.error('[Prompt Library] Error copying to clipboard:', err);
            alert('Failed to copy to clipboard');
        });
    }
    
    async exportCSV() {
        try {
            window.open('/prompt_library/api/export', '_blank');
        } catch (error) {
            console.error('[Prompt Library] Error exporting CSV:', error);
        }
    }
    
    updatePagination() {
        const totalPages = Math.ceil(this.totalCount / this.pageSize);
        const currentPageNum = this.currentPage + 1;
        
        document.getElementById('pageInfo').textContent = `Page ${currentPageNum} of ${Math.max(1, totalPages)}`;
        
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        
        prevBtn.disabled = this.currentPage === 0;
        nextBtn.disabled = this.currentPage >= totalPages - 1 || totalPages === 0;
        
        prevBtn.style.opacity = prevBtn.disabled ? '0.5' : '1';
        nextBtn.style.opacity = nextBtn.disabled ? '0.5' : '1';
        prevBtn.style.cursor = prevBtn.disabled ? 'not-allowed' : 'pointer';
        nextBtn.style.cursor = nextBtn.disabled ? 'not-allowed' : 'pointer';
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new PromptLibraryApp());
} else {
    new PromptLibraryApp();
}
