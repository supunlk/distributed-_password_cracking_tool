import requests


class ServiceDiscovery:
    def __init__(self, endpoint='http://127.0.0.1:8500/v1/agent'):
        self.endpoint = endpoint
        self.url_register = '{}/{}'.format(self.endpoint, 'service/register')
        self.url_deregister = '{}/{}'.format(self.endpoint, 'service/deregister')
        self.url_services = '{}/{}'.format(self.endpoint, 'services')
        self.url_service = '{}/{}'.format(self.endpoint, 'service')

        self.service = {}

    def register(self, service_id, name, address, port=None):
        self.service = {'ID': service_id, 'Name': name, 'Address': address}
        if port:
            self.service['Port'] = int(port)
        r = requests.put(self.url_register, json=self.service)
        if r.status_code != 200:
            print(r.content)
            raise Exception('error')
        return self.service

    def deregister(self, service_id):
        r = requests.delete('{}/{}'.format(self.url_deregister, service_id))
        if r.status_code != 200:
            raise Exception('error')
        return r

    def list(self):
        """List all services that have been registered"""
        r = requests.get(self.url_services)
        services = r.json()
        services_array = list(services.values())
        return services_array
