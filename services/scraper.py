class ProxmoxerScraper():
    def __init__(self,conn):
        self.conn = conn

    def getNodesHierarchy(self):
        """
        Maps LXC containers to their respective physical nodes.
        Creates an object called 'nodes' that contains a dictionary with node names as keys and lists of VMIDs as values.
        """
        data = self.conn(f'/cluster/resources').get()
        self.nodes = {}
        for res in data:
            if res["node"] not in self.nodes:
                self.nodes[res["node"]] = []

            if res['type'] == 'lxc':
                self.nodes[res["node"]].append(res["vmid"])

    def scrapeContainers(self):
        """
        Scrape data from the '/nodes/{node}/lxc/{vmid}/status/current' endpoint, cleans and format it.
        Create an object called 'containerData' that contains a dictionary with vmids as keys and an dictionary with scraped data as values.
        """
        self.containerData = {}
        for node, vmids in self.nodes.items():
            for vmid in vmids:
                data = self.conn(f'/nodes/{node}/lxc/{vmid}/status/current').get()
                cleaned_data = self.formatContainerData(data)
                self.containerData[vmid] = cleaned_data

    def formatContainerData(self, data):
        """
        Format data from '/nodes/{node}/lxc/{vmid}/status/current' incoming API
        """
        gb_factor = 1024**3
        cleaned_data = {
            'name': data['name'],
            'status': data['status'],
            'cpu_usage': round(data['cpu'] * 100,2),
            'cpu_max': data['cpus'],
            'mem_usage': round(data['mem'] / gb_factor,2),
            'mem_max': round(data['maxmem'] / gb_factor,2),
            'swap_usage': round(data['mem'] / gb_factor,2),
            'swap_max': round(data['maxmem'] / gb_factor,2),
            'storage_used': round(data['disk'] / gb_factor,2),
            'storage_max': round(data['maxdisk'] / gb_factor,2),
            'some_cpu_pressure': data.get('pressurecpusome',None), # Percentage of time in the last 10 sec where tasks waited for CPU
            'some_mem_pressure': data.get('pressurememorysome',None), # Percentage of time in the last 10 sec where tasks waited for RAM
            'some_io_pressure': data.get('pressureiosome',None), # Percentage of time in the last 10 sec where tasks waited for storage
            'uptime': data['uptime']
        }

        return cleaned_data

    def scrapeNodes(self):
        """
        Scrape data from the '/nodes/PVE-01/status' endpoint, cleans and format it.
        Create an object called 'nodeData' that contains a dictionary with node names as keys and an dictionary with scraped data as values.
        """
        self.nodeData = {}
        for node in self.nodes:
            data = self.conn(f'/nodes/{node}/status').get()
            cleaned_data = self.formatNodeData(data)
            self.nodeData[node] = cleaned_data

    def formatNodeData(self, data):
        """
        Format data from '/nodes/{node}/status' incoming API
        """
        gb_factor = 1024**3
        cleaned_data = {
            'cpu_model' : data['cpuinfo']['model'],
            'cpu_frequency' : round(float(data['cpuinfo']['mhz']) / 1000,2),
            'cpu_cores': data['cpuinfo']['cores'],
            'cpu_usage': round(data['cpu'] * 100,2),
            'cpu_max' : data['cpuinfo']['cpus'],
            'last_minute_cpu_load' : data['loadavg'][0], #Average of the CPUs used in the last minute (anything below the cpu_max is ok)
            'mem_usage': round(data['memory']['used'] / gb_factor,2),
            'mem_max': round(data['memory']['total'] / gb_factor,2),
            'swap_usage': round(data['swap']['used'] / gb_factor,2), #If above 0, the server is beeing slowed down by RAM
            'root_storage': round(data['rootfs']['avail'] / gb_factor,2), #Storage available in boot drive, if full, server will crash
            'uptime': data['uptime'],
            'storage_wait': round(data['wait'] * 100,2) #Percentage of time system's been waiting for the SSD/HD
        }
        
        return cleaned_data