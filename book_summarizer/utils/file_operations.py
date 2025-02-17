import os
import shutil
from typing import Optional

def copy_and_rename_file(source_path: str, destination_dir: str, new_name: str) -> Optional[str]:
    """
    Copy a file to a destination directory and rename it.
    If a file with the new name already exists, ask the user if they want to delete it.

    Args:
        source_path: The path to the source file
        destination_dir: The directory where the file should be copied
        new_name: The new name for the file in the destination directory

    Returns:
        str: The path to the renamed file in the destination directory
    """
    # Create destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)
    
    # Copy the file to the destination directory
    shutil.copy(source_path, destination_dir)

    # Extract the file extension
    file_extension = os.path.splitext(source_path)[1]

    # Define the destination file path
    destination_file = os.path.join(destination_dir, f"{new_name}{file_extension}")

    # Check if the destination file already exists
    if os.path.exists(destination_file):
        user_input = input(
            f"File {destination_file} already exists. Do you want to delete it and proceed? (yes/no): "
        ).strip().lower()
        if user_input == 'yes':
            os.remove(destination_file)
            print(f"Deleted existing file: {destination_file}")
        else:
            print("Operation cancelled by the user.")
            return None

    # Rename the copied file
    os.rename(
        os.path.join(destination_dir, os.path.basename(source_path)), 
        destination_file
    )
    print(f"File renamed to: {destination_file}")

    return destination_file 