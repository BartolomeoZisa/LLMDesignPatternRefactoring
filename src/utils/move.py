import os
import shutil

## This script moves files and directories with a specific name from a source directory to a destination directory.


def move_named_items(src_root, dest_root, target_name):
    for root, dirs, files in os.walk(src_root, topdown=False):
        # Check for matching directories
        for d in dirs:
            if d == target_name:
                full_dir_path = os.path.join(root, d)
                parent_name = os.path.basename(root)
                dest_dir_path = os.path.join(dest_root, parent_name)
                os.makedirs(dest_dir_path, exist_ok=True)
                target_dest_path = os.path.join(dest_dir_path, d)
                print(f"Moving directory: {full_dir_path} -> {target_dest_path}")
                shutil.move(full_dir_path, target_dest_path)

        # Check for matching files
        for f in files:
            if f == target_name:
                full_file_path = os.path.join(root, f)
                parent_name = os.path.basename(root)
                dest_dir_path = os.path.join(dest_root, parent_name)
                os.makedirs(dest_dir_path, exist_ok=True)
                target_dest_path = os.path.join(dest_dir_path, f)
                print(f"Moving file: {full_file_path} -> {target_dest_path}")
                shutil.move(full_file_path, target_dest_path)

# ==== USAGE ====
source_directory = "../../data/examples"
destination_directory = "../../old/old_results"
name_to_find = "llm2"  # File or folder name

move_named_items(source_directory, destination_directory, name_to_find)


