#!/usr/bin/env python3
"""
Backup tool - Creates timestamped backups before making code changes.
MANDATORY: Run this before editing any file.
"""

import shutil
import sys
from pathlib import Path
from datetime import datetime

def create_backup(file_path):
    """Create a timestamped backup of a file."""
    source = Path(file_path)
    
    if not source.exists():
        print(f"Error: File '{file_path}' does not exist")
        return False
    
    # Create backup directory if it doesn't exist (support both root and tools folder)
    backup_dir = Path('backup')
    if not backup_dir.exists():
        backup_dir = Path('../backup')
    backup_dir.mkdir(exist_ok=True, parents=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    stem = source.stem
    suffix = source.suffix
    backup_name = f"{stem}_{timestamp}{suffix}"
    backup_path = backup_dir / backup_name
    
    # Copy file to backup
    try:
        shutil.copy2(source, backup_path)
        print(f"[OK] Backup created: {backup_path}")
        return True
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

def list_backups(file_pattern=None):
    """List all backups, optionally filtered by file pattern."""
    backup_dir = Path('backup')
    if not backup_dir.exists():
        backup_dir = Path('../backup')
    if not backup_dir.exists():
        print("No backup directory found")
        return []
    
    backups = sorted(backup_dir.glob('*'), key=lambda p: p.stat().st_mtime, reverse=True)
    
    if file_pattern:
        backups = [b for b in backups if file_pattern in b.name]
    
    return backups

def restore_backup(backup_path, target_path=None):
    """Restore a file from backup."""
    backup = Path(backup_path)
    
    if not backup.exists():
        print(f"Error: Backup '{backup_path}' does not exist")
        return False
    
    # Determine target path
    if target_path:
        target = Path(target_path)
    else:
        # Extract original filename (remove timestamp)
        name_parts = backup.stem.rsplit('_', 1)
        if len(name_parts) == 2 and len(name_parts[1]) == 15:  # YYYYMMDD_HHMMSS format
            original_name = name_parts[0] + backup.suffix
        else:
            original_name = backup.name
        target = Path(original_name)
    
    try:
        shutil.copy2(backup, target)
        print(f"[OK] Restored: {backup.name} -> {target}")
        return True
    except Exception as e:
        print(f"Error restoring backup: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python backup_file.py <file>           - Create backup")
        print("  python backup_file.py list [pattern]   - List backups")
        print("  python backup_file.py restore <backup> [target] - Restore backup")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'backup' or (command != 'list' and command != 'restore'):
        # Treat as backup command
        file_path = command if command != 'backup' else sys.argv[2]
        create_backup(file_path)
    
    elif command == 'list':
        pattern = sys.argv[2] if len(sys.argv) > 2 else None
        backups = list_backups(pattern)
        if backups:
            print(f"\nFound {len(backups)} backup(s):")
            for backup in backups[:20]:  # Show last 20
                mtime = datetime.fromtimestamp(backup.stat().st_mtime)
                print(f"  {backup.name} ({mtime.strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            print("No backups found")
    
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("Error: Specify backup file to restore")
            sys.exit(1)
        backup_path = sys.argv[2]
        target_path = sys.argv[3] if len(sys.argv) > 3 else None
        restore_backup(backup_path, target_path)
    
    else:
        print(f"Unknown command: {command}")
