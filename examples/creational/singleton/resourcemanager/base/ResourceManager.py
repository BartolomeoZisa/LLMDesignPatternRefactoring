import threading

class ResourceManager:
    def __init__(self, initial_resources={}):
        self.resources = initial_resources.copy()
        self.lock = threading.Lock()

    def request_resource(self, resource_type, amount, requester):
        with self.lock:
            if self.resources.get(resource_type, 0) >= amount:
                self.resources[resource_type] -= amount
                print(f"{requester} received {amount} of {resource_type} (Remaining: {self.resources.get(resource_type, 0)})")
                return True
            else:
                print(f"{requester} failed to get {amount} of {resource_type} (Available: {self.resources.get(resource_type, 0)})")
                return False


class Factory(threading.Thread):
    def __init__(self, name, resource_manager, build_sequence):
        super().__init__(name=name)
        self.resource_manager = resource_manager
        self.build_sequence = build_sequence

    def run(self):
        for resource_type, amount_needed in self.build_sequence:
            self.resource_manager.request_resource(resource_type, amount_needed, self.name)
        print(f"{self.name} finished building.")
