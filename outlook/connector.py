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

        # Try multiple approaches to find the folder
        target_folder = None

        # Approach 1: Try direct store access (works for local/default account)
        try:
            print(f"🔍 Buscando carpeta en cuenta: {account_email}")
            target_folder = self._try_store_access(folder_name, subfolder_name, inbox_name)
            if target_folder:
                return target_folder
        except Exception as e:
            print(f"   Método 1 falló: {e}")

        # Approach 2: Try shared folder access (works for shared/secondary accounts)
        try:
            target_folder = self._try_shared_access(account_email, folder_name, subfolder_name, inbox_name)
            if target_folder:
                return target_folder
        except Exception as e:
            print(f"   Método 2 falló: {e}")

        # Approach 3: Search all stores
        try:
            target_folder = self._try_search_all_stores(folder_name, subfolder_name)
            if target_folder:
                return target_folder
        except Exception as e:
            print(f"   Método 3 falló: {e}")

        # If all approaches failed, provide helpful error message
        raise Exception(
            f"❌ No se pudo encontrar la carpeta '{folder_name}'.\n\n"
            f"Sugerencias:\n"
            f"1. Ejecuta 'python show_outlook_folders.py' para ver tus carpetas\n"
            f"2. Verifica que la carpeta '{folder_name}' existe en Outlook\n"
            f"3. Verifica que el nombre esté escrito correctamente (mayúsculas/minúsculas)\n"
            f"4. Asegúrate de que Outlook esté completamente cargado\n"
        )

    def _try_store_access(self, folder_name: str, subfolder_name: str, inbox_name: str):
        """Try to access folder through default store."""
        stores = self.namespace.Stores
        for store in stores:
            try:
                root_folder = store.GetRootFolder()

                # Try to find the folder directly under root
                try:
                    target = root_folder.Folders[folder_name]
                    print(f"✅ Carpeta encontrada: {folder_name}")
                    if subfolder_name:
                        target = target.Folders[subfolder_name]
                        print(f"✅ Subcarpeta encontrada: {subfolder_name}")
                    print(f"📧 Items encontrados: {target.Items.Count}")
                    return target
                except Exception:
                    pass

                # Try under Inbox
                try:
                    inbox = root_folder.Folders[inbox_name]
                    target = inbox.Folders[folder_name]
                    print(f"✅ Carpeta encontrada en {inbox_name}: {folder_name}")
                    if subfolder_name:
                        target = target.Folders[subfolder_name]
                        print(f"✅ Subcarpeta encontrada: {subfolder_name}")
                    print(f"📧 Items encontrados: {target.Items.Count}")
                    return target
                except Exception:
                    pass

            except Exception:
                continue
        return None

    def _try_shared_access(self, account_email: str, folder_name: str,
                          subfolder_name: str, inbox_name: str):
        """Try to access folder through shared folder access."""
        try:
            recipient = self.namespace.CreateRecipient(account_email)
            recipient.Resolve()

            if not recipient.Resolved:
                return None

            # Try to get inbox
            inbox = self.namespace.GetSharedDefaultFolder(recipient, 6)  # 6 = Inbox

            # Try folder under inbox
            try:
                target = inbox.Folders[folder_name]
                print(f"✅ Carpeta encontrada (método compartido): {folder_name}")
                if subfolder_name:
                    target = target.Folders[subfolder_name]
                    print(f"✅ Subcarpeta encontrada: {subfolder_name}")
                print(f"📧 Items encontrados: {target.Items.Count}")
                return target
            except Exception:
                pass

            # Try under parent
            try:
                parent = inbox.Parent
                target = parent.Folders[folder_name]
                print(f"✅ Carpeta encontrada (raíz): {folder_name}")
                if subfolder_name:
                    target = target.Folders[subfolder_name]
                    print(f"✅ Subcarpeta encontrada: {subfolder_name}")
                print(f"📧 Items encontrados: {target.Items.Count}")
                return target
            except Exception:
                pass

        except Exception:
            pass

        return None

    def _try_search_all_stores(self, folder_name: str, subfolder_name: str):
        """Search for folder in all stores recursively."""
        stores = self.namespace.Stores
        for store in stores:
            try:
                root_folder = store.GetRootFolder()
                result = self._search_folder_recursive(root_folder, folder_name, subfolder_name)
                if result:
                    print(f"✅ Carpeta encontrada en: {store.DisplayName}")
                    print(f"📧 Items encontrados: {result.Items.Count}")
                    return result
            except Exception:
                continue
        return None

    def _search_folder_recursive(self, parent_folder, folder_name: str,
                                 subfolder_name: str, depth: int = 0):
        """Recursively search for folder."""
        if depth > 5:  # Limit recursion depth
            return None

        try:
            folders = parent_folder.Folders
            for folder in folders:
                try:
                    if folder.Name == folder_name:
                        if subfolder_name:
                            try:
                                return folder.Folders[subfolder_name]
                            except Exception:
                                pass
                        else:
                            return folder

                    # Search in subfolders
                    result = self._search_folder_recursive(folder, folder_name,
                                                          subfolder_name, depth + 1)
                    if result:
                        return result
                except Exception:
                    continue
        except Exception:
            pass

        return None
