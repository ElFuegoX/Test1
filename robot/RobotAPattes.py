from abc import ABC, abstractmethod
from typing import Union, Tuple
import math
from robot.robot import Robot
class RobotAPattes(Robot):
    """
    Concrete implementation of the Robot class representing a robot with legs.
    """

    def __init__(
            self,
            id: Union[int, str],
            name: str,
            position: Tuple[float, float],
            orientation: float,
            energy_source: str,
            nombre_pattes: int,
        ) -> None:
        """
        Initialize a RobotAPattes instance.

        Args:
            id (Union[int, str]): Unique identifier for the robot.
            name (str): Name of the robot.
            position (Tuple[float, float]): The (x, y) coordinates of the robot's position.
            orientation (float): The orientation of the robot in radians.
            energy_source (str): The energy source used by the robot, must be one of the ENERGY_SOURCE list.
            nombre_pattes (int): Number of legs the robot has.

        Raises:
            TypeError: If any of the parameters are of incorrect type.
            ValueError: If the energy source is not in the ENERGY_SOURCE list or if nombre_pattes is not a positive integer.
        """
        super().__init__(id, name, position, orientation, energy_source)

        if not isinstance(nombre_pattes, int) or nombre_pattes < 2 or nombre_pattes % 2 != 0:
            raise ValueError("Nombre de pattes doit être un entier positif multiple de 2.")
       
        self._nombre_pattes = nombre_pattes
       
    @property
    def nombre_pattes(self) -> int:
        """Get the number of legs the robot has."""
        return self._nombre_pattes

    def _calculate_speed_factor(self) -> float:
        """Calculate speed factor based on number of legs."""
        if self.nombre_pattes == 2:
            return 0.8  # Bipède : moins stable, plus lent
        elif self.nombre_pattes == 4:
            return 1.0  # Quadrupède : équilibré
        elif self.nombre_pattes == 6:
            return 1.2  # Hexapode : très stable, peut aller plus vite
        elif self.nombre_pattes == 8:
            return 1.1  # Octopode : stable mais plus lourd
        else:
            return 0.7  # Configurations inhabituelles : plus prudent

    def _calculate_energy_cost(self, distance: float) -> int:
        """Calculate energy cost for movement."""
        # More legs = more energy consumption
        base_cost = distance * 0.1
        leg_factor = self.nombre_pattes * 0.05
        return int(base_cost * (1 + leg_factor))
    
    def move(self, direction: str, distance: float) -> None:
        """
        Move the robot with legs in a specified direction by a certain distance.

        Args:
            direction (str): The direction to move ('forward', 'backward', 'left', 'right').
            distance (float): The distance to move in the specified direction.
        """
        # Check if the robot is active and able to move
        if not self.is_active:
            print(f"{self.name} is not active and cannot move.")
            return

        # Validate direction and distance
        if direction not in ['forward', 'backward', 'left', 'right']:
            raise ValueError("Direction must be one of 'forward', 'backward', 'left', or 'right'.")
        if distance <= 0:
            raise ValueError("Distance must be a positive number.")
        
        # Get current position
        current_x, current_y = self.position
        
        # Calculate new position based on direction and distance
        if direction == 'forward':
            # Se déplacer dans la direction de l'orientation actuelle
            new_x = current_x + distance * math.cos(self.orientation)
            new_y = current_y + distance * math.sin(self.orientation)
            print(f"{self.name} is moving forward by {distance} units with its {self.nombre_pattes} legs.")
        elif direction == 'backward':
            new_x = current_x - distance * math.cos(self.orientation)
            new_y = current_y - distance * math.sin(self.orientation)
            print(f"{self.name} is moving backward by {distance} units with its {self.nombre_pattes} legs.")
        elif direction == 'left':
            new_x = current_x + distance * math.cos(self.orientation + math.pi/2)
            new_y = current_y + distance * math.sin(self.orientation + math.pi/2)
            print(f"{self.name} is moving left by {distance} units with its {self.nombre_pattes} legs.")
        elif direction == 'right':
            new_x = current_x + distance * math.cos(self.orientation - math.pi/2)
            new_y = current_y + distance * math.sin(self.orientation - math.pi/2)
            print(f"{self.name} is moving right by {distance} units with its {self.nombre_pattes} legs.")
        
        # Apply the speed factor based on the number of legs
        speed_factor = self._calculate_speed_factor()
        actual_distance = distance * speed_factor
        
        # Update the robot's position
        self.position = (new_x, new_y)

        # Print the new position
        energy_cost = self._calculate_energy_cost(actual_distance)
        self.generator_level = max(0, self.generator_level - energy_cost)

    def rotate(self, angle: float) -> None:
        """
        Rotate the robot by a certain angle.
        
        Args:
            angle (float): The angle to rotate the robot, in radians.
        """
        # Check if the robot is active
        if not self.is_active:
            print(f"Robot {self.name} is inactive and cannot rotate.")
            return
            
        # Validate angle
        if not isinstance(angle, (int, float)):
            raise TypeError("Angle must be a numeric value.")
        
        # Convert angle to radians if necessary
        if angle < 0:
            print(f"{self.name} is rotating left by {-angle} radians.")
        else:
            print(f"{self.name} is rotating right by {angle} radians.")
        
        # Update orientation
        self.orientation = (self.orientation + angle) % (2 * math.pi)
        
        print(f"{self.name} has rotated to orientation {self.orientation} radians.")
        
        # Stability factor based on the number of legs.
        stability_factor = min(1.0, self.nombre_pattes / 6.0)

        # Energy consumption for rotation
        energy_cost = abs(angle) * (10 / stability_factor)
        self.generator_level = max(0, self.generator_level - int(energy_cost))

        # Check if the robot has enough energy to continue
        if self.generator_level <= 10:
            print(f"Warning: Robot {self.name} has low energy!")
    
    def stop(self) -> None:
        """
        Stop the robot's movement and stabilize all legs.
        """
        if not self.is_active:
            print(f"Robot {self.name} is already inactive.")
            return

        # Stop time based on the number of legs
        stop_efficiency = min(1.0, self.nombre_pattes / 4.0)
        stop_time = 2.0 / stop_efficiency

        # Energy cost for emergency stop
        energy_cost = 5 * (1 / stop_efficiency)
        self.generator_level = max(0, self.generator_level - int(energy_cost))

        print(f"Robot {self.name} stopping... Stabilizing {self.nombre_pattes} legs.")
        print(f"Stop time: {stop_time:.1f}s, Energy cost: {int(energy_cost)}%")
        print(f"Robot {self.name} has stopped successfully.")
        print(f"Energy remaining: {self.generator_level}%")
    
    def recharge(self) -> None:
        """
        Recharge the robot's energy source based on its energy type.
        """
        if self.generator_level >= 100:
            print(f"Robot {self.name} is already fully charged (100%).")
            return
        
        initial_level = self.generator_level

        # Recharge efficiency based on energy source
        if self.energy_source.lower() == "solar":
            recharge_rate = 15 + (self.nombre_pattes * 2)
            recharge_time = "6-8 hours"
            print(f"Solar charging initiated for {self.name}...")
            print(f"Using {self.nombre_pattes} legs as solar panel supports.")

        elif self.energy_source.lower() == "electric":
            recharge_rate = 25 + self.nombre_pattes
            recharge_time = "2-3 hours"
            print(f"Electric charging initiated for {self.name}...")
            print(f"Connecting charging cables to {self.nombre_pattes}-leg base station.")
            
        elif self.energy_source.lower() == "fossil_fuel":
            recharge_rate = 35
            recharge_time = "30 minutes"
            print(f"Fossil fuel refueling initiated for {self.name}...")
            print(f"Refueling tank (leg stability: {self.nombre_pattes} contact points).")

        # Calculate the new charge level
        self.generator_level = min(100, initial_level + recharge_rate)
        
        print(f"Recharging... {initial_level}% → {self.generator_level}%")
        print(f"Estimated time for full charge: {recharge_time}")
        
        if self.generator_level == 100:
            print(f"Robot {self.name} is now fully charged!")
        else:
            remaining = 100 - self.generator_level
            print(f"Partial recharge complete. {remaining}% remaining to full charge.")

    def status(self) -> str:
        """
        Get the current status of the robot.

        Returns:
            str: A string representation of the robot's current status.
        """
        status_info = []
        status_info.append(f"=== {self.name} Status ===")
        status_info.append(f"Type: {self.nombre_pattes}-legged robot")
        status_info.append(f"ID: {self.id}")
        status_info.append(f"Position: ({self.position[0]:.2f}, {self.position[1]:.2f})")
        status_info.append(f"Orientation: {math.degrees(self.orientation):.2f}°")
        status_info.append(f"Energy Source: {self.energy_source}")
        status_info.append(f"Battery Level: {self.generator_level}%")
        status_info.append(f"Active: {'Yes' if self.is_active else 'No'}")

        # Status specific to legs
        if self.nombre_pattes == 2:
            status_info.append("Mobility: Bipedal (human-like)")
        elif self.nombre_pattes == 4:
            status_info.append("Mobility: Quadrupedal (animal-like)")
        elif self.nombre_pattes == 6:
            status_info.append("Mobility: Hexapedal (insect-like)")
        else:
            status_info.append(f"Mobility: Multi-legged ({self.nombre_pattes} legs)")

        # Alert if low energy
        if self.generator_level <= 20:
            status_info.append("⚠️ WARNING: Low battery!")
        
        return "\n".join(status_info)

    def __str__(self) -> str:
        """
        Return a string representation of the robot.

        Returns:
            str: A string containing the robot's ID, name, position, orientation, energy source, and active status.
        """
        return (f"RobotAPattes(ID: {self.id}, Name: {self.name}, Pattes: {self.nombre_pattes}, "
                f"Position: {self.position}, Orientation: {self.orientation}, "
                f"Energy Source: {self.energy_source}, Active: {self.is_active})")

