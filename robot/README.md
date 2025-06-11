# Documentation de la classe RobotAPattes

## Table des matières

1. [Introduction](#introduction)
2. [Concepts de base](#concepts-de-base)
3. [Installation et configuration](#installation-et-configuration)
4. [Utilisation de base](#utilisation-de-base)
5. [Détails techniques](#détails-techniques)
6. [Exemples d'utilisation](#exemples-dutilisation)
7. [Tests](#tests)

## Introduction

La classe `RobotAPattes` représente un robot autonome terrestre se déplaçant à l'aide de pattes. Elle hérite de la classe `Robot` et y ajoute des fonctionnalités spécifiques aux robots dotés de membres articulés (pattes).

## Concepts de base

### Qu'est-ce qu'un RobotAPattes ?

Un `RobotAPattes` est un robot terrestre capable de :

* Se déplacer en avant, arrière, à gauche et à droite
* Ajuster sa vitesse en fonction du nombre de pattes
* Calculer la consommation d'énergie en fonction du déplacement

### Termes importants

* **Position (x, y)** : Coordonnées du robot dans l'espace 2D
* **Orientation** : Angle de direction du robot (en radians)
* **Nombre de pattes** : Doit être un nombre pair à partir de 2
* **Source d'énergie** : Type d'énergie utilisée (ex. batterie, solaire, etc.)

## Installation et configuration

### Prérequis

* Python 3.7 ou supérieur
* Le fichier `robot.py` contenant la classe de base `Robot`

### Installation

1. Ajoutez `robot.py` et `robotAPattes.py` à votre projet
2. Importez la classe dans votre code :

   ```python
   from robot.robotAPattes import RobotAPattes
   ```

## Utilisation de base

### Création d'un robot à pattes

```python
robot = RobotAPattes(
    id=1,
    name="SpiderBot",
    position=(0.0, 0.0),
    orientation=0.0,
    energy_source="batterie",
    nombre_pattes=6
)
```

### Déplacement manuel

```python
robot.activate()  # Active le robot
robot.move("forward", 2.0)
robot.move("left", 1.0)
```

## Détails techniques

### Attributs

* `nombre_pattes` : Nombre de pattes du robot. Accessible via `@property`, lecture seule.
* `_calculate_speed_factor()` : Renvoie un facteur de vitesse basé sur la stabilité offerte par le nombre de pattes.
* `_calculate_energy_cost(distance)` : Calcule la consommation d'énergie pour un déplacement donné.

### Calcul du facteur de vitesse

| Nombre de pattes | Facteur de vitesse |
| ---------------- | ------------------ |
| 2                | 0.8                |
| 4                | 1.0                |
| 6                | 1.2                |
| 8                | 1.1                |
| Autre            | 0.7                |

### Calcul du coût énergétique

La formule approximative est :

```
coût = distance * 0.1 * (1 + nombre_pattes * 0.05)
```

### Méthode de déplacement `move`

* Prend en argument une direction (`"forward"`, `"backward"`, `"left"`, `"right"`) et une distance positive
* Vérifie si le robot est actif avant de se déplacer
* Calcule la nouvelle position en tenant compte de l'orientation
* Affiche un message si le robot est inactif

## Exemples d'utilisation

### Patrouille simple

```python
def patrouille(robot):
    directions = ["forward", "right", "backward", "left"]
    for dir in directions:
        robot.move(dir, 2.0)
```

### Simulation d'usure d'énergie

```python
robot.activate()
for i in range(5):
    robot.move("forward", 1.0)
    print("Énergie restante:", robot.battery_level)
```

## Tests

### Test rapide

```python
robot = RobotAPattes(99, "TestBot", (0,0), 0, "solaire", 4)
robot.activate()
robot.move("forward", 5)
robot.move("right", 2)
print(robot.position)
```

### Ce qui peut être testé :

* Réaction à des directions invalides
* Réaction à des distances négatives
* Énergie consommée vs distance parcourue
* Vitesse relative selon le nombre de pattes

---

> Pour plus d'informations sur la classe parente `Robot`, référez-vous à la documentation correspondante.
