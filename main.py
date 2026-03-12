from services.scraper import ProxmoxerScraper
from settings.connection import ConnectionManager
from db.redis_driver import redisDriver
from db.sql_driver import sqlDriver
from dotenv import load_dotenv
import os
import time

def uploadMysql(Scraper,sql):
    Scraper.getNodesHierarchy()
    Scraper.scrapeContainers()
    Scraper.scrapeNodes()
    sql.updateNodesInMySQL(Scraper.nodeData)
    sql.updateContainersInMySQL(Scraper.containerData)

def uploadRedis(Scraper,rd):
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

sql = sqlDriver()
sql.connect()

while(True):
    for i in range(int(os.getenv("CONTAINER_MYSQL_SCRAPE_INTERVAL"))):
        uploadRedis(Scraper, rd)
        time.sleep(int(os.getenv("CONTAINER_REDIS_SCRAPE_INTERVAL")))
    uploadMysql(Scraper,sql)
    
    