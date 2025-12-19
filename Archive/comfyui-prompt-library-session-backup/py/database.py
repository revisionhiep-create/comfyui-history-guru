"""SQLite database operations for Prompt Library."""
import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from contextlib import contextmanager

from .config import PromptLibraryConfig


class PromptLibraryDatabase:
    """Handles all database operations for prompt history."""
    
    def __init__(self):
        self.db_path = PromptLibraryConfig.get_database_path()
        self._init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _init_database(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create prompts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_text TEXT NOT NULL,
                    negative_prompt TEXT,
                    checkpoint TEXT,
                    seed INTEGER,
                    width INTEGER,
                    height INTEGER,
                    thumbnail_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_favorite BOOLEAN DEFAULT 0,
                    hash TEXT UNIQUE
                )
            """)
            
            # Create loras table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS loras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_id INTEGER NOT NULL,
                    lora_name TEXT NOT NULL,
                    strength REAL NOT NULL,
                    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE
                )
            """)
            
            # Create indices for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_prompts_created_at 
                ON prompts(created_at DESC)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_prompts_favorite 
                ON prompts(is_favorite)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_loras_prompt_id 
                ON loras(prompt_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_loras_name 
                ON loras(lora_name)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_prompts_hash 
                ON prompts(hash)
            """)
            
            print("[Prompt Library] Database initialized at:", self.db_path)
    
    def add_prompt(self, 
                   prompt_text: str,
                   thumbnail_path: str,
                   negative_prompt: Optional[str] = None,
                   checkpoint: Optional[str] = None,
                   seed: Optional[int] = None,
                   width: Optional[int] = None,
                   height: Optional[int] = None,
                   loras: Optional[List[Dict[str, Any]]] = None,
                   hash_value: Optional[str] = None) -> Optional[int]:
        """
        Add a new prompt to the database.
        
        Args:
            prompt_text: The main prompt text
            thumbnail_path: Path to thumbnail image
            negative_prompt: Negative prompt text
            checkpoint: Model/checkpoint name
            seed: Generation seed
            width: Image width
            height: Image height
            loras: List of dicts with 'name' and 'strength' keys
            hash_value: Hash for deduplication
        
        Returns:
            prompt_id if successful, None if duplicate or error
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if hash exists (duplicate)
                if hash_value:
                    cursor.execute("SELECT id FROM prompts WHERE hash = ?", (hash_value,))
                    if cursor.fetchone():
                        print(f"[Prompt Library] Duplicate prompt detected, skipping")
                        return None
                
                # Insert prompt
                cursor.execute("""
                    INSERT INTO prompts 
                    (prompt_text, negative_prompt, checkpoint, seed, width, height, 
                     thumbnail_path, hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (prompt_text, negative_prompt, checkpoint, seed, width, height,
                      thumbnail_path, hash_value))
                
                prompt_id = cursor.lastrowid
                
                # Insert LoRAs if provided
                if loras:
                    for lora in loras:
                        cursor.execute("""
                            INSERT INTO loras (prompt_id, lora_name, strength)
                            VALUES (?, ?, ?)
                        """, (prompt_id, lora.get('name', ''), lora.get('strength', 1.0)))
                
                print(f"[Prompt Library] Added prompt #{prompt_id}")
                return prompt_id
                
        except Exception as e:
            print(f"[Prompt Library] Error adding prompt: {e}")
            return None
    
    def get_prompts(self, 
                    limit: int = 50,
                    offset: int = 0,
                    search_lora: Optional[str] = None,
                    sort_by: str = "date",
                    favorites_only: bool = False) -> List[Dict]:
        """
        Retrieve prompts with optional filtering.
        
        Args:
            limit: Maximum number of results
            offset: Pagination offset
            search_lora: Filter by LoRA name
            sort_by: Sort method ("date" or "alphabetical")
            favorites_only: Only return favorited prompts
        
        Returns:
            List of prompt dictionaries with associated LoRAs
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Build query
                query = "SELECT * FROM prompts WHERE 1=1"
                params = []
                
                if favorites_only:
                    query += " AND is_favorite = 1"
                
                if search_lora:
                    query += """ AND id IN (
                        SELECT prompt_id FROM loras 
                        WHERE lora_name LIKE ?
                    )"""
                    params.append(f"%{search_lora}%")
                
                # Sorting
                if sort_by == "alphabetical":
                    query += " ORDER BY prompt_text ASC"
                else:  # date (default)
                    query += " ORDER BY created_at DESC"
                
                query += " LIMIT ? OFFSET ?"
                params.extend([limit, offset])
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                prompts = []
                for row in rows:
                    prompt_dict = dict(row)
                    
                    # Get associated LoRAs
                    cursor.execute("""
                        SELECT lora_name, strength 
                        FROM loras 
                        WHERE prompt_id = ?
                    """, (prompt_dict['id'],))
                    
                    loras = [
                        {'name': lora_row['lora_name'], 'strength': lora_row['strength']}
                        for lora_row in cursor.fetchall()
                    ]
                    
                    prompt_dict['loras'] = loras
                    prompts.append(prompt_dict)
                
                return prompts
                
        except Exception as e:
            print(f"[Prompt Library] Error retrieving prompts: {e}")
            return []
    
    def toggle_favorite(self, prompt_id: int) -> bool:
        """Toggle favorite status for a prompt."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE prompts 
                    SET is_favorite = NOT is_favorite 
                    WHERE id = ?
                """, (prompt_id,))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"[Prompt Library] Error toggling favorite: {e}")
            return False
    
    def delete_prompt(self, prompt_id: int) -> bool:
        """Delete a prompt and its associated data."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get thumbnail path for deletion
                cursor.execute("SELECT thumbnail_path FROM prompts WHERE id = ?", (prompt_id,))
                row = cursor.fetchone()
                
                if row and row['thumbnail_path']:
                    # Delete thumbnail file
                    try:
                        if os.path.exists(row['thumbnail_path']):
                            os.remove(row['thumbnail_path'])
                    except:
                        pass
                
                # Delete from database (LoRAs will cascade)
                cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
                
                print(f"[Prompt Library] Deleted prompt #{prompt_id}")
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"[Prompt Library] Error deleting prompt: {e}")
            return False
    
    def cleanup_old_prompts(self, keep_count: int):
        """Delete oldest prompts exceeding the keep_count limit."""
        if keep_count < 1:
            print("[Prompt Library] Invalid keep_count, skipping cleanup")
            return 0
            
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get IDs of prompts to delete
                cursor.execute("""
                    SELECT id, thumbnail_path FROM prompts 
                    ORDER BY created_at DESC 
                    LIMIT -1 OFFSET ?
                """, (keep_count,))
                
                old_prompts = cursor.fetchall()
                deleted_count = 0
                
                for prompt in old_prompts:
                    try:
                        # Delete thumbnail file
                        if prompt['thumbnail_path'] and os.path.exists(prompt['thumbnail_path']):
                            try:
                                os.remove(prompt['thumbnail_path'])
                            except OSError as e:
                                print(f"[Prompt Library] Warning: Could not delete thumbnail: {e}")
                        
                        # Delete from database (cascade will handle LoRAs)
                        cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt['id'],))
                        deleted_count += 1
                    except Exception as e:
                        print(f"[Prompt Library] Error deleting prompt {prompt['id']}: {e}")
                        continue
                
                if deleted_count > 0:
                    print(f"[Prompt Library] Cleaned up {deleted_count} old prompts")
                
                return deleted_count
                
        except Exception as e:
            print(f"[Prompt Library] Error during cleanup: {e}")
            import traceback
            traceback.print_exc()
            return 0
    
    def get_total_count(self, search_lora: Optional[str] = None, favorites_only: bool = False) -> int:
        """Get total count of prompts matching criteria."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT COUNT(*) as count FROM prompts WHERE 1=1"
                params = []
                
                if favorites_only:
                    query += " AND is_favorite = 1"
                
                if search_lora:
                    query += """ AND id IN (
                        SELECT prompt_id FROM loras 
                        WHERE lora_name LIKE ?
                    )"""
                    params.append(f"%{search_lora}%")
                
                cursor.execute(query, params)
                result = cursor.fetchone()
                return result['count'] if result else 0
                
        except Exception as e:
            print(f"[Prompt Library] Error getting count: {e}")
            return 0
    
    def export_to_csv(self, output_path: str) -> bool:
        """Export all prompts to CSV file."""
        try:
            import csv
            
            prompts = self.get_prompts(limit=PromptLibraryConfig.MAX_SEARCH_RESULTS)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'prompt_text', 'negative_prompt', 'checkpoint', 
                             'seed', 'width', 'height', 'loras', 'created_at', 'is_favorite']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for prompt in prompts:
                    # Format LoRAs as string
                    loras_str = "; ".join([
                        f"{lora['name']} ({lora['strength']:.2f})"
                        for lora in prompt.get('loras', [])
                    ])
                    
                    writer.writerow({
                        'id': prompt['id'],
                        'prompt_text': prompt['prompt_text'],
                        'negative_prompt': prompt.get('negative_prompt', ''),
                        'checkpoint': prompt.get('checkpoint', ''),
                        'seed': prompt.get('seed', ''),
                        'width': prompt.get('width', ''),
                        'height': prompt.get('height', ''),
                        'loras': loras_str,
                        'created_at': prompt['created_at'],
                        'is_favorite': prompt.get('is_favorite', 0)
                    })
            
            print(f"[Prompt Library] Exported to {output_path}")
            return True
            
        except Exception as e:
            print(f"[Prompt Library] Error exporting to CSV: {e}")
            return False
