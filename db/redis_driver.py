import redis
import json
import os

class redisDriver():
    _instance = None
    _initialized = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        if self._initialized is None:
            self._initialized = True
            self.host = os.getenv("REDIS_HOST")
            self.port = int(os.getenv("REDIS_PORT", 6379))
            self.password = os.getenv("REDIS_PASSWORD")
            self.cnx = None
    
    def connect(self) -> None:
        """
        Connects to the redis database and create an connection object.
        """
        self.r = redis.Redis(host=self.host,
                             port=self.port,
                             password=self.password,
                             decode_responses=True)
    
    def storeStatusByContainer(self, data: dict) -> None:
        """
        Recieves a dictionary where keys are the vmid and it's contents are the containerses status.
        Store scraped and formatted containers data on Redis using 'ct:{vmid}:status' as tag.
        """
        for vmid, status in data.items():
            try:
                json_status = json.dumps(status)
                self.r.set(name= f'ct:{vmid}:status',
                    value= json_status,
                    ex= os.getenv("REDIS_EXPIRE_IN_SECONDS"))
            except redis.exceptions.ConnectionError:
                print(f"CRITICAL: Could not reach Redis to save VM {vmid}")
        print("VMs uploaded to Redis!")

    def storeStatusByNode(self, data: dict) -> None:
        """
        Recieves a dictionary where keys are the nodes names and it's contents are the nodeses status.
        Store scraped and formatted nodes data on Redis using 'ct:{node_name}:status' as tag.
        """
        for node_name, status in data.items():
            try:
                json_status = json.dumps(status)
                self.r.set(name= f'node:{node_name}:status',
                    value= json_status,
                    ex= os.getenv("REDIS_EXPIRE_IN_SECONDS"))
            except redis.exceptions.ConnectionError:
                print(f"CRITICAL: Could not reach Redis to save node {node_name}")
        print("Nodes uploaded to Redis!")
    
    def close(self):
        self.r.close()
        self._instance = None
        self._initialized = None
