import threading
from threading import Lock


#volatile is not needed in Python, everything is in main memory
class SingletonMeta(type):
    """
    Thread-safe Singleton using Double-Checked Locking.
    """
    _instances = {}
    _lock: Lock = Lock()  # Lock for synchronizing threads

    def __call__(cls, *args, **kwargs):
        # First check (without locking) to improve performance
        if cls not in cls._instances:
            with cls._lock:  # Second check (with locking) to ensure only one instance is created
                if cls not in cls._instances:  
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
class ResourceManager(metaclass=SingletonMeta):
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