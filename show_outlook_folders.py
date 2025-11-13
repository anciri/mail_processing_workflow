"""
Outlook Folder Explorer
Shows your Outlook folder structure to help configure the workflow correctly.
"""
import win32com.client
import sys


def explore_outlook_folders():
    """Explore and display Outlook folder structure."""
    print("=" * 70)
    print("OUTLOOK FOLDER EXPLORER")
    print("=" * 70)
    print()

    try:
        # Connect to Outlook
        print("Connecting to Outlook...")
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        print("✅ Connected to Outlook successfully!\n")

        # Get all accounts
        print("=" * 70)
        print("YOUR OUTLOOK ACCOUNTS:")
        print("=" * 70)

        stores = namespace.Stores
        for i, store in enumerate(stores, 1):
            print(f"\n{i}. {store.DisplayName}")
            try:
                # Try to get email address if available
                if hasattr(store, 'GetRootFolder'):
                    root = store.GetRootFolder()
                    print(f"   Root folder: {root.Name}")
            except Exception:
                pass

        print("\n" + "=" * 70)
        print("FOLDER STRUCTURE FOR EACH ACCOUNT:")
        print("=" * 70)

        # Explore each store's folders
        for store in stores:
            print(f"\n📧 Account: {store.DisplayName}")
            print("-" * 70)

            try:
                root_folder = store.GetRootFolder()
                explore_folder(root_folder, indent=0)
            except Exception as e:
                print(f"   ❌ Could not access folders: {e}")

        print("\n" + "=" * 70)
        print("CONFIGURATION HELP:")
        print("=" * 70)
        print("\nTo configure your workflow:")
        print("1. Find your account name from the list above")
        print("2. Find the folder where your emails are stored")
        print("3. Note the complete folder path")
        print("\nIn config.py, set:")
        print("   TARGET_ACCOUNT_EMAIL = 'your-email@domain.com'")
        print("   TARGET_FOLDER_NAME = 'YourFolderName'")
        print("   TARGET_SUBFOLDER_NAME = 'SubfolderName' (if needed, else leave empty)")
        print()

    except Exception as e:
        print(f"❌ Error connecting to Outlook: {e}")
        print("\nMake sure:")
        print("1. Outlook is open")
        print("2. You have permission to access it")
        print("3. Outlook is properly configured")
        return 1

    return 0


def explore_folder(folder, indent=0):
    """
    Recursively explore folder structure.

    Args:
        folder: Outlook folder object
        indent: Indentation level for display
    """
    prefix = "  " * indent

    try:
        # Get folder info
        folder_name = folder.Name
        try:
            item_count = folder.Items.Count
            folder_info = f"{folder_name} ({item_count} items)"
        except Exception:
            folder_info = f"{folder_name}"

        # Print folder
        if indent == 0:
            print(f"{prefix}📁 {folder_info}")
        else:
            print(f"{prefix}└─ 📂 {folder_info}")

        # Explore subfolders (limit depth to avoid too much output)
        if indent < 3:
            try:
                subfolders = folder.Folders
                for subfolder in subfolders:
                    try:
                        explore_folder(subfolder, indent + 1)
                    except Exception:
                        pass
            except Exception:
                pass

    except Exception as e:
        print(f"{prefix}❌ Error reading folder: {e}")


if __name__ == "__main__":
    sys.exit(explore_outlook_folders())
