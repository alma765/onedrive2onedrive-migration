# OneDrive Transfer Tool

This tool helps you transfer files between two OneDrive accounts using rclone.

## Prerequisites

1. Install rclone from https://rclone.org/downloads/
2. Make sure rclone is added to your system PATH
3. Python 3.6 or higher

## How to Use

1. Run the script:
   ```
   python onedrive_transfer.py
   ```

2. The script will guide you through:
   - Configuring your source OneDrive account
   - Configuring your destination OneDrive account
   - Selecting source and destination folders
   - Confirming and executing the transfer

## Authentication Process

When you run the script for the first time, it will:
1. Open your web browser for authentication
2. Ask you to log in to your Microsoft account
3. Request permission to access your OneDrive
4. Guide you through the same process for both source and destination accounts

## Notes

- The transfer process will show progress in real-time
- Files are copied (not moved) by default to ensure data safety
- The script will create the destination folder if it doesn't exist
- You can cancel the transfer at any time before it starts

## Troubleshooting

If you encounter any issues:
1. Make sure rclone is properly installed and in your PATH
2. Check your internet connection
3. Ensure you have proper permissions on both OneDrive accounts
4. Verify that you have enough storage space in the destination account 