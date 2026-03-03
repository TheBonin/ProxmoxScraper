from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv
import os

class ConnectionManager():
    def __init__(self):
        load_dotenv()
        self.conn = None

    def connect(self):
        if self.conn == None:
            self.conn = ProxmoxAPI(os.getenv("PVE_HOST"),
                        user = os.getenv("PVE_USER"),
                        token_name = os.getenv("PVE_TOKEN_NAME"),
                        token_value = os.getenv("PVE_TOKEN_VALUE"),
                        verify_ssl = False)
        return self.conn