from .robot import Robot

class DeliveryRobot(Robot):
    def __init__(self, name, position=(0, 0), destination=(5, 5)):
        super().__init__(name, position)
        self.payload = None
        self.destination = destination

    def move(self):
        if self._battery_level < 15:
            print(f"{self._name} n’a pas assez de batterie pour livrer.")
            return
        print(f"{self._name} se dirige vers {self.destination}.")
        self._position = self.destination
        self._battery_level -= 15

    def load(self, item):
        self.payload = item
        print(f"{self._name} a chargé : {item}")

    def unload(self):
        print(f"{self._name} a livré : {self.payload}")
        self.payload = None
