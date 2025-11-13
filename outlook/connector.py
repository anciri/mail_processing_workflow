"""
Outlook connector - handles connection to Outlook and folder navigation.
"""
import win32com.client


class OutlookConnector:
    """Handles connection to Microsoft Outlook."""

    def __init__(self):
        self.outlook = None
        self.namespace = None

    def connect(self):
        """
        Connect to Outlook application.

        Raises:
            Exception if Outlook cannot be accessed
        """
        try:
            self.outlook = win32com.client.Dispatch("Outlook.Application")
            self.namespace = self.outlook.GetNamespace("MAPI")
            print("✅ Conectado a Outlook exitosamente")
        except Exception as e:
            raise Exception(
                f"No se pudo conectar a Outlook. "
                f"Asegúrate de que Outlook esté abierto y funcionando.\n"
                f"Error: {e}"
            )

    def get_folder(self, account_email: str, inbox_name: str,
                   folder_name: str, subfolder_name: str = ""):
        """
        Navigate to a specific folder in Outlook.

        Args:
            account_email: Email account to access
            inbox_name: Name of inbox folder (usually "Inbox")
            folder_name: Target folder name
            subfolder_name: Optional subfolder name

        Returns:
            Outlook folder object

        Raises:
            Exception if folder cannot be found
        """
        if not self.namespace:
            raise Exception("Not connected to Outlook. Call connect() first.")

        try:
            # Get the account
            recipient = self.namespace.CreateRecipient(account_email)
            recipient.Resolve()

            if not recipient.Resolved:
                raise Exception(f"No se pudo encontrar la cuenta: {account_email}")

            # Get folders
            folders = self.namespace.GetSharedDefaultFolder(recipient, 6)  # 6 = Inbox

            # Navigate to inbox
            inbox = folders.Parent.Folders[inbox_name]
            print(f"📂 Accediendo a carpeta: {inbox_name}")

            # Navigate to target folder
            target_folder = inbox.Folders[folder_name]
            print(f"📂 Accediendo a carpeta: {folder_name}")

            # Navigate to subfolder if specified
            if subfolder_name:
                target_folder = target_folder.Folders[subfolder_name]
                print(f"📂 Accediendo a subcarpeta: {subfolder_name}")

            item_count = target_folder.Items.Count
            print(f"📧 Encontrados {item_count} items en la carpeta")

            return target_folder

        except Exception as e:
            raise Exception(
                f"Error al acceder a la carpeta.\n"
                f"Verifica que la cuenta '{account_email}' y "
                f"la carpeta '{folder_name}' existan.\n"
                f"Error: {e}"
            )
