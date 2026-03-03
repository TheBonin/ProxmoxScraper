class ProxmoxerScraper():
    def __init__(self,conn):
        self.conn = conn

    def formatClusterData(self, data):
        # Format data from '/cluster/resources' incoming API
        cleaned_data = {}
        for res in data:
            if res['type'] in ['lxc']:
                cleaned_data[res['vmid']] = {
                    'name': res['name'],
                    'cpu_usage': round(res['cpu'] * 100,2),
                    'cpu_max': res['maxcpu'],
                    'mem_usage': round(res['mem'] / (1024**3),2),
                    'mem_max': round(res['maxmem'] / (1024**3),2),
                    'storage_used': round(res['disk'] / (1024**3),2),
                    'storage_max': round(res['maxdisk'] / (1024**3),2),
                    'uptime': res['uptime'],
                    'type' : res['type']
                }

            elif res['type'] in ['node']:
                cleaned_data[res['node']] = {
                    'cpu_usage': round(res['cpu'] * 100,2),
                    'cpu_max': res['maxcpu'],
                    'mem_usage': round(res['mem'] / (1024**3),2),
                    'mem_max': round(res['maxmem'] / (1024**3),2),
                    'storage_used': round(res['disk'] / (1024**3),2),
                    'storage_max': round(res['maxdisk'] / (1024**3),2),
                    'uptime': res['uptime'],
                    'type' : res['type']
                }
                

        return cleaned_data

    def formatContainerData(self, data):
        # Format data from '/nodes/{node}/lxc/{containerId}/status/current' incoming API
        cleaned_data = {
            data['vmid']: {
                'name': data['name'],
                'status': data['status'],
                'cpu_usage': round(data['cpu'] * 100,2),
                'cpu_max': data['cpus'],
                'mem_usage': round(data['mem'] / (1024**3),2),
                'mem_max': round(data['maxmem'] / (1024**3),2),
                'swap_usage': round(data['mem'] / (1024**3),2),
                'swap_max': round(data['maxmem'] / (1024**3),2),
                'storage_used': round(data['disk'] / (1024**3),2),
                'storage_max': round(data['maxdisk'] / (1024**3),2),
                'some_cpu_pressure': data['pressurecpusome'], # Percentage of time in the last 10 sec where tasks waited for CPU
                'some_mem_pressure': data['pressurememorysome'], # Percentage of time in the last 10 sec where tasks waited for RAM
                'some_io_pressure': data['pressureiosome'], # Percentage of time in the last 10 sec where tasks waited for storage
                'uptime': data['uptime']
            }
        }

        return cleaned_data

    def scrapeContainer(self,node,containerId):
        # Scrape data from the '/nodes/PVE-01/lxc/{containerId}/status/current' endpoint, cleans and format it
        data = self.conn(f'/nodes/{node}/lxc/{containerId}/status/current').get()
        cleaned_data = self.formatContainerData(data)
        return cleaned_data

    def scrapeCluster(self) -> dict:
        # Scrape data from the '/cluster/resources' endpoint, cleans and format it
        data = self.conn('/cluster/resources').get()
        cleaned_data = self.formatClusterData(data)
        return cleaned_data