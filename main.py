import os
import shutil
import time
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_title_after_dash(name):
    """
    Extract text after " - " for sorting. Handle cases without " - ".
    """
    parts = name.split(' - ', 1)
    return parts[1].strip() if len(parts) > 1 else parts[0].strip()

def sort_folders_by_title_ps1(folder_path):
    """
    Sort folders by the title after " - " in descending alphabetical order.
    """
    items = [item for item in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, item))]
    items.sort(key=lambda x: extract_title_after_dash(x), reverse=True)
    return items

def sort_files_by_title_psp(folder_path):
    """
    Sort files alphabetically in descending order.
    """
    files = os.listdir(folder_path)
    files.sort(reverse=True)  # Sort in descending alphabetical order
    return files

def copy_file(source_path, destination_path):
    """
    Copy a file from source to destination.
    """
    try:
        # Perform copy operation with buffering
        with open(source_path, 'rb') as src_file:
            with open(destination_path, 'wb') as dst_file:
                shutil.copyfileobj(src_file, dst_file)
        current_time = time.time()
        os.utime(destination_path, (current_time, current_time))
        print(f"[INFO] Finished copying file: {os.path.basename(source_path)} - Complete")
    except Exception as e:
        print(f"[ERROR] Failed to copy file: {os.path.basename(source_path)} - {e}")

def copy_and_sort_folder(source_folder, destination_folder, is_ps1):
    """
    Copy and sort files or folders based on the game type.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    if is_ps1:
        # Scan the whole folder and copy in descending alphabetical order by title after " - "
        items = sort_folders_by_title_ps1(source_folder)
        
        skipped_folders = []
        new_folders = []
        
        for item_name in items:
            source_path = os.path.join(source_folder, item_name)
            destination_path = os.path.join(destination_folder, item_name)
            
            print(f"\n[INFO] Currently copying folder: {item_name}...")
            try:
                shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                new_folders.append(item_name)
                # Update the modification time
                current_time = time.time()
                for root_dir, _, files in os.walk(destination_path):
                    for file_name in files:
                        file_path = os.path.join(root_dir, file_name)
                        os.utime(file_path, (current_time, current_time))
                print(f"[INFO] Finished copying folder: {item_name} - Complete")
            except Exception as e:
                print(f"[ERROR] Failed to copy folder: {item_name} - {e}")
        
        print()  # Move to the next line
        
        # Print sorted folders in the destination folder
        print("Folders in destination folder (sorted by name after ' - '):")
        for folder_name in sort_folders_by_title_ps1(destination_folder):
            print(folder_name)
        
    else:
        # Copy files for PSP games one by one
        files = sort_files_by_title_psp(source_folder)
        
        skipped_files = []
        new_files = []
        
        for file_name in files:
            source_path = os.path.join(source_folder, file_name)
            destination_path = os.path.join(destination_folder, file_name)
            
            if os.path.isfile(source_path):
                if file_name not in os.listdir(destination_folder):
                    print(f"\n[INFO] Currently copying file: {file_name}...")
                    copy_file(source_path, destination_path)
                    new_files.append(file_name)
                    time.sleep(1)  # Simulate a slight delay, adjust as needed
                else:
                    skipped_files.append(file_name)
                    print(f"\n[INFO] Currently skipping file: {file_name} (already exists in destination)...")
                    print(f"[INFO] Finished skipping file: {file_name} - Complete")
        
        print()  # Move to the next line
        
        # Sort files in the destination folder
        destination_files = sort_files_by_title_psp(destination_folder)
        for i, file_name in enumerate(destination_files):
            destination_path = os.path.join(destination_folder, file_name)
            mod_time = time.time() + i
            os.utime(destination_path, (mod_time, mod_time))
        
        # Print sorted files in the destination folder
        print("Files in destination folder (sorted by name in descending alphabetical order):")
        for file_name in destination_files:
            print(file_name)
        
        if skipped_files:
            print("\nSkipped files (already exist):")
            for file_name in skipped_files:
                print(file_name)
        
        if new_files:
            print("\nNew files copied:")
            for file_name in new_files:
                print(file_name)
    
    print("All files have been copied and sorted successfully.")

def select_folder(prompt):
    """
    Prompt the user to select a folder.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory(title=prompt)
    root.destroy()
    return folder_path

def select_game_type():
    """
    Prompt the user to select the game type.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    game_type = messagebox.askquestion("Game Type", "Select the game type:\n\nYes for PS1\nNo for PSP")
    root.destroy()
    return game_type == 'yes'

# Example usage:
game_type = select_game_type()
source_folder = select_folder("Select the source folder")
destination_folder = select_folder("Select the destination folder")

if source_folder and destination_folder:
    copy_and_sort_folder(source_folder, destination_folder, is_ps1=game_type)
else:
    print("Source and destination folders must be selected.")
