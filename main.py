#!/usr/bin/env python3
"""
File Organizer CLI Tool

A command-line utility that organizes files in a directory based on their file extensions.
Files are moved into categorized folders for better organization.
"""

import os
import shutil
import argparse
from datetime import datetime
import logging

def setup_logger():
    """Configure logging for the application"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"file_organizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def get_category(file_extension):
    """
    Determine the category folder based on file extension
    """
    extension = file_extension.lower()
    
    categories = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.tiff', '.webp'],
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
        'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
        'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.ts', '.jsx', '.json'],
    }
    
    for category, extensions in categories.items():
        if extension in extensions:
            return category
    
    return 'others'

def organize_files(directory, create_category_folders=True, dry_run=False, recursive=False):
    """
    Organize files in the given directory into category folders
    """
    logger = logging.getLogger(__name__)
    
    if not os.path.exists(directory):
        logger.error(f"Directory not found: {directory}")
        return False
    
    if not os.path.isdir(directory):
        logger.error(f"Not a directory: {directory}")
        return False
    
    total_files = 0
    organized_files = 0
    skipped_files = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip if not recursive and not in the top directory
        if not recursive and root != directory:
            continue

        for filename in files:
            # Skip hidden files
            if filename.startswith('.'):
                continue
                
            file_path = os.path.join(root, filename)
            
            # Skip if the file is a symbolic link
            if os.path.islink(file_path):
                logger.info(f"Skipping symbolic link: {file_path}")
                skipped_files += 1
                continue
                
            total_files += 1
            
            # Get the file extension
            _, file_extension = os.path.splitext(filename)
            
            if not file_extension:
                logger.info(f"Skipping file without extension: {filename}")
                skipped_files += 1
                continue
            
            # Determine the category
            category = get_category(file_extension)
            
            # Create category directory if it doesn't exist
            category_path = os.path.join(directory, category)
            if create_category_folders and not os.path.exists(category_path) and not dry_run:
                os.makedirs(category_path)
                logger.info(f"Created category directory: {category}")
            
            # Destination path for the file
            dest_path = os.path.join(directory, category, filename)
            
            # Skip if source and destination are the same
            if os.path.abspath(file_path) == os.path.abspath(dest_path):
                logger.info(f"Skipping file already in the correct folder: {filename}")
                skipped_files += 1
                continue
            
            # Handle filename conflicts
            counter = 1
            original_dest_path = dest_path
            while os.path.exists(dest_path) and not dry_run:
                name, ext = os.path.splitext(original_dest_path)
                dest_path = f"{name}_{counter}{ext}"
                counter += 1
            
            # Move or copy the file
            try:
                if dry_run:
                    logger.info(f"Would move '{file_path}' to '{category}/{filename}'")
                else:
                    shutil.move(file_path, dest_path)
                    logger.info(f"Moved '{filename}' to '{category}/{os.path.basename(dest_path)}'")
                organized_files += 1
            except Exception as e:
                logger.error(f"Error moving file '{filename}': {str(e)}")
                skipped_files += 1
    
    logger.info(f"Processed {total_files} files: {organized_files} organized, {skipped_files} skipped")
    return True

def main():
    """Main entry point for the CLI tool"""
    parser = argparse.ArgumentParser(description="File Organizer - A tool to organize files by category")
    
    parser.add_argument("directory", nargs="?", default=os.getcwd(),
                       help="Directory to organize (default: current directory)")
    parser.add_argument("-n", "--dry-run", action="store_true",
                       help="Perform a dry run without moving files")
    parser.add_argument("-r", "--recursive", action="store_true",
                       help="Recursively organize files in subdirectories")
    parser.add_argument("-s", "--stats", action="store_true",
                       help="Show statistics after organizing")
    
    args = parser.parse_args()
    
    logger = setup_logger()
    logger.info(f"Starting file organization in: {args.directory}")
    logger.info(f"Options: dry_run={args.dry_run}, recursive={args.recursive}")
    
    if args.dry_run:
        logger.info("DRY RUN MODE: No files will be moved")
    
    start_time = datetime.now()
    success = organize_files(args.directory, dry_run=args.dry_run, recursive=args.recursive)
    end_time = datetime.now()
    
    if success:
        duration = (end_time - start_time).total_seconds()
        logger.info(f"Organization completed in {duration:.2f} seconds")
        
        if args.stats and not args.dry_run:
            # Get directory sizes after organization
            category_sizes = {}
            for item in os.listdir(args.directory):
                item_path = os.path.join(args.directory, item)
                if os.path.isdir(item_path) and item != 'logs':
                    size = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                               for dirpath, _, filenames in os.walk(item_path) 
                               for filename in filenames)
                    category_sizes[item] = size
            
            logger.info("Category statistics:")
            for category, size in sorted(category_sizes.items()):
                if size > 1024 * 1024 * 1024:  # GB
                    size_str = f"{size / (1024 * 1024 * 1024):.2f} GB"
                elif size > 1024 * 1024:  # MB
                    size_str = f"{size / (1024 * 1024):.2f} MB"
                elif size > 1024:  # KB
                    size_str = f"{size / 1024:.2f} KB"
                else:  # bytes
                    size_str = f"{size} bytes"
                
                logger.info(f"  {category}: {size_str}")
    else:
        logger.error("Organization failed")

if __name__ == "__main__":
    main()