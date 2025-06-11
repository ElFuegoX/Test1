from abc import ABC, abstractmethod
from typing import Union, Tuple

class Robot(ABC):
    """
    Abstract base class representing a robot in a simulation environment.
    """
    # Class variable to define valid energy sources
    ENERGY_SOURCE = ["solar", "fossil_fuel", "electric"]

    def  init(
            self,
            id: Union[int, str],
            name: str,
            position: Tuple[float, float],
            orientation: float,
            energy_source: str,
        ) -> None:
        """
        Initialize a Robot instance.

        Args:
            id (Union[int, str]): Unique identifier for the robot.
            name (str): Name of the robot.
            position (Tuple[float, float]): The (x, y) coordinates of the robot's position.
            orientation (float): The orientation of the robot in radians.
            energy_source (str): The energy source used by the robot, must be one of the ENERGY_SOURCE list.

        ENERGY_SOURCE is a list of valid energy sources:
            - "solar"
            - "fossil_fuel"
            - "electric"

        Raises:
            TypeError: If any of the parameters are of incorrect type.
            ValueError: If the energy source is not in the ENERGY_SOURCE list.
        """
        # Validate input types
        if not isinstance(id, (int, str)):
            raise TypeError("ID must be an integer or a string.")
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not isinstance(position, tuple) or len(position) != 2 or not all(isinstance(coord, (int, float)) for coord in position):
            raise TypeError("Position must be a tuple of two numeric values (x, y).")
        if not isinstance(orientation, (int, float)):
            raise TypeError("Orientation must be a numeric value (in radians).")
        if energy_source.lower() not in self.ENERGY_SOURCE:
            raise ValueError("Energy source must be an instance of ENERGY_SOURCE List.")

        self._id = id
        self._name = name
        self._position = position
        self._orientation = orientation
        self._energy_source = energy_source

        # Indicates if the robot is currently active
        self._is_active = True

        # Generator power level
        self._generator_level = 100

    # Properties to access robot attributes
    @property
    def id(self) -> Union[int, str]:
        """Get the unique identifier of the robot."""
        return self._id

    @property
    def name(self) -> str:
        """Get the name of the robot."""
        return self._name

    @property
    def position(self) -> Tuple[float, float]:
        """Get the current position of the robot."""
        return self._position

    @property
    def orientation(self) -> float:
        """Get the current orientation of the robot in radians."""
        return self._orientation

    @property
    def energy_source(self) -> str:
        """Get the energy source of the robot."""
        return self._energy_source

    @property
    def generator_level(self) -> int:
        """Get the current generator level of the robot."""
        return self._generator_level

    @property
    def is_active(self) -> bool:
        """Check if the robot is currently active."""
        return self._is_active

    # Setters to modify robot attributes
    @position.setter
    def position(self, new_position: Tuple[float, float]) -> None:
        """Set a new position for the robot."""
        self._position = new_position

    @orientation.setter
    def orientation(self, new_orientation: float) -> None:
        """Set a new orientation for the robot."""
        self._orientation = new_orientation

    @generator_level.setter
    def generator_level(self, new_level: int) -> None:
        """Set a new generator level for the robot."""
        self._generator_level = new_level

    @is_active.setter
    def is_active(self, active: bool) -> None:
        """Set the active status of the robot."""
        self._is_active = active

    # Abstract methods to be implemented by subclasses
    @abstractmethod
    def move(self, direction: str, distance: float) -> None:
        """
        Move the robot in a specified direction by a certain distance.

        Args:
            direction (str): The direction to move ('forward', 'backward', 'left', 'right').
            distance (float): The distance to move in the specified direction.
        """
        pass

    @abstractmethod
    def rotate(self, angle: float) -> None:
        """
        Rotate the robot by a certain angle.

        Args:
            angle (float): The angle to rotate the robot, in radians.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the robot's movement.
        """
        pass

    @abstractmethod
    def recharge(self) -> None:
        """
        Recharge the robot's energy source.
        """
        pass

    @abstractmethod
    def status(self) -> str:
        """
        Get the current status of the robot.

        Returns:
            str: A string representation of the robot's current status.
        """
        pass

    def str(self) -> str:
        """
        Return a string representation of the robot.

        Returns:
            str: A string containing the robot's ID, name, position, orientation, energy source, and active status.
        """
        return (f"Robot(ID: {self.id}, Name: {self.name}, Position: {self.position}, "
                f"Orientation: {self.orientation}, Energy Source: {self.energy_source}, "
                f"Active: {self.is_active})")

    def repr(self) -> str:
        """
        Return a detailed string representation of the robot for debugging.

        Returns:
            str: A string containing the class name and the robot's attributes.
        """
        return (f"{self.class.name}(ID={self.id}, Name={self.name}, "
                f"Position={self.position}, Orientation={self.orientation}, "
                f"Energy Source={self.energy_source}, Active={self.is_active})")

    def eq(self, other: object) -> bool:
        """
        Check if two robots are equal based on their ID.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the IDs are the same, False otherwise.
        """
        if not isinstance(other, Robot):
            return NotImplemented
        return self.id == other.id


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
        # Plus de pattes = plus de consommation énergétique
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
        # Vérifier si le robot est actif et peut se déplacer
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
        
        # Calculer les nouvelles coordonnées selon la direction
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
        
        # Appliquer le facteur de vitesse
        speed_factor = self._calculate_speed_factor()
        actual_distance = distance * speed_factor
        
        # Mettre à jour la position
        self.position = (new_x, new_y)

        # Calculer la consommation d'énergie
        energy_cost = self._calculate_energy_cost(actual_distance)
        self.generator_level = max(0, self.generator_level - energy_cost)

    def rotate(self, angle: float) -> None:
        """
        Rotate the robot by a certain angle.
        
        Args:
            angle (float): The angle to rotate the robot, in radians.
        """
        # Vérifier si le robot est actif
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
        
        # Facteur de stabilité basé sur le nombre de pattes
        stability_factor = min(1.0, self.nombre_pattes / 6.0)

        # Consommation d'énergie pour la rotation
        energy_cost = abs(angle) * (10 / stability_factor)
        self.generator_level = max(0, self.generator_level - int(energy_cost))

        # Vérifier si le robot a assez d'énergie pour continuer
        if self.generator_level <= 10:
            print(f"Warning: Robot {self.name} has low energy!")
    
    def stop(self) -> None:
        """
        Stop the robot's movement and stabilize all legs.
        """
        if not self.is_active:
            print(f"Robot {self.name} is already inactive.")
            return
        
        # Temps d'arrêt basé sur le nombre de pattes
        stop_efficiency = min(1.0, self.nombre_pattes / 4.0)
        stop_time = 2.0 / stop_efficiency
        
        # Coût énergétique pour l'arrêt d'urgence
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
        
        # Efficacité de recharge selon la source d'énergie
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

        # Calcul de la nouvelle charge
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
        
        # Status spécifique aux pattes
        if self.nombre_pattes == 2:
            status_info.append("Mobility: Bipedal (human-like)")
        elif self.nombre_pattes == 4:
            status_info.append("Mobility: Quadrupedal (animal-like)")
        elif self.nombre_pattes == 6:
            status_info.append("Mobility: Hexapedal (insect-like)")
        else:
            status_info.append(f"Mobility: Multi-legged ({self.nombre_pattes} legs)")
        
        # Alerte si énergie faible
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


# Exemple d'utilisation
import math
if __name__ == "__main__":
    # Créer un robot à 4 pattes
    robot1 = RobotAPattes(
        id=1,
        name="Rex",
        position=(0.0, 0.0),
        orientation=0.0,
        energy_source="electric",
        nombre_pattes=4
    )
    
    print(robot1)
    print(robot1.status())
    
    # Test des mouvements
    robot1.move("forward", 5.0)
    robot1.rotate(math.pi/4)  # 45 degrés
    robot1.move("left", 3.0)
    
    print(f"\nPosition finale: {robot1.position}")
    print(f"Orientation finale: {math.degrees(robot1.orientation)}°")
    print(f"Énergie restante: {robot1.generator_level}%")