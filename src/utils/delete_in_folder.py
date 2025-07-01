import os
import shutil
import sys

ROOTDIR = "../../data/results"
TARGET_NAME = sys.argv[1] if len(sys.argv) > 1 else "llm"  # Default to "llm" if no argument is provided

def delete_items_by_name(root_path, target_name):
    """
    Traverse through the root_path and delete all folders and files with the given name.

    Args:
        root_path (str): The root directory to start traversal.
        target_name (str): The name of the folders or files to delete.

    Returns:
        list: A list of paths that were deleted.
    """
    deleted_paths = []

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        # Delete directories
        for dirname in dirnames:
            if dirname == target_name:
                full_path = os.path.join(dirpath, dirname)
                try:
                    shutil.rmtree(full_path)
                    deleted_paths.append(full_path)
                    print(f"Deleted folder: {full_path}")
                except Exception as e:
                    print(f"Failed to delete folder {full_path}: {e}")

        # Delete files
        for filename in filenames:
            if filename == target_name:
                full_path = os.path.join(dirpath, filename)
                try:
                    os.remove(full_path)
                    deleted_paths.append(full_path)
                    print(f"Deleted file: {full_path}")
                except Exception as e:
                    print(f"Failed to delete file {full_path}: {e}")

    return deleted_paths

if __name__ == "__main__":
    confirm = input(f"Are you sure you want to delete all folders and files named '{TARGET_NAME}' in '{ROOTDIR}'? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        exit(0)

    deleted_items = delete_items_by_name(ROOTDIR, TARGET_NAME)
    print(f"Deleted items: {deleted_items}")

