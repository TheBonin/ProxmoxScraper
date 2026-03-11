from proxmoxer import ProxmoxAPI
import os

class ConnectionManager():
    def __init__(self):
        self.conn = None
        self.host = os.getenv("PVE_HOST")
        self.user = os.getenv("PVE_USER")
        self.tokenName = os.getenv("PVE_TOKEN_NAME")
        self.tokenValue = os.getenv("PVE_TOKEN_VALUE")

    def connect(self):
        #Connects to the PROXMOX cluster
        if self.conn is None:
            self.conn = ProxmoxAPI(host = self.host,
                                   user = self.user,
                                   token_name = self.tokenName,
                                   token_value = self.tokenValue,
                                   verify_ssl = False)
        return self.conn