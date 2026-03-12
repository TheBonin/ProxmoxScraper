import mysql.connector
import os

class sqlDriver():
    _instance = None
    _initialized = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        if self._initialized is None:
            self.host = os.getenv("MYSQL_HOST")
            self.port = int(os.getenv("MYSQL_PORT", 3306))
            self.user = os.getenv("MYSQL_USER")
            self.password = os.getenv("MYSQL_PASSWORD")
            self.database = os.getenv("MYSQL_DATABASE")
            self._initialized = True
            self.cnx = None

    def connect(self) -> None:
        # Connects to and return an MySQL instance
        try:
            if self.cnx is None:
                self.cnx = mysql.connector.connect(host=self.host,
                                                   port=self.port,
                                                   user=self.user,
                                                   password=self.password,
                                                   database=self.database)
        except Exception as e:
            print(f"Não foi possível conectar ao banco MySQL: {e}")
            raise
        
        self.cursor = self.cnx.cursor()

    def updateNodesInMySQL(self, data: dict) -> None:
        """
        Runs through the nodes in the MySQL database and updates it if needed based on the received data from the scraper
        """
        query = "SELECT node_name FROM nodes"
        self.cursor.execute(query)
        db_result = self.cursor.fetchall()
        nodes_in_database = [row[0] for row in db_result]

        for node_name, node_metrics in data.items():
            if node_name in nodes_in_database:
                query = "UPDATE nodes " \
                        "SET node_cpu_model = %s, node_cpu_max = %s, node_cpu_cores = %s, node_mem_max = %s, node_swap_max = %s " \
                        "WHERE node_name = %s"
                values = [node_metrics['cpu_model'], node_metrics['cpu_max'], node_metrics['cpu_cores'], node_metrics['mem_max'], node_metrics['swap_max'], node_name]
            else:
                query = "INSERT INTO nodes " \
                        "(node_name, node_cpu_model, node_cpu_max, node_cpu_cores, node_mem_max, node_swap_max) " \
                        "VALUES (%s,%s,%s,%s,%s,%s)"
                values = [node_name, node_metrics['cpu_model'], node_metrics['cpu_max'], node_metrics['cpu_cores'], node_metrics['mem_max'], node_metrics['swap_max']]
            self.cursor.execute(query,values)
        self.cnx.commit()
        print("Nodes uplodaded to MySQL!")

    def updateContainersInMySQL(self, data: dict) -> None:
        """
        Runs the containers in the MySQL database and updates it if needed based on the recieved data from the scraper
        """
        query = "SELECT vm_code FROM virtual_machines"
        self.cursor.execute(query)
        db_result = self.cursor.fetchall()
        vms_in_database = [row[0] for row in db_result]

        for vm_code, vm_metrics in data.items():
            if vm_code in vms_in_database:
                query = "UPDATE virtual_machines " \
                        "SET node_name = %s, vm_name = %s, vm_cpu_max = %s, vm_mem_max = %s, vm_swap_max = %s, vm_storage_max = %s " \
                        "WHERE vm_code = %s"
                values = [vm_metrics['node'], vm_metrics['name'], vm_metrics['cpu_max'], vm_metrics['mem_max'], vm_metrics['swap_max'], vm_metrics['storage_max'], vm_code]
            else:
                query = "INSERT INTO virtual_machines " \
                        "(node_name, vm_code, vm_name, vm_cpu_max, vm_mem_max, vm_swap_max, vm_storage_max) " \
                        "VALUES (%s,%s,%s,%s,%s,%s,%s)"
                values = [vm_metrics['node'], vm_code, vm_metrics['name'], vm_metrics['cpu_max'], vm_metrics['mem_max'], vm_metrics['swap_max'], vm_metrics['storage_max']]
            self.cursor.execute(query,values)
        self.cnx.commit()
        print("Containers uplodaded to MySQL!")

    def closeConnection(self):
        if self.cnx:
            self.cnx.close()
        sqlDriver._instance = None
        sqlDriver._initialized = None