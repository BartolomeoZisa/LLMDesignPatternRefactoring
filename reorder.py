#!/usr/bin/env python3
import os
import shutil
import argparse
from pathlib import Path

def reorganize_folders(root_dir):
    """
    Recursively visits folders and reorganizes:
    - 'base' and 'test' folders go into a new 'base' subfolder
    - 'refactored' and 'test_refactored' folders go into a new 'refactored' subfolder
    """
    # Convert to Path object for easier handling
    root = Path(root_dir)
    
    # Walk through all directories
    for current_dir, subdirs, files in os.walk(root, topdown=False):
        current_path = Path(current_dir)
        
        # Check if current directory contains target folders
        has_base = 'base' in subdirs
        has_test = 'test' in subdirs
        has_refactored = 'refactored' in subdirs
        has_test_refactored = 'test_refactored' in subdirs
        
        # Process base and test folders
        if has_base and has_test:
            # Create new base folder
            new_base_dir = current_path / 'base_folder'
            os.makedirs(new_base_dir, exist_ok=True)
            
            # Move base folder
            shutil.move(str(current_path / 'base'), str(new_base_dir / 'base'))
            subdirs.remove('base')
            
            # Move test folder
            shutil.move(str(current_path / 'test'), str(new_base_dir / 'test'))
            subdirs.remove('test')
            
            print(f"Created base_folder with base and test in: {current_dir}")
        
        # Process refactored and test_refactored folders
        if has_refactored and has_test_refactored:
            # Create new refactored folder
            new_refactored_dir = current_path / 'refactored_folder'
            os.makedirs(new_refactored_dir, exist_ok=True)
            
            # Move refactored folder
            shutil.move(str(current_path / 'refactored'), str(new_refactored_dir / 'refactored'))
            subdirs.remove('refactored')
            
            # Move test_refactored folder
            shutil.move(str(current_path / 'test_refactored'), str(new_refactored_dir / 'test_refactored'))
            subdirs.remove('test_refactored')
            
            print(f"Created refactored_folder with refactored and test_refactored in: {current_dir}")

def main():
    parser = argparse.ArgumentParser(description='Reorganize folders recursively')
    parser.add_argument('root_dir', help='Root directory to start reorganizing from')
    args = parser.parse_args()
    
    if not os.path.isdir(args.root_dir):
        print(f"Error: {args.root_dir} is not a valid directory")
        return
    
    print(f"Starting reorganization from: {args.root_dir}")
    reorganize_folders(args.root_dir)
    print("Folder reorganization complete!")

if __name__ == "__main__":
    main()