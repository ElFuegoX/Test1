from .robot import Robot

class ExplorerRobot(Robot):
    def __init__(self, name, position=(0, 0), sensor_range=5):
        super().__init__(name, position)
        self.sensor_range = sensor_range

    def move(self):
        if self._battery_level < 10:
            print(f"{self._name} n’a pas assez de batterie pour bouger.")
            return
        new_x = self._position[0] + 1
        new_y = self._position[1] + 1
        self._position = (new_x, new_y)
        self._battery_level -= 10
        print(f"{self._name} explore vers ({new_x}, {new_y}).")

    def scan_area(self):
        print(f"{self._name} scanne une zone de {self.sensor_range} mètres.")
