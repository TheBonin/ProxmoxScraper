import redis
import json
import os

class redisDriver():
    def __init__(self):
        self.r = None
    
    def connect(self):
        # Connects to and return an Redis instance
        if self.r is None:
            self.r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"),
                password=os.getenv("REDIS_PASSWORD"),
                decode_responses=True)
        return self.r
    
    def storeStatusByContainer(self, data: dict) -> None:
        # Recieve a dictionary where key is the container/VM/node id and it's content is the container/VM/node's status.
        # Store scraped and formatted container/VM/node data on Redis using 'ct:{id}:status' as tag.
        for id in data:
            if data[id]['type'] == 'node':
                json_data = json.dumps(data[id])
                self.r.set(name= f'node:{id}:status',
                    value= json_data,
                    ex= os.getenv("REDIS_EXPIRE_IN_SECONDS"))
                print(f'{id}: status salvo no Redis!')
            else:
                json_data = json.dumps(data[id])
                self.r.set(name= f'ct:{id}:status',
                    value= json_data,
                    ex= os.getenv("REDIS_EXPIRE_IN_SECONDS"))
                print(f'{id}: status salvo no Redis!')

    def storeClusterStatus(self,data,clusterId: dict) -> None:
        # Recieve a dictionary where it's content is the Node status.
        # Store scraped and formatted cluster data on Redis using 'ct:{clusterId}:status' as tag.
        json_data = json.dumps(data)
        self.r.set(name= f'ct:{clusterId}:status',
              value= json_data,
              ex= os.getenv("REDIS_EXPIRE_IN_SECONDS"))
        print(f'ct:{clusterId}:status salvo no Redis!')