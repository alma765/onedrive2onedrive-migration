import subprocess
import os
import json
import sys
from pathlib import Path

def run_rclone_command(command):
    """Run rclone command and return output"""
    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running rclone command: {e}")
        print(f"Error output: {e.stderr}")
        return None

def configure_rclone():
    """Configure rclone for both source and destination OneDrive accounts"""
    print("Let's configure rclone for your OneDrive accounts.")
    
    # Configure source OneDrive
    print("\n=== Configuring Source OneDrive Account ===")
    source_name = input("Enter a name for your source OneDrive (e.g., 'source'): ")
    print("\nA browser window will open. Please follow these steps:")
    print("1. Log in to your Microsoft account")
    print("2. Grant the requested permissions")
    print("3. Copy the authentication code back to this window")
    run_rclone_command(["rclone", "config", "create", source_name, "onedrive"])
    
    # Configure destination OneDrive
    print("\n=== Configuring Destination OneDrive Account ===")
    dest_name = input("Enter a name for your destination OneDrive (e.g., 'dest'): ")
    print("\nA browser window will open. Please follow these steps:")
    print("1. Log in to your Microsoft account")
    print("2. Grant the requested permissions")
    print("3. Copy the authentication code back to this window")
    run_rclone_command(["rclone", "config", "create", dest_name, "onedrive"])
    
    return source_name, dest_name

def list_folders(remote_name):
    """List folders in the specified remote"""
    print(f"\nListing folders in {remote_name}:")
    output = run_rclone_command(["rclone", "lsf", f"{remote_name}:"])
    
    if not output:
        print("No folders found or error occurred. Please check your authentication.")
        return []
    
    folders = [line for line in output.split('\n') if line.strip()]
    
    if not folders:
        print("No folders found in the remote.")
        return []
    
    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder}")
    
    return folders

def select_folder(remote_name):
    """Let user select a folder from the remote"""
    while True:
        folders = list_folders(remote_name)
        if not folders:
            retry = input("\nWould you like to try again? (yes/no): ")
            if retry.lower() != 'yes':
                sys.exit(1)
            continue
            
        try:
            choice = int(input("\nEnter the number of the folder you want to select: "))
            if 1 <= choice <= len(folders):
                return folders[choice - 1]
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def transfer_files(source_remote, source_folder, dest_remote, dest_folder, operation_type):
    """Transfer files from source to destination using specified operation type"""
    print(f"\nStarting {operation_type} from {source_remote}:{source_folder} to {dest_remote}:{dest_folder}")
    
    # Create destination folder if it doesn't exist
    run_rclone_command(["rclone", "mkdir", f"{dest_remote}:{dest_folder}"])
    
    # Perform the transfer
    command = [
        "rclone",
        "copy",  # Always use copy as base command
        f"{source_remote}:{source_folder}",
        f"{dest_remote}:{dest_folder}",
        "--progress"
    ]
    
    # Add operation-specific options
    if operation_type == "sync":
        command[1] = "sync"  # Change to sync command
        command.extend([
            "--delete-after",  # Delete files in destination that don't exist in source
            "--delete-excluded"  # Delete excluded files from destination
        ])
    elif operation_type == "migrate":
        command.extend([
            "--ignore-existing",  # Skip files that exist in destination
            "--checksum"  # Use checksum comparison for better accuracy
        ])
    
    run_rclone_command(command)
    
    print(f"\n{operation_type.capitalize()} completed!")

def main():
    print("Welcome to the OneDrive Transfer Tool!")
    
    # Check if rclone is installed
    try:
        subprocess.run(["./rclone", "version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: rclone is not found in the current directory.")
        print("Please make sure rclone.exe is in the same directory as this script.")
        sys.exit(1)
    
    # Configure rclone if needed
    source_remote, dest_remote = configure_rclone()
    
    # Select source folder
    print("\nSelect source folder:")
    source_folder = select_folder(source_remote)
    
    # Select destination folder
    print("\nSelect destination folder:")
    dest_folder = select_folder(dest_remote)
    
    # Select operation type
    print("\nSelect operation type:")
    print("1. Copy (add all files to destination)")
    print("2. Sync (make destination match source exactly)")
    print("3. Migrate (only copy files that don't exist in destination)")
    while True:
        try:
            op_choice = int(input("\nEnter your choice (1, 2, or 3): "))
            if op_choice in [1, 2, 3]:
                operation_type = {
                    1: "copy",
                    2: "sync",
                    3: "migrate"
                }[op_choice]
                break
            print("Invalid selection. Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Confirm transfer
    print(f"\nYou are about to {operation_type} files from:")
    print(f"Source: {source_remote}:{source_folder}")
    print(f"Destination: {dest_remote}:{dest_folder}")
    
    if operation_type == "sync":
        print("\nWARNING: Sync will delete files in the destination that don't exist in the source!")
    elif operation_type == "migrate":
        print("\nMigration will only copy files that don't exist in the destination.")
        print("Existing files will be skipped.")
    
    confirm = input("\nDo you want to proceed? (yes/no): ")
    
    if confirm.lower() == 'yes':
        transfer_files(source_remote, source_folder, dest_remote, dest_folder, operation_type)
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main() 