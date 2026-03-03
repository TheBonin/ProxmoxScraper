from services.scraper import ProxmoxerScraper
from settings.connection import ConnectionManager
from db.redis_driver import redisDriver
from dotenv import load_dotenv
import os
import time


def main():
    for i in range(5):
        data = prox.scrapeCluster()
        rd.storeStatusByContainer(data)
        time.sleep(int(os.getenv("CONTAINER_SCRAPE_INTERVAL")))
    
    #Inserir futuramente o prox.scrapeContainer() atualizando uma vez para cada container. (Listar os containers no Mysql e armazernar as infos no MongoDB)


cm = ConnectionManager()
prox = ProxmoxerScraper(cm.connect())

rd = redisDriver()
rd.connect()

load_dotenv()
while(True):
    main()
    time.sleep(int(os.getenv("CONTAINER_SCRAPE_INTERVAL")))
    