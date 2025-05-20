import os
import shutil
import sys

ROOTDIR = "../../data/"
FOLDERTODELETE = sys.argv[1] if len(sys.argv) > 1 else "llm2"  # Default to "llm2" if no argument is provided

def delete_folder_by_name(root_path, folder_name_to_delete):
    """
    Traverse through the root_path and delete all folders with the given name.

    Args:
        root_path (str): The root directory to start traversal.
        folder_name_to_delete (str): The name of the folders to delete.

    Returns:
        list: A list of paths that were deleted.
    """
    deleted_paths = []

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        for dirname in dirnames:
            if dirname == folder_name_to_delete:
                full_path = os.path.join(dirpath, dirname)
                try:
                    shutil.rmtree(full_path)
                    deleted_paths.append(full_path)
                    print(f"Deleted: {full_path}")
                except Exception as e:
                    print(f"Failed to delete {full_path}: {e}")

    return deleted_paths

if __name__ == "__main__":
    #ask if you're sure you want to delete the folder
    confirm = input(f"Are you sure you want to delete all folders named '{FOLDERTODELETE}' in '{ROOTDIR}'? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        exit(0)

    # Delete the specified folder
    deleted_folders = delete_folder_by_name(ROOTDIR, FOLDERTODELETE)
    print(f"Deleted folders: {deleted_folders}")
