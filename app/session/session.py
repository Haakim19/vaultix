class VaultSession:
    def __init__(self, vault, vault_key):
        self.vault = vault
        self.vault_key = vault_key

    def clear(self):
        self.vault = None
        self.vault_key = None