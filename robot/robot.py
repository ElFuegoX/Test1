from abc import ABC, abstractmethod
   
class Robot(ABC):
    def __init__(self, name, position=(0, 0)):
        self._name = name
        self._battery_level = 100
        self._position = position
        self._status = "Idle"

    def charge(self):
        self._battery_level = 100
        print(f"{self._name} est maintenant complètement chargé.")

    def shutdown(self):
        self._status = "Shutdown"
        print(f"{self._name} est éteint.")

    def start(self):
        self._status = "Active"
        print(f"{self._name} est actif.")

    def display_info(self):
        print(f"Robot: {self._name}")
        print(f"Position: {self._position}")
        print(f"Battery: {self._battery_level}%")
        print(f"Status: {self._status}")

    @abstractmethod
    def move(self):
        pass
