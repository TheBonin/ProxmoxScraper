from services.scraper import ProxmoxerScraper
from settings.connection import ConnectionManager
from db.redis_driver import redisDriver
from dotenv import load_dotenv
import os
import time

def main(Scraper,rd):
    Scraper.getNodesHierarchy()
    Scraper.scrapeContainers()
    Scraper.scrapeNodes()
    rd.storeStatusByContainer(Scraper.containerData)
    rd.storeStatusByNode(Scraper.nodeData)

load_dotenv()

cm = ConnectionManager()
conn = cm.connect()

Scraper = ProxmoxerScraper(conn)
Scraper.scrapeNodes

rd = redisDriver()
rd.connect()

while(True):
    main(Scraper, rd)
    time.sleep(int(os.getenv("CONTAINER_SCRAPE_INTERVAL")))
    